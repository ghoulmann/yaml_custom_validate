1 / 1

Finished browsing

Searched: “Python package requirements for argparse, yaml, sys, jsonschema, titlecase”

Searched: “argparse PyPI”

Reading content

Searched: “PyYAML PyPI”

Reading content

Searched: “jsonschema PyPI”

Reading content

Searched: “titlecase PyPI”

Reading content

Finished browsing

README.md
=========

Introduction
------------

This repository contains a Python script for validating YAML data against a JSON schema. It uses the `jsonschema` Python package and extends its functionality with custom validators. The script takes a YAML file and a JSON schema file as input and outputs validation errors if any are found in the YAML data.

Prerequisites
-------------

Ensure you have Python 3 installed on your system.

Installation
------------

Clone this repository to your local machine.

Required Packages
-----------------

The script requires the following Python packages:

*   argparse 1.4.0​[1](https://pypi.org/project/argparse/)​
*   PyYAML 6.0​[2](https://libraries.io/pypi/PyYAML)​
*   jsonschema 4.17.3​3​
*   titlecase 2.4​[4](https://pypi.org/project/titlecase/)​

You can install these packages using pip:

bashCopy code

`pip install argparse==1.4.0 PyYAML==6.0 jsonschema==4.17.3 titlecase==2.4`

Usage
-----

`python yaml_validator.py -s schema.json data.yaml`

Where `schema.json` is the JSON schema file and `data.yaml` is the YAML file you want to validate.

Extending with More Validators
------------------------------

You can extend the functionality of the script with more validators by adding them to the `validators.py` file. Each validator is a function that takes four arguments: the validator, the value of the schema keyword, the instance, and the schema. The function should yield a `ValidationError` if the instance is invalid.

Example
-------

Let's consider the following example:

### Example Schema (schema.json)

```json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "titlecase": true
    }
  }
}
```

### Example YAML (data.yaml)


`title: "this is a title"`

### Example Output

If you run the script with the above schema and data:



`python yaml_validator.py -s schema.json data.yaml`

It will output:

```shell
this is a title is not in title case (1/code)
```

Contributing
------------

Contributions are welcome! Please feel free to submit a Pull Request.

License
-------

This project is licensed under the MIT License.
