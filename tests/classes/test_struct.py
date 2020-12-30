"""test_struct.py

Unit tests for the Struct class.
"""


import collections
import unittest
import warnings

from classes.struct import Struct


class TestStruct(unittest.TestCase):
    # Initialization test inputs
    INIT_FULL = collections.OrderedDict({
        "foo": {
            "type":     "<I",
            "default":  1,
            "help":     "Init dict entry is filled as expected",
        },
    })
    INIT_PART = collections.OrderedDict({
        "foo": {
            "type":     "<I",
            "help":     "Init dict entry missing default",
        },
    })
    INIT_INVALID = collections.OrderedDict({
        "foo": {
            "help":     "Init dict entry missing type and default",
        },
    })

    # Type test inputs
    INIT_INT = collections.OrderedDict({
        "foo": {
            "type":     "<I",
            "default":  1,
            "help":     "Example integer field",
        },
    })
    INIT_FLOAT = collections.OrderedDict({
        "foo": {
            "type":     "<f",
            "default":  1.0,
            "help":     "Example float field",
        },
    })
    INIT_CHAR = collections.OrderedDict({
        "foo": {
            "type":     "c",
            "default":  b"c",
            "help":     "Example char field",
        },
    })
    INIT_STRING = collections.OrderedDict({
        "foo": {
            "type":     "8s",
            "default":  b"string",
            "help":     "Example string field",
        },
    })

    # Byte order test inputs
    INIT_BIG_ENDIAN = collections.OrderedDict({
        "foo": {
            "type":     ">Q",
            "default":  1,
            "help":     "Big-endian long long",
        }
    })
    INIT_LITTLE_ENDIAN = collections.OrderedDict({
        "foo": {
            "type":     "<Q",
            "default":  1,
            "help":     "Little-endian long long",
        }
    })

    # Comlex struct test inputs
    INIT_MIXED_SIZE = collections.OrderedDict({
        "foo": {
            "type":     "<B",
            "default":  1,
            "help":     "Mixed dict byte entry",
        },
        "bar": {
            "type":     "<H",
            "default":  2,
            "help":     "Mixed dict short entry",
        },
        "baz": {
            "type":     "<L",
            "default":  3,
            "help":     "Mixed dict long entry",
        },
    })
    INIT_MIXED_TYPE = collections.OrderedDict({
        "foo": {
            "type":     "<I",
            "default":  1,
            "help":     "Mixed dict number entry",
        },
        "bar": {
            "type":     "8s",
            "default":  b"string",
            "help":     "Mixed dict string entry",
        },
    })
    INIT_NESTED = collections.OrderedDict({
        "foo": {
            "type":     Struct({
                            "nested": {
                                "type":     "8s",
                                "default":  b"nested",
                                "help":     "Hello, I'm nested!",
                            },
                        }),
            "help":     "Nested entry",
        },
    })
    INIT_COMPLEX = collections.OrderedDict({
        "foo": {
            "type":     "<I",
            "default":  1,
            "help":     "Mixed dict number entry",
        },
        "bar": {
            "type":     "8s",
            "default":  b"string",
            "help":     "Mixed dict string entry",
        },
        "baz": {
            "type":     Struct({
                            "nested": {
                                "type":     "8s",
                                "default":  b"nested",
                                "help":     "Hello, I'm nested!",
                            },
                        }),
            "help":     "Nested entry",
        },
    })

    ###########################################################################
    # TEST STRUCT INITIALIZATION
    ###########################################################################
    # Test basic initialization
    def test_struct_init_full(self):
        """Test initialization with full init dict."""
        test_struct = Struct(self.INIT_FULL)
        self.assertEqual(test_struct["foo"], self.INIT_FULL["foo"]["default"])

    def test_struct_init_part(self):
        """Test initialization with partial init dict."""
        warnings.simplefilter("ignore")
        test_struct = Struct(self.INIT_PART)
        self.assertEqual(test_struct["foo"], 0)

    def test_struct_init_invalid(self):
        """Test initialization with invalid init dict."""
        with self.assertRaises(SyntaxError):
            _ = Struct(self.INIT_INVALID)

        with self.assertRaises(TypeError):
            _ = Struct([1, 2, 3])
            _ = Struct("invalid")
            _ = Struct(1.0)
            _ = Struct(1)

    def test_struct_init_copy(self):
        """Test copy initialization."""
        test_struct = Struct(self.INIT_FULL)
        copy_struct = Struct(test_struct)

        self.assertEqual(test_struct["foo"], self.INIT_FULL["foo"]["default"])
        self.assertEqual(copy_struct["foo"], self.INIT_FULL["foo"]["default"])

    # Test initialization with different types
    def test_struct_init_int(self):
        """Test initialization with integer type."""
        test_struct = Struct(self.INIT_INT)
        self.assertEqual(test_struct["foo"], self.INIT_INT["foo"]["default"])

    def test_struct_init_float(self):
        """Test initialization with float type."""
        test_struct = Struct(self.INIT_FLOAT)
        self.assertAlmostEqual(test_struct["foo"],
                               self.INIT_FLOAT["foo"]["default"])

    def test_struct_init_char(self):
        """Test initialization with char type."""
        test_struct = Struct(self.INIT_CHAR)
        self.assertEqual(test_struct["foo"], self.INIT_CHAR["foo"]["default"])

    def test_struct_init_string(self):
        """Test initialization with string type."""
        test_struct = Struct(self.INIT_STRING)
        self.assertEqual(test_struct["foo"],
                         self.INIT_STRING["foo"]["default"])

    def test_struct_init_byte_order(self):
        """Test initialiation with different byte orders."""
        be_struct = Struct(self.INIT_BIG_ENDIAN)
        le_struct = Struct(self.INIT_LITTLE_ENDIAN)

        self.assertEqual(be_struct["foo"],
                         self.INIT_BIG_ENDIAN["foo"]["default"])
        self.assertEqual(le_struct["foo"],
                         self.INIT_LITTLE_ENDIAN["foo"]["default"])

    # Test initialization with more complex structs
    def test_struct_init_mixed_size(self):
        """Test initialization with mixed field sizes."""
        test_struct = Struct(self.INIT_MIXED_SIZE)
        self.assertEqual(test_struct["foo"],
                         self.INIT_MIXED_SIZE["foo"]["default"])
        self.assertEqual(test_struct["bar"],
                         self.INIT_MIXED_SIZE["bar"]["default"])
        self.assertEqual(test_struct["baz"],
                         self.INIT_MIXED_SIZE["baz"]["default"])

    def test_struct_init_mixed_type(self):
        """Test initialization with mixed field types."""
        test_struct = Struct(self.INIT_MIXED_TYPE)
        self.assertEqual(test_struct["foo"],
                         self.INIT_MIXED_TYPE["foo"]["default"])
        self.assertEqual(test_struct["bar"],
                         self.INIT_MIXED_TYPE["bar"]["default"])

    def test_struct_init_nested(self):
        """Test initialization with nested fields."""
        test_struct = Struct(self.INIT_NESTED)
        self.assertEqual(test_struct["foo"]["nested"],
                         self.INIT_NESTED["foo"]["type"]["nested"])
        self.assertTrue(isinstance(test_struct["foo"], Struct))

    def test_struct_init_complex(self):
        """Test initialization with a complex init dict."""
        test_struct = Struct(self.INIT_COMPLEX)
        self.assertEqual(test_struct["foo"],
                         self.INIT_COMPLEX["foo"]["default"])
        self.assertEqual(test_struct["bar"],
                         self.INIT_COMPLEX["bar"]["default"])
        self.assertEqual(test_struct["baz"]["nested"],
                         self.INIT_COMPLEX["baz"]["type"]["nested"])
        self.assertTrue(isinstance(test_struct["baz"], Struct))

    ###########################################################################
    # TEST DICT FUNCTIONALITY
    ###########################################################################
    def test_struct_set_get(self):
        """Test that we can get and set Struct fields."""
        test_struct = Struct(self.INIT_COMPLEX)
        self.assertEqual(test_struct["foo"],
                         self.INIT_COMPLEX["foo"]["default"])
        self.assertEqual(test_struct["bar"],
                         self.INIT_COMPLEX["bar"]["default"])
        self.assertEqual(test_struct["baz"]["nested"],
                         self.INIT_COMPLEX["baz"]["type"]["nested"])

        test_struct["foo"] = 2
        test_struct["bar"] = b"bar"
        test_struct["baz"]["nested"] = b"baz"

        self.assertEqual(test_struct["foo"], 2)
        self.assertEqual(test_struct["bar"], b"bar")
        self.assertEqual(test_struct["baz"]["nested"], b"baz")

    def test_struct_contains(self):
        """Test that Struct __contains__ method is working."""
        test_struct = Struct(self.INIT_COMPLEX)
        self.assertTrue("foo" in test_struct)
        self.assertTrue("bar" in test_struct)
        self.assertTrue("baz" in test_struct)
        self.assertFalse("invalid" in test_struct)

    def test_struct_length(self):
        """Test that Struct length can be determined."""
        test_struct = Struct(self.INIT_COMPLEX)
        self.assertEqual(len(test_struct), 3)

    def test_struct_isolation(self):
        """Test that modifying a struct does not modify the
        initialization object.
        """
        test_struct = Struct(self.INIT_COMPLEX)
        copy_struct = Struct(test_struct)

        test_struct["foo"] = 2
        test_struct["bar"] = b"bar"
        test_struct["baz"]["nested"] = b"baz"

        copy_struct["foo"] = 3
        copy_struct["bar"] = b"BAR"
        copy_struct["baz"]["nested"] = b"BAZ"

        # Make sure the initialization object is intact
        self.assertEqual(self.INIT_COMPLEX["foo"]["default"], 1)
        self.assertEqual(self.INIT_COMPLEX["bar"]["default"], b"string")
        self.assertEqual(self.INIT_COMPLEX["baz"]["type"]["nested"], b"nested")

        # Make sure none of the Structs share the same value, and that they
        # don't match the initialization object either
        self.assertNotEqual(self.INIT_COMPLEX["foo"]["default"],
                            test_struct["foo"])
        self.assertNotEqual(self.INIT_COMPLEX["bar"]["default"],
                            test_struct["bar"])
        self.assertNotEqual(self.INIT_COMPLEX["baz"]["type"]["nested"],
                            test_struct["baz"]["nested"])

        self.assertNotEqual(self.INIT_COMPLEX["foo"]["default"],
                            copy_struct["foo"])
        self.assertNotEqual(self.INIT_COMPLEX["bar"]["default"],
                            copy_struct["bar"])
        self.assertNotEqual(self.INIT_COMPLEX["baz"]["type"]["nested"],
                            copy_struct["baz"]["nested"])

        self.assertNotEqual(test_struct["foo"], copy_struct["foo"])
        self.assertNotEqual(test_struct["bar"], copy_struct["bar"])
        self.assertNotEqual(test_struct["baz"]["nested"],
                            copy_struct["baz"]["nested"])

    def test_struct_field_order(self):
        """Test that field order is preserved on intialization."""
        ordered = ["foo", "bar", "baz"]

        test_struct = Struct(self.INIT_COMPLEX)
        for i, field in enumerate(test_struct):
            self.assertEqual(field, ordered[i])

        copy_struct = Struct(test_struct)
        for i, field in enumerate(copy_struct):
            self.assertEqual(field, ordered[i])

    def test_struct_immutability(self):
        """Test that a Struct is immutable once created."""
        test_struct = Struct(self.INIT_COMPLEX)

        with self.assertRaises(KeyError):
            test_struct["invalid"] = b"invalid"
        with self.assertRaises(KeyError):
            _ = test_struct["invalid"]
        with self.assertRaises(NotImplementedError):
            del test_struct["foo"]

    def test_struct_pickle(self):
        """Test that Struct pickling works as expected."""
        i_struct = Struct(self.INIT_INT)
        f_struct = Struct(self.INIT_FLOAT)
        c_struct = Struct(self.INIT_CHAR)
        s_struct = Struct(self.INIT_STRING)

        ms_struct = Struct(self.INIT_MIXED_SIZE)
        mt_struct = Struct(self.INIT_MIXED_TYPE)
        cp_struct = Struct(self.INIT_COMPLEX)

        self.assertEqual(i_struct.pickle(), b"\x01\x00\x00\x00")
        self.assertEqual(f_struct.pickle(), b"\x00\x00\x80\x3F")
        self.assertEqual(c_struct.pickle(), b"c")
        self.assertEqual(s_struct.pickle(), b"string\x00\x00")

        self.assertEqual(ms_struct.pickle(), b"\x01\x02\x00\x03\x00\x00\x00")
        self.assertEqual(mt_struct.pickle(), b"\x01\x00\x00\x00string\x00\x00")
        self.assertEqual(cp_struct.pickle(),
                         b"\x01\x00\x00\x00string\x00\x00nested\x00\x00")

    def test_struct_calcsize(self):
        """Test that calcsize returns the correct Struct size."""
        i_struct = Struct(self.INIT_INT)
        f_struct = Struct(self.INIT_FLOAT)
        c_struct = Struct(self.INIT_CHAR)
        s_struct = Struct(self.INIT_STRING)

        ms_struct = Struct(self.INIT_MIXED_SIZE)
        mt_struct = Struct(self.INIT_MIXED_TYPE)
        cp_struct = Struct(self.INIT_COMPLEX)

        self.assertEqual(i_struct.calcsize(), 4)
        self.assertEqual(f_struct.calcsize(), 4)
        self.assertEqual(c_struct.calcsize(), 1)
        self.assertEqual(s_struct.calcsize(), 8)

        self.assertEqual(ms_struct.calcsize(), 7)
        self.assertEqual(mt_struct.calcsize(), 12)
        self.assertEqual(cp_struct.calcsize(), 20)

    def test_struct_string(self):
        """Test automatic string manipulation works as expected."""
        test_struct = Struct(self.INIT_STRING)

        # Test string padding
        test_struct["foo"] = b"small"
        self.assertEqual(test_struct["foo"], b"small")
        self.assertEqual(test_struct.pickle(), b"small\x00\x00\x00")

        # Test string truncation
        test_struct["foo"] = b"much longer string"
        self.assertEqual(test_struct["foo"], b"much lon")
        self.assertEqual(test_struct.pickle(), b"much lon")

    def test_struct_helpstring(self):
        """Test that helpstring was set up as expected."""
        test_struct = Struct(self.INIT_COMPLEX, structname="ComplexStruct")
        fields = ["foo", "bar", "baz"]

        helplines = test_struct.helpstring.split("\n")
        self.assertTrue(helplines[0].startswith("ComplexStruct"))

        for i, field in enumerate(fields):
            line = helplines[i + 1].lstrip().rstrip()
            self.assertTrue(line.startswith(field))
            self.assertTrue(line.endswith(self.INIT_COMPLEX[field]["help"]))
