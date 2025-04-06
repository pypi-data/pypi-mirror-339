import os

def load_env_file(path=".env") -> dict:
    """
    Load environment variables from a .env file into os.environ.
    Returns a dictionary of the loaded values.
    """
    if not os.path.exists(path):
        print(f"⚠️ .env file not found at {path}, skipping load.")
        return {}

    env_vars = {}

    with open(path, "r") as file:
        for lineno, line in enumerate(file, start=1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue  # Skip comments or blank lines

            if "=" not in line:
                raise ValueError(f"Invalid format on line {lineno}: {line}")

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            env_vars[key] = value
            os.environ[key] = value  # Optionally load into os.environ

    return env_vars


def apply_schema(raw_env: dict, schema: dict) -> dict:
    validated = {}

    for key, rules in schema.items():
        value = raw_env.get(key)

        # Required check
        if rules.get("required") and value is None:
            raise ValueError(f"Missing required env var: {key}")

        # Type casting
        if value is not None:
            expected_type = rules.get("type", str)
            value = cast_value(value, expected_type)

        # Default fallback
        if value is None and "default" in rules:
            value = rules.get("default")

        validated[key] = value

    return validated


def cast_value(value, expected_type):
    if expected_type == bool:
        return str(value).strip().lower() in ["true", "1", "yes", "on"]
    elif expected_type == int:
        return int(value)
    elif expected_type == float:
        return float(value)
    elif expected_type == str:
        return str(value).strip()
    else:
        raise ValueError(f"Unsupported type for value: {value}")