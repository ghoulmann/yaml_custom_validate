import jsonschema
import titlecase

# Custom validator function
def validate_title_case(validator, value, instance, schema):
    # Check if the instance value is in title case
    if titlecase.titlecase(instance) != instance:
        error_message = f"Value '{instance}' is not in title case."
        error = jsonschema.ValidationError(error_message)
        validator.errors.append(error)