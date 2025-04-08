import logging
import re
import textwrap

import cfnlint.config
import cfnlint.core
import cfnlint.helpers
import cfnlint.version
from cfnlint.config import ConfigMixIn as CfnLintConfig
from jsonschema.exceptions import ValidationError
from taskcat._common_utils import neglect_submodule_templates
from taskcat._config import Config
from taskcat._dataclasses import Templates

# Ignoring linting errors here as pylint doesn't seem to handle the conditional nature
if cfnlint.version.__version__.startswith("0."):
    from cfnlint.core import (  # pylint:disable=no-name-in-module, ungrouped-imports
        CfnLintExitException,
    )
else:
    from cfnlint.runner import (  # pylint:disable=no-name-in-module, ungrouped-imports
        CfnLintExitException,
    )

LOG = logging.getLogger(__name__)


class Lint:

    _code_regex = re.compile("^([WER][0-9]*:)")

    def __init__(self, config: Config, templates: Templates, strict: bool = False):
        """
        Lints templates using cfn_python_lint. Uses config to define regions and
        templates to test. Recurses into child templates, excluding submodules.

        :param config: path to taskcat ci config file
        """
        self._config: Config = config
        self._templates: Templates = templates
        self._cfnlint_config = None
        try:
            self._cfnlint_config = CfnLintConfig([])
        except ValidationError as e:
            LOG.error("Error parsing cfn-lint config file: %s", str(e))
            raise

        # There is a change in the way that the cfn lint config class functions between the 0.x and 1.x versions.
        # In 1.x, the append_rules property getter includes the default rule set along with the loaded configuration
        # https://github.com/aws-cloudformation/cfn-lint/blob/23ee527fadb43e4fd54238eeea5bc3a169175c91/src/cfnlint/config.py#L773
        # In 0.x, it only returned the loaded configuration.
        # https://github.com/aws-cloudformation/cfn-lint/blob/f006cb5d8c7056923f3f21b31c14edfeed3804b5/src/cfnlint/config.py#L730
        #
        # This causes issues for us as the get_rules method combines the supplied value with the default rule list,
        # resulting in a duplicate rule error. get_rules has always behaved this way though, so not sure if we have just missed something
        # in the intended approach to calling this.
        if cfnlint.version.__version__.startswith("0."):
            append_rules = self._cfnlint_config.append_rules
        else:
            append_rules = self._cfnlint_config.append_rules
            append_rules.remove(cfnlint.config._DEFAULT_RULESDIR)

        self._rules = cfnlint.core.get_rules(
            append_rules,
            self._cfnlint_config.ignore_checks,
            self._cfnlint_config.include_checks,
            self._cfnlint_config.configure_rules,
            self._cfnlint_config.include_experimental,
            self._cfnlint_config.mandatory_checks,
        )
        if self._cfnlint_config.override_spec:
            cfnlint.helpers.override_specs(self._cfnlint_config.override_spec)
        self.lints = self._lint()
        self.strict: bool = strict

    @staticmethod
    def _filter_unsupported_regions(regions):
        lint_regions = set(cfnlint.helpers.REGIONS)
        if set(regions).issubset(lint_regions):
            return regions
        supported = set(regions).intersection(lint_regions)
        unsupported = set(regions).difference(lint_regions)
        LOG.error(
            "The following regions are not supported by cfn-python-lint and will "
            "not be linted %s",
            unsupported,
        )
        return list(supported)

    def _lint(self):
        lints = {}
        lint_errors = set()

        for name, test in self._config.config.tests.items():
            lints[name] = {"regions": self._filter_unsupported_regions(test.regions)}
            lints[name]["template"] = self._templates[name].template_path
            lints[name]["results"] = {}

            templates = []
            for template in self._templates.values():
                templates.append(template)
                templates += list(template.descendents)
            templates = neglect_submodule_templates(
                self._config.project_root, templates
            )
            templates = set(templates)
            for template in templates:
                self._run_checks(template, name, lint_errors, lints)
            for err in lint_errors:
                LOG.error(err)
        for test in lints:  # pylint: disable=consider-using-dict-items
            for result in lints[test]["results"]:
                if lints[test]["results"][result]:
                    if self._is_error(lints[test]["results"][result]):
                        lint_errors.add(result)
        return lints, lint_errors

    def _run_checks(self, template, name, lint_errors, lints):
        tpath = str(template.template_path)
        results = []
        try:
            results = cfnlint.core.run_checks(
                tpath, template.template, self._rules, lints[name]["regions"]
            )
            lints[name]["results"][tpath] = results
        except CfnLintExitException as e:
            lint_errors.add(str(e))
        lints[name]["results"][tpath] = results

    def output_results(self):  # noqa: C901
        """
        Prints lint results to terminal using taskcat console formatting

        :return:
        """
        passed = set()
        issue = {"warning": {}, "error": {}}
        lints = self.lints[0]
        for test in lints:  # pylint: disable=consider-using-dict-items
            for result in lints[test]["results"]:
                if not lints[test]["results"][result]:
                    passed.add(result)
                else:
                    if self._is_error(lints[test]["results"][result]):
                        if result in issue["error"]:
                            continue
                        issue["error"][result] = lints[test]["results"][result]
                    else:
                        if result in issue["warning"]:
                            continue
                        issue["warning"][result] = lints[test]["results"][result]
        for filename in passed:
            LOG.info(f"Linting passed for file: {filename}")
        for filename, result_data in issue["warning"].items():
            LOG.warning("---")
            LOG.warning(f"Linting detected issues in: {filename}")
            for result_message in result_data:
                self._format_message(result_message, result_data)
        for filename, result_data in issue["error"].items():
            LOG.error("---")
            LOG.error(f"Linting detected issues in: {filename}")
            for result_message in result_data:
                self._format_message(result_message, result_data)

    @property
    def passed(self):
        for test in self.lints[0]:
            for template in self.lints[0][test]["results"]:
                results = self.lints[0][test]["results"][template]
                if results:
                    if self._is_error(results) or self.strict:
                        return False
        return True

    @staticmethod
    def _is_error(messages):
        for message in messages:
            sev = message.__str__().lstrip("[")[0]
            if sev == "E":
                return True
        return False

    @staticmethod
    def _format_message(message, full_results):
        sev = message.rule.id[0]
        code = message.rule.id[1:]
        prefix = f"    line {message.linenumber} [{code}] [{message.rule.shortdesc}] "
        indent = "\n" + " " * (2 + len(prefix))
        message = indent.join(textwrap.wrap(message.message, 141 - (len(indent) + 11)))
        message = prefix + message
        if sev == "E":
            LOG.error(message)
        elif sev == "W":
            if "E" + code not in [r.__str__().lstrip("[") for r in full_results]:
                LOG.warning(message)
        else:
            LOG.error("linter produced unkown output: " + message)
