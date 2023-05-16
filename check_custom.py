import sys
import json
import yaml
import jsonschema
from jsonschema.validators import Draft7Validator
from jsonschema.validators import create
from titlecase import titlecase

def validate_title_case(validator, value, instance, schema):
    if titlecase(instance) != instance:
        error_message = f"Value '{instance}' is not in title case."
        error = jsonschema.ValidationError(error_message)
        error.path = list(validator.path)
        validator.errors.append(error)

custom_validators = {
    "title_case_validator": validate_title_case
}

CustomValidator = create(
    Draft7Validator.META_SCHEMA,
    validators=custom_validators,
)

schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "pattern": "^[A-Z]{2}\\d{3}$"
            },
            "description": {
                "type": "string",
                "pattern": "^[A-Z][a-zA-Z ]+$",
                "title_case_validator": {}
            },
            "location": {
                "type": "string",
                "pattern": "^[a-z_]+$"
            }
        },
        "required": ["code", "description", "location"],
        "propertyOrder": ["code", "description", "location"],
        "additionalProperties": True,
        "minProperties": 3
    }
}

validator = CustomValidator(schema)

def validate_yaml(yaml_file):
    with open(yaml_file) as f:
        yaml_data = yaml.safe_load(f)

    errors = list(validator.iter_errors(yaml_data))

    if errors:
        for error in errors:
            print(error.message)
        return False
    else:
        print("Validation successful!")
        return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_yaml.py <yaml_file>")
        sys.exit(1)

    yaml_file = sys.argv[1]
    validate_yaml(yaml_file)

if __name__ == "__main__":
    main()
