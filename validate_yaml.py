import argparse
import traceback
#from ruamel.yaml import YAML
import yamllint
from yamllint.config import YamlLintConfig
from titlecase import titlecase
import jsonschema
from jsonschema.validators import Draft7Validator
import sys
import json
import yaml
from jsonschema import ValidationError

# Custom validator
def validate_title_case(validator, value, instance, schema):
    if titlecase(instance) != instance:
        error_message = f"Value '{instance}' is not in title case."
        error = ValidationError(error_message)
        error.path = list(validator.path)
        validator.errors.append(error)


class CustomValidator:
    def __init__(self, schema):
        self.validator = Draft7Validator(schema)
        self.validator.VALIDATORS["title_case_validator"] = validate_title_case

    def validate(self, data):
        return self.validator.validate(data)

    def iter_errors(self, data):
        return self.validator.iter_errors(data)


def lint_yaml_file(yaml_file):
    # Create yamllint configuration with rules to check for trailing spaces and missing newline
    yamllint_config = YamlLintConfig(
        """
        extends: default
        rules:
          quoted-strings:
            required: only-when-needed
          trailing-spaces: {}
          line-length:
            max: 80
          document-start:
            present: false
          new-line-at-end-of-file: disable
        """
    )

    # Run yamllint on YAML file with the created configuration
    try:
        for p in yamllint.linter.run(open(yaml_file, "r"), yamllint_config):
            print(f"{p.level}: {p.line}, {p.column} - {p.desc}")


    except Exception as e:
        print(e)



def validate_yaml(schema_file, yaml_file):

    # Create a YAML parser
    #yaml = YAML(typ="safe")

    # Load the YAML data preserving the order
    with open(yaml_file) as f:
        data = yaml.safe_load(f)

    # Load the JSONSchema
    with open(schema_file) as f:
        schema = json.load(f)

    # Create a CustomValidator instance and validate the YAML data against the JSONSchema
    validator = CustomValidator(schema)

    errors = validator.iter_errors(data)

    if errors:

        return errors

    else:
        return("No validation errors")

    # If there are no validation errors, return True
    #return True
    """
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
        return False
    """
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("yaml_file", help="The path to the YAML file to validate.")
    parser.add_argument(
        "-s", "--schema_file",
        default="schema.json",
        help="The path to the JSONSchema file to use for validation.",
    )
    args = parser.parse_args()

    lint_yaml_file(args.yaml_file)

    for e in validate_yaml(args.schema_file, args.yaml_file):
        print(e.message)


if __name__ == "__main__":
    main()
