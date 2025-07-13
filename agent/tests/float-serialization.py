import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from api.serialization import var_to_bytes, bytes_to_var

if __name__ == "__main__":
    # Test float serialization
    test_floats = [
        1.0,
        3.14159,
        2.718281828459045,
        1.7976931348623157e308,
        2.2250738585072014e-308,
        -1.0,
        -3.14159,
        -2.718281828459045,
        -1.7976931348623157e308,
        -2.2250738585072014e-308,
        0.0,
        1.0e-10,
        -1.0e-10,
        1.0e10,
        -1.0e10,
    ]
    for f in test_floats:
        print(f"Testing float: {f}")
        serialized = var_to_bytes(f)
        print(f"Serialized bytes: {serialized}")
        deserialized = bytes_to_var(serialized)
        print(f"Deserialized value: {deserialized}")
        assert f == deserialized, f"Failed for {f}: {deserialized}"
