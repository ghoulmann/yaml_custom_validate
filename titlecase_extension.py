
import titlecase

def validate_titlecase(data):
    if data != titlecase.titlecase(data):
        raise AssertionError("Value must be in title case.")
        return False
    else:
        return True
