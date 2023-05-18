# yaml_validator.py
import argparse
import yaml
import sys
import jsonschema
from validators import is_title_case
from jsonschema import Draft7Validator

# Extend Draft7Validator with the new check
Draft7ValidatorWithCaseCheck = jsonschema.validators.extend(
    Draft7Validator, validators={"titlecase": is_title_case}
)

def main():
    # Create a parser
    parser = argparse.ArgumentParser(description='Validate YAML data against a JSON schema.')
    parser.add_argument('-s', '--schema', help='The path to the schema file')
    parser.add_argument('file', help='The file to be validated')

    # Parse the arguments
    args = parser.parse_args()

    # Load the schema
    with open(args.schema, 'r') as f:
        schema = yaml.safe_load(f)

    # Load the data
    with open(args.file, 'r') as f:
        data = yaml.safe_load(f)

    # Validate the data against the schema
    validator = Draft7ValidatorWithCaseCheck(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

    # Check if there are any errors
    if errors:
        print('\n'.join(f"{e.message} ({'/'.join(map(str, e.path))})" for e in errors))
        sys.exit(1)  # Exit with failure status
    else:
        print("Validation passed successfully.")
        sys.exit(0)  # Exit with success status

if __name__ == "__main__":
    main()
