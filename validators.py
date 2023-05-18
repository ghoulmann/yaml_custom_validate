# validators.py
from titlecase import titlecase
import jsonschema

def is_title_case(validator, value, instance, schema):
    if schema and not instance == titlecase(instance):
        yield jsonschema.ValidationError(f"{instance} is not in title case")
