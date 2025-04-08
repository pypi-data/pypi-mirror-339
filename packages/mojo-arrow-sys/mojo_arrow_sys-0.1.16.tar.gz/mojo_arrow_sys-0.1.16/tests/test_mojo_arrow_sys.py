import unittest
import pytest
import mojo_arrow_sys
from typing import Any
import ctypes
import pyarrow as pa


class TestMojoArrowSys(unittest.TestCase):
    def test_arrow_stream_attribute_missing(self):
        # Test that proper error is raised when __arrow_c_stream__ is missing
        with pytest.raises(TypeError):
            mojo_arrow_sys.arrow_stream(object())

    def test_arrow_stream(self):
        # Create a simple PyArrow table for testing
        data = {
            "id": [1, 2, 3, 4, 5],
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "value": [10.1, 20.2, 30.3, 40.4, 50.5],
        }
        table = pa.Table.from_pydict(data)

        try:
            # Use the real PyArrow table which implements __arrow_c_stream__
            result = mojo_arrow_sys.arrow_stream(table)
            # We just test that it returns something and doesn't crash
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"arrow_stream raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
