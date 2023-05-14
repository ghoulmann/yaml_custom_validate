import sys
import re
import yaml
import titlecase


def validate_key_presence(key, data, rules, line_num):
    """
    Validate that a required key is present in the YAML file.
    """
    if key not in data:
        print(f"Error: Line {line_num} - Required key '{key}' is missing.")
        return False

    return True


def validate_title_case(key, data, rules, line_num):                                                                                                                                         
    """                                                                                                                                                                                      
    Validate that a key is in title case (first letter of each word                                                                                                                       
    capitalized).                                                                                                                                                                            
    """                                                                                                                                                                                      
    if key in data and titlecase(titlecase.titlecase(data[key])) != data[key]:                                                                                                               
        print(f"Error: Line {line_num} - '{key}' must be in title case.")                                                                                                                    
        return False                                                                                                                                                                         
                                                                                                                                                                                            
    return True


def validate_snake_case(key, data, rules, line_num):
    """
       Validate that a key is in snake_case (lowercase, with underscores instead
    spaces).
    """
    if key in data and not re.match(r"[a-z]+(_[a-z]+)*", data[key]):
        print(f"Error: Line {line_num} - '{key}' must be in snake_case.")
        return False

    return True


def validate_regex(key, data, rules, line_num):
    """
       Validate that a key matches a regular expression pattern defined in the
    configuration file.
    """
    pattern = rules.get(key, {}).get("regex")
    if pattern and key in data and not re.match(pattern, data[key]):
        print(
            f"Error: Line {line_num} - '{key}' must match the regex pattern '{pattern}'."
        )
        return False

    return True


def validate_data_type(key, data, rules, line_num):
    """
       Validate that a key has a value of a specific data type specified in the
    configuration file.
    """
    data_type = rules.get(key, {}).get("type")
    if data_type and key in data and not isinstance(data[key], data_type):
        print(
            f"Error: Line {line_num} - '{key}' must be of type '{data_type.__name__}'."
        )
        return False

    return True

def validate_spacing(key, data, line_num):
    """
    Validate that a key has no trailing white space and conforms to YAML syntax.
    """
    if key in data:
        value = str(data[key])
        if len(value) > 0 and (value[-1] == " " or value[0] == " "):
            print(
                f"Error: Line {line_num} - '{key}' must not have any trailing or leading white space."
            )
            return False
        if not re.match(r"^([^-].*):[^:].*$", value):
            print(f"Error: Line {line_num} - '{key}' must conform to YAML syntax.")
            return False

    return True


def validate_dict_keys(key, data, rules, line_num):
    """
    Validate that the keys in a dictionary match the allowed list of keys
    specified in the configuration file, and that the keys appear in the corre
    order.
    """
    allowed_keys = rules.get(key, {}).get("keys", [])
    if key in data and isinstance(data[key], dict):
        # Check for additional keys in the dictionary
        extra_keys = set(data[key].keys()) - set(allowed_keys)
        if extra_keys:
            print(
                f"Error: Line {line_num} - '{key}' dictionary has extra key(s) {', '.join(sorted(extra_keys))}"
            )
            return False

        # Check that all required keys are present
        missing_keys = set(allowed_keys) - set(data[key].keys())
        if missing_keys:
            print(
                f"Error: Line {line_num} - '{key}' dictionary is missing required key(s): {', '.join(sorted(missing_keys))}"
            )
            return False

        # Check that keys appear in the correct order
        key_index = {k: i for i, k in enumerate(allowed_keys)}
        prev_key_index = -1
        for subkey in sorted(data[key].keys(), key=lambda k: key_index[k]):
            if key_index[subkey] < prev_key_index:
                print(
                    f"Error: Line {line_num} - '{key}' dictionary has incorrect ordering of keys."
                )
                return False
            prev_key_index = key_index[subkey]

        # Validate the subkeys
        for subkey in allowed_keys:
            if subkey not in data[key]:
                continue
            if not validate_quotes(subkey, data[key], rules, line_num):
                return False
            if not validate_spacing(subkey, data[key], rules, line_num):
                return False

    return True


def validate_quotes(key, data, rules, line_num):
    """
        Validate that the value for a key is enclosed in quotes if it requires
    quotes according to YAML syntax.
    """
    value = data.get(key)
    if isinstance(value, str):
        # Check if quotes are required according to YAML syntax
        requires_quotes = (
            "|" in value
            or "\n" in value
            or ":" in value
            or '"' in value
            or "'" in value
            or value.startswith("<")
            or value.endswith(">")
        )

        # Check if quotes are present or absent as required
        if requires_quotes and not (value.startswith('"') and value.endswith('"')):
            quote_type = "double" if "'" in value else "single"
            print(
                f"Error: Line {line_num} - '{key}' must be enclosed in {quote_type} quotes."
            )
            return False
        elif not requires_quotes and (value.startswith('"') and value.endswith('"')):
            quote_type = "double" if "'" in value else "single"
            print(
                f"Error: Line {line_num} - '{key}' must not be enclosed in {quote_type} quotes."
            )
            return False

    return True


def check_unique_value(key, data, rules, line_num):
    unique_values = []
    if rules.get(key, {}).get("unique", False):
        value = data[key]
        for k, v in data.items():
            if k != key and v == value:
                print(f"Error: Line {line_num} - Value for key '{key}' is not unique.")
                return False
    return True


def check_yaml_lint(file_path):
    """
        Check a YAML file for lint errors using PyYAML's load_all function, and
    output any errors to the console.
    """
    with open(file_path, "r") as f:
        try:
            for i, _ in enumerate(yaml.load_all(f, Loader=yaml.SafeLoader), 1):
                pass
            return True
        except yaml.MarkedYAMLError as e:
            problem_mark = e.problem_mark
            print(
                f"Error: {file_path} - On line {problem_mark.line}, column {problem_mark.column}: {e.problem}"
            )
            return False


def validate_yaml_file(file_path, config_file):
    """
        Validate a YAML file against a set of predefined rules, and check for lint
    errors.
    """
    # Check for YAML lint errors first
    if not check_yaml_lint(file_path):
        sys.exit(1)

    # Load the YAML file with line numbers
    with open(file_path, "r") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        line_num = f.readline().count("\n") + 1

        while f.readline():
            line_num += 1

    # Load the configuration file
    with open(config_file, "r") as f:
        rules = yaml.load(f, Loader=yaml.SafeLoader)["rules"]

    # Validate each key based on the defined rules
    for key in rules:
        validate_key_presence(key, data, rules, line_num)
        validate_title_case(key, data, rules, line_num)
        validate_snake_case(key, data, rules, line_num)
        validate_regex(key, data, rules, line_num)
        validate_data_type(key, data, rules, line_num)
        validate_spacing(key, data, rules, line_num)
        validate_dict_keys(key, data, rules, line_num)
        validate_quotes(key, data, rules, line_num)
        check_unique_value(key, data, rules, line_num)

    return True


if __name__ == "__main__":                                                                                                                                                                   
    # Set up argparse to parse command-line arguments                                                                                                                                        
    parser = argparse.ArgumentParser(description="Validate a YAML file")                                                                                                                     
    parser.add_argument("yaml_file", help="Path to YAML file to validate")                                                                                                                   
    parser.add_argument(                                                                                                                                                                     
        "-c",                                                                                                                                                                                
        "--config",                                                                                                                                                                          
        default="config.yaml",                                                                                                                                                               
        help="Path to configuration file (default: 'config.yaml')",                                                                                                                          
    )                                                                                                                                                                                        
                                                                                                                                                                                            
    # Parse command-line arguments                                                                                                                                                           
    args = parser.parse_args()                                                                                                                                                               
                                                                                                                                                                                            
    # Validate the YAML file                                                                                                                                                                 
    if not validate_yaml_file(args.yaml_file, args.config):                                                                                                                                  
        sys.exit(1)