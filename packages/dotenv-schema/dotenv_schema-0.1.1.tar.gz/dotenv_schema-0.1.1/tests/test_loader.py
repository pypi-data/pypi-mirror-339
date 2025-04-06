import os
import tempfile
import unittest
from unittest.mock import patch

from dotenv_schema.loader import load_env_file, apply_schema, cast_value


class TestLoadEnvFile(unittest.TestCase):
    def setUp(self):
        # Save original environment variables
        self.original_environ = os.environ.copy()

    def tearDown(self):
        # Restore original environment variables
        os.environ.clear()
        os.environ.update(self.original_environ)

    def test_load_valid_env_file(self):
        # Create a temporary .env file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
            temp.write("TEST_VAR=test_value\n")
            temp.write("ANOTHER_VAR=another_value\n")
            temp_path = temp.name

        try:
            # Load the env file
            env_vars = load_env_file(temp_path)

            # Check that variables were loaded correctly
            self.assertEqual(env_vars["TEST_VAR"], "test_value")
            self.assertEqual(env_vars["ANOTHER_VAR"], "another_value")

            # Check that variables were added to os.environ
            self.assertEqual(os.environ["TEST_VAR"], "test_value")
            self.assertEqual(os.environ["ANOTHER_VAR"], "another_value")
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)

    def test_load_env_file_with_quotes(self):
        # Create a temporary .env file with quoted values
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
            temp.write('QUOTED_VAR="quoted value"\n')
            temp.write("SINGLE_QUOTED='single quoted value'\n")
            temp_path = temp.name

        try:
            # Load the env file
            env_vars = load_env_file(temp_path)

            # Check that quotes were stripped
            self.assertEqual(env_vars["QUOTED_VAR"], "quoted value")
            self.assertEqual(env_vars["SINGLE_QUOTED"], "single quoted value")
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)

    def test_load_env_file_with_comments_and_empty_lines(self):
        # Create a temporary .env file with comments and empty lines
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
            temp.write("# This is a comment\n")
            temp.write("\n")  # Empty line
            temp.write("TEST_VAR=test_value\n")
            temp.write("   # Indented comment\n")
            temp.write("ANOTHER_VAR=another_value\n")
            temp_path = temp.name

        try:
            # Load the env file
            env_vars = load_env_file(temp_path)

            # Check that only variables were loaded
            self.assertEqual(len(env_vars), 2)
            self.assertEqual(env_vars["TEST_VAR"], "test_value")
            self.assertEqual(env_vars["ANOTHER_VAR"], "another_value")
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)

    def test_load_nonexistent_env_file(self):
        # Try to load a non-existent file
        with patch('builtins.print') as mock_print:
            env_vars = load_env_file("nonexistent_file.env")

            # Check that warning was printed
            mock_print.assert_called_once()

            # Check that an empty dict was returned
            self.assertEqual(env_vars, {})

    def test_invalid_format_in_env_file(self):
        # Create a temporary .env file with invalid format
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
            temp.write("TEST_VAR=test_value\n")
            temp.write("INVALID_LINE\n")  # No equals sign
            temp_path = temp.name

        try:
            # Try to load the env file, should raise ValueError
            with self.assertRaises(ValueError) as context:
                load_env_file(temp_path)

            # Check the error message
            self.assertIn("Invalid format on line 2", str(context.exception))
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)


class TestApplySchema(unittest.TestCase):
    def test_apply_schema_with_required_fields(self):
        # Create a raw env dict and schema
        raw_env = {"REQUIRED_VAR": "value", "OPTIONAL_VAR": "optional"}
        schema = {
            "REQUIRED_VAR": {"required": True},
            "OPTIONAL_VAR": {"required": False},
            "MISSING_VAR": {"required": True}
        }

        # Should raise ValueError for missing required field
        with self.assertRaises(ValueError) as context:
            apply_schema(raw_env, schema)

        # Check the error message
        self.assertIn("Missing required env var: MISSING_VAR", str(context.exception))

    def test_apply_schema_with_type_casting(self):
        # Create a raw env dict and schema with type casting
        raw_env = {
            "STRING_VAR": "string value",
            "INT_VAR": "42",
            "FLOAT_VAR": "3.14",
            "BOOL_VAR_TRUE": "true",
            "BOOL_VAR_FALSE": "false"
        }
        schema = {
            "STRING_VAR": {"type": str},
            "INT_VAR": {"type": int},
            "FLOAT_VAR": {"type": float},
            "BOOL_VAR_TRUE": {"type": bool},
            "BOOL_VAR_FALSE": {"type": bool}
        }

        # Apply the schema
        validated = apply_schema(raw_env, schema)

        # Check that values were cast to the correct types
        self.assertEqual(validated["STRING_VAR"], "string value")
        self.assertEqual(validated["INT_VAR"], 42)
        self.assertEqual(validated["FLOAT_VAR"], 3.14)
        self.assertEqual(validated["BOOL_VAR_TRUE"], True)
        self.assertEqual(validated["BOOL_VAR_FALSE"], False)

    def test_apply_schema_with_default_values(self):
        # Create a raw env dict and schema with default values
        raw_env = {"EXISTING_VAR": "value"}
        schema = {
            "EXISTING_VAR": {"type": str},
            "MISSING_VAR": {"default": "default value"},
            "MISSING_INT": {"type": int, "default": 42},
            "MISSING_BOOL": {"type": bool, "default": True}
        }

        # Apply the schema
        validated = apply_schema(raw_env, schema)

        # Check that default values were used for missing variables
        self.assertEqual(validated["EXISTING_VAR"], "value")
        self.assertEqual(validated["MISSING_VAR"], "default value")
        self.assertEqual(validated["MISSING_INT"], 42)
        self.assertEqual(validated["MISSING_BOOL"], True)


class TestCastValue(unittest.TestCase):
    def test_cast_to_bool(self):
        # Test various boolean string representations
        self.assertTrue(cast_value("true", bool))
        self.assertTrue(cast_value("True", bool))
        self.assertTrue(cast_value("TRUE", bool))
        self.assertTrue(cast_value("yes", bool))
        self.assertTrue(cast_value("1", bool))
        self.assertTrue(cast_value("on", bool))

        self.assertFalse(cast_value("false", bool))
        self.assertFalse(cast_value("False", bool))
        self.assertFalse(cast_value("FALSE", bool))
        self.assertFalse(cast_value("no", bool))
        self.assertFalse(cast_value("0", bool))
        self.assertFalse(cast_value("off", bool))
        self.assertFalse(cast_value("anything else", bool))

    def test_cast_to_int(self):
        # Test casting to int
        self.assertEqual(cast_value("42", int), 42)
        self.assertEqual(cast_value("-42", int), -42)
        self.assertEqual(cast_value("0", int), 0)

        # Should raise ValueError for non-integer strings
        with self.assertRaises(ValueError):
            cast_value("not an int", int)

    def test_cast_to_float(self):
        # Test casting to float
        self.assertEqual(cast_value("3.14", float), 3.14)
        self.assertEqual(cast_value("-3.14", float), -3.14)
        self.assertEqual(cast_value("0.0", float), 0.0)
        self.assertEqual(cast_value("42", float), 42.0)

        # Should raise ValueError for non-float strings
        with self.assertRaises(ValueError):
            cast_value("not a float", float)

    def test_cast_to_string(self):
        # Test casting to string
        self.assertEqual(cast_value("string", str), "string")
        self.assertEqual(cast_value("  string with spaces  ", str), "string with spaces")
        self.assertEqual(cast_value("42", str), "42")

    def test_unsupported_type(self):
        # Test casting to an unsupported type
        with self.assertRaises(ValueError) as context:
            cast_value("value", list)

        # Check the error message
        self.assertIn("Unsupported type for value", str(context.exception))


if __name__ == "__main__":
    unittest.main()
