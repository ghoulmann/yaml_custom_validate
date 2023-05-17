import argparse
import jsonschema
from titlecase import titlecase


class TitleCaseValidator(jsonschema.validators.AbstractValidator):
    """
    A validator that checks if a value is in title case.
    """

    def __init__(self, message=None):
        super().__init__(message=message)

    def validate(self, value, schema=None, instance=None, path=None, **kwargs):
        if not isinstance(value, str):
            return

        if not titlecase(value).lower() == value.lower():
            raise jsonschema.ValidationError(
                self.message or "Value is not in title case."
            )


jsonschema.validators.register_validator("titlecase", TitleCaseValidator)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("yaml_file", type=str)
    parser.add_argument("-s", "--schema", type=str, default="schema.json")
    args = parser.parse_args()

    with open(args.yaml_file, "r") as f:
        data = f.read()

    with open(args.schema, "r") as f:
        schema = json.load(f)

    try:
        jsonschema.validate(data, schema, titlecase=True)
    except jsonschema.ValidationError as e:
        print(f"{args.yaml_file}:{e.context['line']}:{e.context['path']}:{e.message}")


if __name__ == "__main__":
    main()
