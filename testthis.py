import jsonschema
from jsonschema import Draft7Validator
from titlecase import titlecase
import yaml

# Create a function to check if a string is title case
def is_title_case(validator, value, instance, schema):
    if schema and not instance == titlecase(instance):
        yield jsonschema.ValidationError(f"{instance} is not in title case")

"""
# Create a function to check if a string is snake case
def is_snake_case(validator, value, instance, schema):
    if schema and not re.fullmatch(r'^[a-z0-9_]+$', instance):
        yield jsonschema.ValidationError(f"{instance} is not in snake case")
"""

"""
# Extend Draft7Validator with the new checks
Draft7ValidatorWithCaseCheck = jsonschema.validators.extend(
    Draft7Validator, validators={"titleCase": is_title_case, "snakeCase": is_snake_case}
)
"""

# Extend Draft7Validator with the new check
Draft7ValidatorWithCaseCheck = jsonschema.validators.extend(
    Draft7Validator, validators={"titleCase": is_title_case}
)

# Define a JSON schema for validation


"""
schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "titleCase": True
        },
        "name": {
            "type": "string",
            "snakeCase": True
        }
    },
}
"""

schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "titleCase": True
        }
    },
}

# Load YAML file

data = {"title": "this is not a title case"}


# Validate the YAML data against the schema
validator = Draft7ValidatorWithCaseCheck(schema)
errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
for error in errors:
    print(error)
