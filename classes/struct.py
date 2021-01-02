"""struct.py

Generic structure used for any ordered file headers, footers, and data.
A Struct is a stripped-down subclass of 'dict', and the term 'field' is
the same as a dictionary 'key'.

A Struct is initialized with a dict-like object that is made up of one
or more fields that each have details about them. A Struct can also be
initialized with another Struct which will make a copy of the original
into the new Struct. Any dict-list object used for initialization must
have the following structure:

{
    "field": {
        "type":     "<struct format string (e.g. '<I', '4s')>",
        "default":  "<optional default value (type must match)>",
        "help":     "<optional help string>",
    },
}

Features:
    - Structs can be nested (a field in a Struct can be Struct type)
    - Throws exceptions and warnings if not configured as expected
    - Field order is maintained (similar to collections.OrderedDict)
    - Struct is immutable once initialized
        - Cannot add new fields during runtime
        - Cannod delete fields during runtime
    - 'pickle' method pickles the Struct to a bytes array
    - 'calcsize' method calculates the Struct size in bytes
    - Fields that are strings are automatically truncated or padded
        when updated in a Struct
    - Fields that are string have any trailing null characters stripped
        when getting field values in a Struct
    - Automatically sets value of a field to zero or empty string if
        default is not set
    - Provides a help string that outlines the required fields and
        information about each field (if set up)

Notes:
    - All string values for fields must be a bytes string (i.e. b"")
    - All string values must have a known, fixed maximum length
"""


import collections
import copy
import re
import struct
import textwrap
import warnings


# Set default values for different types.
_DEFAULT_NUMBER = 0
_DEFAULT_STRING = b""

# Regular expressions for determining simple struct types.
# See documentation for 'struct' library for valid types. Note that some types
# (like bool, pad, and some floats) are not supported for arbitrary reasons.
_RE_STRUCT_NUMBER_RAW = r"^[@=<>!]?[\?bBdfhHiIlLnNqQ]$"
_RE_STRUCT_STRING_RAW = r"^[@=<>!]?(\d)*[cs]$"

_RE_STRUCT_NUMBER = re.compile(_RE_STRUCT_NUMBER_RAW)
_RE_STRUCT_STRING = re.compile(_RE_STRUCT_STRING_RAW)


class Struct(dict):
    def __init__(self, fields, structname=None):
        # Type validations and init parameter sanitation.
        if not isinstance(fields, dict):
            raise TypeError("Must initialized Struct with a dict-like object")

        if structname is None:
            structname = self.__class__.__name__

        # Check for initialization special cases
        if type(fields) is Struct:
            # One special case is initializing a Struct with another struct.
            # The behaviour is to copy the initialization struct's content,
            # but modify the struct name if required. The copy initialization
            # performs all object structure setup and store validation.
            self.__copy_init(fields, structname)
            return

        # Parameter validation and sanitation is complete, start setting up
        # the object structure and validate the internal store.
        self._store = collections.OrderedDict(copy.deepcopy(fields))
        self._structname = structname
        self.helpstring = f"{self._structname} details\n"

        self.__update_and_validate_store()
        self.__update_helpstring()

    def __copy_init(self, original, structname):
        """Initialize the Struct by copying another existing Struct
        into this new Struct object. The new Struct can be given a new
        structname.

        Initialize the Struct by making a copy of another Struct.

        Parameters:
            original    Original Struct object to copy
            structname  New structname for the new Struct

        Return:
            None
        """
        self._structname = structname
        self._store = copy.deepcopy(original._store)
        self.helpstring = original.helpstring.replace(original._structname,
                                                      self._structname)

    def __update_and_validate_store(self):
        """Update and validate the internal Struct store. Validation
        ensures all fields in the store have a supported type. Update
        sets that internal value of that field that can be modified
        later.
        """
        for field in self._store:
            # Create a detailed field name string for better exception and
            # warning messages.
            fieldname = f"{self._structname}.{field}"

            # Validate the field type. Ensure that it exists, is the expected
            # type, and is a valid struct format string.
            ftype = self._store[field].get("type")

            if ftype is None:
                raise SyntaxError(f"{fieldname} missing type")

            if not (isinstance(ftype, Struct) or isinstance(ftype, str)):
                raise TypeError(f"{fieldname} type must be instance of string "
                                + f" or Struct - '{type(ftype)}' type invalid")

            if isinstance(ftype, str) \
                    and _RE_STRUCT_NUMBER.match(ftype) is None \
                    and _RE_STRUCT_STRING.match(ftype) is None:
                raise SyntaxError(f"{fieldname} type '{ftype}' is invalid")

            # If the type is a struct, just store the struct as the value
            # and continue. We don't need to worry about automatically
            # packing this until we need to pickle this Struct.
            if isinstance(ftype, Struct):
                self._store[field]["value"] = ftype
                return
            # NOTE: from here on out, the only possible type of ftype is 'str'

            # Warn users is there is no default values and populate the
            # value field.
            fvalue = self._store[field].get("default")

            if fvalue is None:
                if _RE_STRUCT_NUMBER.match(ftype):
                    fvalue = _DEFAULT_NUMBER
                    warnings.warn(f"{fieldname} missing default value - "
                                  + f"setting value to '{fvalue}'")
                else:
                    fvalue = _DEFAULT_STRING
                    warnings.warn(f"{fieldname} missing default value - "
                                  + f"setting value to '{fvalue}'")

            self._store[field]["value"] = struct.pack(ftype, fvalue)

            # Warn users if there is no help information for the field.
            fhelp = self._store[field].get("help", "")

            if fhelp == "":
                warnings.warn(f"{fieldname} missing optional help text")

    def __update_helpstring(self):
        """Update the help string by reading each field's help info and
        append it to the currently existing help string.
        """
        helpwidth = max(len(field) for field in self._store)

        for field in self._store:
            obj = self._store[field]

            fhelp = obj.get("help", "[No details]")
            self.helpstring += f"  {field:<{helpwidth}} -- {fhelp}\n"

            if isinstance(obj["type"], Struct):
                self.helpstring += textwrap.indent(obj["type"].helpstring,
                                                   "    ")

    def __contains__(self, item):
        """Pass all __contains__ calls to the internal store."""
        return self._store.__contains__(item)

    def __delitem__(self, key):
        """Prevent any fields from being deleted - Struct is
        immutable after initialization.
        """
        raise NotImplementedError("Cannot delete fields from "
                                  + f"{self._structname}")

    def __getitem__(self, key):
        """Custom __getitem__ implementation that automatically unpacks
        values when they are gotten from the Struct.

        Parameters:
            key     Field to unpack

        Return:
            The unpacked field.

        Raises:
            KeyError
        """
        # Automatically unpack an item when accessed.
        if key not in self._store:
            raise KeyError(f"Struct '{self._structname}'"
                           + f" - cannot find '{key}' field"
                           + " - does not exist")

        fmt = self._store[key]["type"]
        val = self._store[key]["value"]

        if not isinstance(fmt, str):
            # The field's type is Struct - no need to unpack this value, we can
            # just return the whole Struct.
            return val
        elif _RE_STRUCT_STRING.match(fmt) is not None:
            # Unpack any strings and remove padding.
            return b"".join(struct.unpack(fmt, val)).rstrip(b"\x00")
        else:
            # Treat everything else as a single number.
            return struct.unpack(fmt, val)[0]

    def __iter__(self):
        """Pass all __iter__ calls to the internal store."""
        return self._store.__iter__()

    def __len__(self):
        """Pass all __len__ calls to the internal store."""
        return self._store.__len__()

    def __missing__(self, key):
        # Do not implement this because __getitem__ already handles fields
        # that are not in the store.
        raise NotImplementedError()

    def __next__(self):
        """Pass all __next__ calls to the internal store."""
        return self._store.__next__()

    def __reversed__(self):
        """Prevent any fields from being reversed. The Struct fields
        don't need to be accessed in reverse.
        """
        # Structs shouldn't be reversed.
        raise NotImplementedError(f"Cannot reverse Struct {self._structname}")

    def __setitem__(self, key, value):
        """Custom __setitem__ implementation that automatically packs
        values when they are updated. This also prevents new fields
        from being added to the Struct. This will automatically pad or
        truncate any string fields.

        Parameters:
            key     Field to pack and update
            value   Updated field's value

        Return:
            None

        Raises:
            KeyError
        """
        # Automatically pack an item when set.
        if key not in self._store:
            raise KeyError(f"Struct '{self._structname}'"
                           + f" - cannot set '{key}' field"
                           + " - does not exist")

        fmt = self._store[key]["type"]

        if isinstance(fmt, Struct):
            if isinstance(value, Struct):
                self._store[key] = value
            else:
                raise TypeError(f"'{self._structname}.{key}' is type 'Struct'")
        else:
            self._store[key]["value"] = struct.pack(fmt, value)

    def calcsize(self):
        """Calculate the Struct size in bytes.

        Parameters:
            None

        Return:
            Size of the Struct in bytes.
        """
        size = 0
        for field in self._store:
            ftype = self._store[field]["type"]

            if isinstance(ftype, Struct):
                size += ftype.calcsize()
            else:
                size += struct.calcsize(ftype)

        return size

    def pickle(self):
        """Pickle the Struct object into a byte array.

        Parameters:
            None

        Return:
            The Struct object pickled as a byte array.
        """
        pickled = b""
        for field in self._store:
            fvalue = self._store[field]["value"]

            if isinstance(fvalue, Struct):
                pickled += fvalue.pickle()
            else:
                pickled += fvalue

        return pickled
