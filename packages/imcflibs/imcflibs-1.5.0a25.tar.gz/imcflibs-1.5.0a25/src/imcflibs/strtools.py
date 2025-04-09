"""String related helper functions."""

import re

from ._jython_compat import file_types


# this is taken from numpy's iotools:
def _is_string_like(obj):
    """Check whether obj behaves like a string.

    Using this way of checking for a string-like object is more robust when
    dealing with stuff that can behave like a 'str' but is not strictly an
    instance of it (or a subclass thereof). So it's more generic than using
    isinstance(obj, str).

    Parameters
    ----------
    obj : any
        The object to be checked for being string-like.

    Example
    -------
    >>> _is_string_like('foo')
    True
    >>> _is_string_like(123)
    False
    """
    try:
        obj + ""
    except (TypeError, ValueError):
        return False
    return True


def filename(name):
    """Get the filename from either a filehandle or a string.

    This is a convenience function to retrieve the filename as a string given
    either an open filehandle or just a plain str containing the name.

    When running in Jython the function will also convert `java.io.File` objects
    to `str`. NOTE: this also works if the Java object is a directory, not an
    actual file.

    Parameters
    ----------
    name : str or filehandle or java.io.File
        The object to retrieve the filename from.

    Returns
    -------
    name : str

    Example
    -------
    >>> filename('test_file_name')
    'test_file_name'

    >>> import os.path
    >>> fname = filename(open(__file__, 'r'))
    >>> os.path.basename(fname) in ['strtools.py', 'strtools.pyc']
    True
    """
    try:
        if isinstance(name, java.io.File):
            return str(name)
    except:
        # we silently ignore this case and continue with checks below as most
        # likely we are not running under Jython
        pass

    if isinstance(name, file_types):
        return name.name
    elif _is_string_like(name):
        return name
    else:
        raise TypeError


def flatten(lst):
    """Make a single string from a list of strings.

    Parameters
    ----------
    lst : list(str)
        The list of strings to be flattened.

    Returns
    -------
    flat : str

    Example
    -------
    >>> flatten(('foo', 'bar'))
    'foobar'
    """
    flat = ""
    for line in lst:
        flat += line
    return flat


def strip_prefix(string, prefix):
    """Remove a given prefix from a string.

    Parameters
    ----------
    string : str
        The original string from which the prefix should be removed.
    prefix : str
        The prefix to be removed.

    Returns
    -------
    str
        The original string without the given prefix. In case the original
        string doesn't start with the prefix, it is returned unchanged.
    """
    if string.startswith(prefix):
        string = string[len(prefix) :]
    return string


def sort_alphanumerically(data):
    """Sort a list alphanumerically.

    Parameters
    ----------
    data : list(str)
        List of strings to be sorted.

    Returns
    -------
    list

    Examples
    --------
    >>> sorted([ "foo-1", "foo-2", "foo-10" ])
    ["foo-1", "foo-10", "foo-2"]

    >>> sort_alphanumerically([ "foo-1", "foo-2", "foo-10" ])
    ["foo-1", "foo-2", "foo-10"]
    """

    def convert(text):
        return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key):
        return [convert(c) for c in re.split("([0-9]+)", key)]

    return sorted(data, key=alphanum_key)


def pad_number(index, pad_length=2):
    """Pad a number with leading zeros to a specified length.

    Parameters
    ----------
    index : int or str
        The number to be padded
    pad_length : int, optional
        The total length of the resulting string after padding, by default 2

    Returns
    -------
    str
        The padded number as a string

    Examples
    --------
    >>> pad_number(7)
    '07'
    >>> pad_number(42, 4)
    '0042'
    """
    return str(index).zfill(pad_length)
