import jsonschema
from jsonschema import Draft7Validator
from titlecase import titlecase
import yaml

# Create a function to check if a string is title case
def is_title_case(validator, value, instance, schema):
    if not instance == titlecase(instance):
        yield jsonschema.ValidationError(f"{instance} is not in title case")

# Extend Draft7Validator with the new check
Draft7ValidatorWithCaseCheck = jsonschema.validators.extend(
    Draft7Validator, validators={"titleCase": is_title_case}
)

# Define a JSON schema for validation
schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "titleCase": {}
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
