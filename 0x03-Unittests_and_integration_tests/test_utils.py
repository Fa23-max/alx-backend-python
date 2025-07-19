import unittest
#!/usr/bin/env python3
# --- The function to be tested (access_nested_map) ---
import unittest
from parameterized import parameterized # Import parameterized

def access_nested_map(nested_map, path):
    """
    Accesses a value in a nested dictionary (map) given a list of keys (path).

    Args:
        nested_map (dict): The nested dictionary to navigate.
        path (list): A list of keys representing the path to the desired value.

    Returns:
        Any: The value found at the specified path.

    Raises:
        KeyError: If any key in the path does not exist in the nested map.
    """
    current_level = nested_map
    for key in path:
        if not isinstance(current_level, dict) or key not in current_level:
            # The error message should accurately reflect what was not found
            # and where. The current message is fine for this context.
            raise KeyError(f"Key '{key}' not found in the nested map.")
        current_level = current_level[key]
    return current_level

# --- The Test Class ---
class TestAccessNestedMap(unittest.TestCase):
    """
    Test suite for the access_nested_map function.
    """

    def test_access_nested_map(self):
        """
        Tests that access_nested_map returns the correct value for various
        valid nested map and path combinations.
        """
        # Test Case 1: Simple nested map, single key path
        nested_map_1 = {"a": 1}
        path_1 = ["a"]
        self.assertEqual(access_nested_map(nested_map_1, path_1), 1)

        # Test Case 2: Deeper nested map, multiple key path
        nested_map_2 = {"a": {"b": 2}}
        path_2 = ["a", "b"]
        self.assertEqual(access_nested_map(nested_map_2, path_2), 2)

        # Test Case 3: Even deeper nested map
        nested_map_3 = {"a": {"b": {"c": 3}}}
        path_3 = ["a", "b", "c"]
        self.assertEqual(access_nested_map(nested_map_3, path_3), 3)

        # Test Case 4: Different keys and values
        nested_map_4 = {"data": {"user": {"id": 123, "name": "Alice"}}}
        path_4_id = ["data", "user", "id"]
        path_4_name = ["data", "user", "name"]
        self.assertEqual(access_nested_map(nested_map_4, path_4_id), 123)
        self.assertEqual(access_nested_map(nested_map_4, path_4_name), "Alice")

        # Test Case 5: Path leading to a dictionary (not a leaf value)
        nested_map_5 = {"config": {"settings": {"theme": "dark"}}}
        path_5 = ["config", "settings"]
        self.assertEqual(access_nested_map(nested_map_5, path_5), {"theme": "dark"})

        # Test Case 6: Empty path (should return the original map)
        nested_map_6 = {"x": {"y": 10}}
        path_6_empty = []
        self.assertEqual(access_nested_map(nested_map_6, path_6_empty), nested_map_6)
        # Verify it's the same object for empty path
        self.assertIs(access_nested_map(nested_map_6, path_6_empty), nested_map_6)


    def test_access_nested_map_key_error(self):
        """
        Tests that access_nested_map raises a KeyError for invalid paths.
        """
        nested_map = {"a": {"b": {"c": 3}}}

        # Test Case 7: Key not found at the first level
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, ["d"])
        self.assertEqual(str(cm.exception), "Key 'd' not found in the nested map.") # Removed outer quotes

        # Test Case 8: Key not found at an intermediate level
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, ["a", "d"])
        self.assertEqual(str(cm.exception), "Key 'd' not found in the nested map.") # Removed outer quotes

        # Test Case 9: Key not found at the deepest level
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, ["a", "b", "d"])
        self.assertEqual(str(cm.exception), "Key 'd' not found in the nested map.") # Removed outer quotes

        # Test Case 10: Path goes beyond existing nested dicts
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, ["a", "b", "c", "d"])
        # The error message will reflect the last key that failed
        self.assertEqual(str(cm.exception), "Key 'd' not found in the nested map.") # Removed outer quotes


    def test_access_nested_map_type_error(self):
        """
        Tests that access_nested_map handles non-dictionary intermediate values gracefully
        (or raises an appropriate error if the current level is not a dict).
        """
        nested_map = {"a": {"b": "not_a_dict"}}

        # Test Case 11: Attempt to access a key on a non-dictionary value
        with self.assertRaises(KeyError) as cm: # KeyError is raised by my implementation's check
            access_nested_map(nested_map, ["a", "b", "c"])
        self.assertEqual(str(cm.exception), "Key 'c' not found in the nested map.") # Removed outer quotes


# To run the tests from the command line:
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

nested_map={"a": 1}, path=("a",)
nested_map={"a": {"b": 2}}, path=("a",)
nested_map={"a": {"b": 2}}, path=("a", "b")




def access_nested_map(nested_map, path):
    """
    Accesses a value in a nested dictionary (map) given a list of keys (path).

    Args:
        nested_map (dict): The nested dictionary to navigate.
        path (list or tuple): A list or tuple of keys representing the path to the desired value.

    Returns:
        Any: The value found at the specified path.

    Raises:
        KeyError: If any key in the path does not exist in the nested map.
    """
    current_level = nested_map
    for key in path:
        # Check if current_level is a dictionary AND if the key exists in it
        if not isinstance(current_level, dict) or key not in current_level:
            # Raise KeyError with a specific message
            raise KeyError(f"Key '{key}' not found in the nested map.")
        current_level = current_level[key]
    return current_level

# --- The Test Class ---
class TestAccessNestedMap(unittest.TestCase):
    """
    Test suite for the access_nested_map function.
    """

    def test_access_nested_map(self):
        """
        Tests that access_nested_map returns the correct value for various
        valid nested map and path combinations.
        """
        # Test Case 1: Simple nested map, single key path
        nested_map_1 = {"a": 1}
        path_1 = ["a"]
        self.assertEqual(access_nested_map(nested_map_1, path_1), 1)

        # Test Case 2: Deeper nested map, multiple key path
        nested_map_2 = {"a": {"b": 2}}
        path_2 = ["a", "b"]
        self.assertEqual(access_nested_map(nested_map_2, path_2), 2)

        # Test Case 3: Even deeper nested map
        nested_map_3 = {"a": {"b": {"c": 3}}}
        path_3 = ["a", "b", "c"]
        self.assertEqual(access_nested_map(nested_map_3, path_3), 3)

        # Test Case 4: Different keys and values
        nested_map_4 = {"data": {"user": {"id": 123, "name": "Alice"}}}
        path_4_id = ["data", "user", "id"]
        path_4_name = ["data", "user", "name"]
        self.assertEqual(access_nested_map(nested_map_4, path_4_id), 123)
        self.assertEqual(access_nested_map(nested_map_4, path_4_name), "Alice")

        # Test Case 5: Path leading to a dictionary (not a leaf value)
        nested_map_5 = {"config": {"settings": {"theme": "dark"}}}
        path_5 = ["config", "settings"]
        self.assertEqual(access_nested_map(nested_map_5, path_5), {"theme": "dark"})

        # Test Case 6: Empty path (should return the original map)
        nested_map_6 = {"x": {"y": 10}}
        path_6_empty = []
        self.assertEqual(access_nested_map(nested_map_6, path_6_empty), nested_map_6)
        # Verify it's the same object for empty path
        self.assertIs(access_nested_map(nested_map_6, path_6_empty), nested_map_6)


    # New test method using parameterized.expand
    @parameterized.expand([
        ({}, ("a",), "Key 'a' not found in the nested map."),
        ({"a": 1}, ("a", "b"), "Key 'b' not found in the nested map."),
        ({"a": {"b": {"c": 3}}}, ("a", "d"), "Key 'd' not found in the nested map."),
        ({"a": {"b": {"c": 3}}}, ("a", "b", "d"), "Key 'd' not found in the nested map."),
        ({"a": {"b": "not_a_dict"}}, ("a", "b", "c"), "Key 'c' not found in the nested map.")
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_message):
        """
        Tests that access_nested_map raises a KeyError with the expected message
        for various invalid paths.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), expected_message)


# To run the tests from the command line:
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
