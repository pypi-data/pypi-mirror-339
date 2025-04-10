#!/usr/bin/env python3

###############################################################################
# 
# Copyright (c) 2025, Anders Andersen, UiT The Arctic University of
# Norway. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
# - Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# 
# - Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
# 
# - Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# 
###############################################################################

R"""A Python module for generating Python module documentation

The `pypimdoc` module generates documentation for a Python module
based on a README template file and the documentation text strings
from the Python source code of the module.  The README template file
is a Markdown text document with the additions of what we call *module
documentation macros*, or just *MD-macros* for short.  These macros
are on separate lines inside HTML comments:

```
<!-- doc(PyPiMDoc.process_template, hlevel=2) -->
```

In the example above, the MD-macro line will be replaced by the
documentation string of the `process_template` method of the
`PyPiMDoc` class with a level 2 heading. If the module is used in
inline-mode (and not the default HTML comment block-mode), the
MD-macros are placed inline in the markdown template file and not
inside HTML comments:

```python
doc(PyPiMDoc.process_template, hlevel=2)
```

Other available MD-macros includes the heading macro `h` (to create at
heading), the table of content macro `toc` (to create table of
content), the Python code evaluation macro `eval` (to insert the
result of the evaluated Python code), the shell command macro `cmd`
(to insert the result of the executed shell command), and the help
text macro `help` (to insert the result of the help commad `-h` when
the module is used as a console script).

The `pypimdoc` module also provides an MD-macro to loop over a list:

```
<!-- for_in(x, [_ismethod, _get_doc], "doc(x, hlevel = 3)") -->
```

The example above has the same effect as inserting the following lines
in the README template:

```
<!-- doc(_ismethod, hlevel = 3) -->
<!-- doc(_get_doc, hlevel = 3) -->
```

A few MD-macros are also available as multi-line HTML comment
blocks. The `for_in` MD-macro is typically more often used as a
multi-line HTML comment block:

```
<!-- for x in [_ismethod, _get_doc]:
  doc(x, hlevel = 3)
-->
```

If the `pypimdoc` module is used in inline-mode, the equivalent code
of the example above will be:

```python
for x in [_ismethod, _get_doc]:
  doc(x, hlevel = 3)
end_for
```

Currently, the MD-macros `for_in` and `code` can be used as
multi-line HTML comment blocks (or inline-mode blocks).  This is an
example of such a multi-line HTML comment block for `code`:

```
<!-- code:

def rm_md(name: str) -> str:
    return name.split(".")[-1][4:]

def md_mds(title: str) -> str:
    return title.replace("Method", "MD-macro")

-->
```

The inline-mode version of the code block example above will be as follows:

```python
code:

def rm_md(name: str) -> str:
    return name.split(".")[-1][4:]

def md_mds(title: str) -> str:
    return title.replace("Method", "MD-macro")

end_code
```

The MD-macro `code` and the example of code blocks above populates the
name space where the MD-macros are executed. The consequence is that
the functions (and variables) defined in such code blocks can be used
in the arguments of MD-macros. For example, based on the code block
above, the documentation of the MD-macro `doc` can be generated using
the MD-macro `doc` itself with the two help functions defined in the
code blocks above:

```
<!-- doc(PyPiMDoc._md_doc, hlevel = 2, name_transform = rm_md, title_transform = md_mds) -->
```

The `name_transform` argument `rm_md` will change the name of the
method from `"PyPiMDoc._md_doc"` to `"doc"`, and the `title_transform`
argument `md_mds` will change the the title `"Method doc"` to
`"MD-macro doc"` (see the implementation of these help functions in
the code blocks above).

The `pypimdoc` module also provides some predefined help functions
available in the name space where the MD-macros are executed. These
predefined help fuctions can also be used in the arguments of
MD-macros. For example, to create a level-two header with the title
from the title part (the first line) of the documentation string of
`_is_method`, you can use the help function `mdoc_title` in the
arguments of the MD-macro `h`:

```
<!-- h(mdoc_title(_is_method), hlevel = 2) -->
```

The `mdoc_title` returns the title part (the first line) of the
documentation string of the object provided as the argument; in this
case the function `_is_method`. To create a level-one header with the
title string of the module (the first line of the documentation string
of the module), you use the MD-macro `h` in the following way:

```
<!-- h(mdoc_title(), hlevel = 1) -->
```

In addition, the two MD-macros `eval` and `cmd` are also made
available in the name space where the MD-macros are executed and can
be used in the argument part of other MD-macros.

To produce the the markdown documentation of a module where the
documentation strings are written in markdown, you can use the console
script `pypimdoc`:

```bash
pypimdoc -t README.template -o README.md mymodule.py
```

The command above generates the markdown documentation of the module
`mymodule` in the `README.md` file based on source code of the module
in the file `mymodule.py` and the README template file
`README.template`. If the `mymodule` provides one class `MyClass`, the
following could be a complete example of the README template file:

```
<!-- doc(hlevel = 1) -->

<!-- doc(MyClass, hlevel = 1, complete = True) -->
```

The first `doc` MD-macro creates a level-one heading with the title
(first line) of the module documentation string followed by the body
of module documentation string.  The second `doc` MD-macro creates
the complete documentation of the class `MyClass` with the constructor
and all public methods (methods with names not starting with `_`). A
level-one heading is added to the start where the title is the title
(first line) of the documentation string of the class `MyClass`.  The
documentation for each public method is from the documentation string
of each of these methods, and a sub-heading is added for each of these
methods.

"""


#
# Some useful values
#

# Current version of module
version = "1.12"

# The produced-by text
produced_by = "This documentation is generate using the `pypimdoc` module"

# The where-to-find text
where_to_find = "Available from [PyPi](https://pypi.org/project/pypimdoc/)"

#
# Import Python modules used
#

# Import standard modules
import sys, re
import urllib.parse
import importlib.util
from pathlib import Path
from io import TextIOBase, StringIO
from inspect import signature, getdoc, isclass, ismethod, isfunction, ismodule
from collections.abc import Callable

# Use subprocess to perform the command line operations
import subprocess

# Import some `pygments` stuff
#from pygments import highlight
#from pygments.lexers.python import PythonLexer
#from pygments.util import ClassNotFound
#from pygments.styles import get_style_by_name
#from pygments.formatters import HtmlFormatter, LatexFormatter


#
# Regular expressions used by the module
#

# Blocks
_block_begin = r"<!--"
_block_end = r"-->"
_block_end_compiled = re.compile(rf"^\s*{_block_end}\s*$")

# Match `pypimdoc` MD-macros in README templates, like the line
# `doc(PyPiMDoc, hlevel = 1, complete = True)`
_md_macro_re = r"(?P<macro>\w+)\((?P<args>.*)\)"
_md_macro = {
    "inline": re.compile(rf"^\s*{_md_macro_re}\s*$"),
    "block": re.compile(
        rf"^{_block_begin}\s*{_md_macro_re}\s*{_block_end}\s*$")
}
_md_name_arg = re.compile(r"[\w \t='\"]*name=(?P<name>['\"]\w+['\"]).*")

# Loop
_md_loop_re = r"for\s+(?P<var>\w+)\s+in\s+(?P<listexpr>.+)\s*:"
_md_loop_inline_end = r"end_for"
_md_forloop = {
    "inline": {
        "begin": re.compile(rf"^\s*{_md_loop_re}\s*$"),
        "end": re.compile(rf"^\s*{_md_loop_inline_end}\s*$")
    },
    "block": {
        "begin": re.compile(rf"^{_block_begin}\s*{_md_loop_re}\s*$"),
        "end": _block_end_compiled
    }
}

# Code block
_md_code_re = r"code\s*:"
_md_code_inline_end = r"end_code"
_md_code = {
    "inline": {
        "begin": re.compile(rf"^\s*{_md_code_re}\s*$"),
        "end": re.compile(rf"^\s*{_md_code_inline_end}\s*$")
    },
    "block": {
        "begin": re.compile(rf"^{_block_begin}\s*{_md_code_re}\s*$"),
        "end": _block_end_compiled
    }
}

# Match <class>.<method>, like `PyPiMDoc.process_template`
_cmnames = re.compile(r"(?P<class>\w+)\.(?P<method>\w+)")

# Match module file name <name>.py, like `pypimdoc.py`
_pysrcname = re.compile(r"^(?P<name>\w+)\.(?P<ext>py)$")

# Match a header (empty line followed by title ending with colon
# followed by empty line)
_margsheader = re.compile(r'\n\s*\n([\w /]+:)\n\s*\n')

# In-line code starts and ends with lines starting with three single
# back-quotes
_inline_code = re.compile(r'^```')

# Match a markdown heading
_md_heading = re.compile(r"^(?P<level>#+)\s*(?P<title>.+)$")


#
# Help functions
#


# Matches for the `help2md` function (sol = start of line)
import re
_sol_lc = re.compile(r"^[a-z].*")
_sol_usage = re.compile(r"^Usage:")
_sol_ws_rest = re.compile(r"^ +.*$")
_sol_empty = re.compile(r"^$")
_sol_descr = re.compile(r"^[a-zA-Z_0-9][a-zA-Z_0-9 ]+.*[^:]$")
_sol_args = re.compile(r"^[OP][a-zA-Z_0-9 ]+:$")
_py_fn = re.compile(r"[a-z]+[.]py")
_single_quoted = re.compile(r"'[^']+'")
_sol_ten_ws = re.compile(r"^          ")
_cont_line = re.compile(r"` \| ")
_sol_two_ws = re.compile(r"^  ")

def help2md(help_msg: str) -> str:
    R"""Convert a help message to markdown text

    Convert a command help message (the output from a command when the
    `-h` flag is given) to a valid and well-formated markdown text.
    This function is tailored for the help messages produced by Python
    programs using the `argparse` module.

    Arguments/return value:

    `help_msg`: The help message to convert

    `returns`: The markdown text

    """

    # Initialize help variables
    usage: bool = False
    descr: bool = False
    options: bool = False
    prev: str = ""
    nr: int = 0
    md_txt: str = ""

    # Parse each line of `help_msg`
    for line in help_msg.splitlines():

        # Count lines
        nr += 1

        # Use `match` if matching the beginning of line, and `search`
        # to match inside line

        # Uppercase first character in paragraphs
        # /^[a-z]/ 
        if _sol_lc.match(line):
            line = line[0].upper() + line[1:]

        # Initialize usage section (and optional first usage line)
        # /^Usage:/
        if _sol_usage.match(line):
            usage = True
            line = re.sub(r"^Usage: +", "\n```bash\n", line)
            line = re.sub(r"^Usage:$", "\n```bash", line)
            utxt = "\n**Usage:**\n" + line
            continue

        # Format usage code
        # usage && /^ +.*$/
        if usage and _sol_ws_rest.match(line):
            line = re.sub(r"^ +", " ", line)
            utxt += line
            continue

        # Close usage code if after usage
        # usage && /^$/
        if usage and _sol_empty.match(line):
            usage = False
            descr = True
            utxt += "\n```"
            continue

        # Close options
        # options && /^$/
        if options and _sol_empty.match(line):
            options = False

        # Description? (if so, first text after usage)
        # descr && /^[a-zA-Z_0-9][a-zA-Z_0-9 ]+.*[^:]$/
        if descr and _sol_descr.match(line):
            descr = False
            prev = "*" + line + "*"
            line = utxt

        # Initialize options/positional-arguments section
        # !usage && /^[OP][a-zA-Z_0-9 ]+:$/
        if (not usage) and _sol_args.match(line):
            if descr: descr = False
            options = True
            line = "**" + line + "**\n\nName | Description\n---- | -----------"

        # Remove .py from command
        # /[a-z]+[.]py/
        if _py_fn.search(line):
            line = re.sub(r"[.]py", "", line)

        # Substitute quote with backquote
        # /'[^']+'/
        if _single_quoted.search(line):
            line = line.replace("'", "`", 2)

        # Join continuation lines with previous line
        # /^          /
        if _sol_ten_ws.match(line):

            # options && (prev !~ /` \| /)
            if options and not _cont_line.search(prev):
                line = re.sub(r"^ *", "` | ", line)
            else:
                line = re.sub(r"^ *", " ", line)
            prev += line
            continue

        # Format arguments/options table
        # !usage && /^  /
        if not usage and _sol_two_ws.match(line):
            line = re.sub(r"^  +", "`", line)
            line = re.sub(r"  +", "` | ", line)

        # Initialize buffered line
        # NR == 1
        if nr == 1:
            prev = line

        # Print line (one line buffered)
        # NR > 1 
        else:
            md_txt += prev + "\n"
            prev = line

    # END
    md_txt += prev + "\n"
    return md_txt


# A few one-liners
_title = lambda obj: obj[0]
_body = lambda obj: obj[1]
_combined = lambda obj: f"{obj[0]}\n\n{obj[1]}"


def _get_nested_attr(ns, attr_str: str) -> object:
    R"""Get a nested attribute

    Return the named nested attribute `attr_str` from the namespace
    `ns`.  For example, if `attr_str` is `"a.b"`, return the attribute
    `b` of `a`.

    Arguments/return value:

    `ns`: Name space to find nested attribute in

    `attr_str`: Nested attributed as a string using dot notation

    `returns`: The attribute named in `attr_str`

    """
    attr = ns
    nested_attr = attr_str.split(".")
    for a in nested_attr:
        attr = getattr(attr, a)
    return attr


def _mkid(txt: str, idlist: list, max_length: int = 20) -> str:
    R"""Make a valid id or reference

    Create a valid and unique HTML id/reference from the text string
    `txt`.  The text string is tyically a title or a Python object
    name.

    Arguments/return value:

    `txt`: The text to be transformed to an id

    `idlist`: A list of used ids

    `max_length`: The maximum length of the id

    `returns`: The new unique id

    """

    # Create a quoted (safe) id and start with that one as the new id
    qid = urllib.parse.quote_plus(txt[:max_length])
    nid = qid
    lqid = len(qid)

    # Continue until we have a unique id
    i = 1
    while nid in idlist:

        # Count and create a numer to append (to ensure uniqueness) 
        num = str(i)

        # Ensure that the id is not longer than `max_length`
        newl = lqid + len(num)
        if newl > max_length:
            rl = newl - max_length
            nid = qid[:-rl] + num
        else:
            nid = qid + num

        # Increase counter
        i += 1

    # Add new unique id to id list and return the new id
    idlist.append(nid)
    return nid


def _ismethod(attr: object) -> bool:
    R"""A more relaxed implementation of `ismethod`

    This version of `ismethod` will also return `True` if it is not in
    an instance of the class of the method. The trick (that might give
    false positives) is to check that the function's long name
    (`__qualname__`) is a nested name (with a dot).

    Arguments/return value:

    `attr`: The object we are verifying is a method

    `returns`: `True` if `attr` is a method

    """
    if ismethod(attr) or isfunction(attr):
        cmmatch = _cmnames.match(attr.__qualname__)
        if cmmatch:
            return True
    return False


def _getdoc(attr: object) -> str:
    R"""Extended get documentation of attribute

    This extended `getdoc` function will first try to return the
    documentation string of the attribute, and if that is not
    available, the related (possibly multiline) comment.

    Arguments/return value:

    `attr`: The object to get the doc string from

    `returns`: The documentation string

    """
    doc = getdoc(attr)
    if not doc:
        try:
            doc = getcomments(attr)
        except:
            doc = None
    if not doc:
        if hasattr(attr, "__name__"):
            m = f" from {attr.__name__}"
        else:
            m = ""
        raise PyPiMDocError(
            f"Unable to get documentation string (or comment){m}")
    return doc


def _signature(attr: object) -> str | None:
    R"""Get signature of function or method as a text string

    Returns the signature of a function or method. If it is a method,
    `self` is removed from the signature. If it is not a function or
    method, `None` is returned.

    Arguments/return value:

    `attr`: The object to get the signature of

    `returns`: The signature of the function or method as a text
    string, or `None` if `attr` is not a function or a method

    """
    if isfunction(attr):
        sig = str(signature(attr))
        if _ismethod(attr):
            if "(self, " in sig:
                sig = sig.replace("self, ", "", 1)
            elif "(self)" in sig:
                sig = sig.replace("self", "", 1)
        return sig
    return None


#
# Exceptions/errors by the module
#

class PyPiMDocError(Exception):
    R"""Any error in the `pypimdoc` module"""
    def __init__(self, errmsg: str):
        self.errmsg = errmsg


#
# The main class of the module
#

class PyPiMDoc:
    R"""The Python module documentation class

    The class implementing the different MD-macros used in the
    markdown template for the documentation of a Python module.

    The most common usage of the module is as a console script.  As a
    consequence, the users of the module seldom need to use this class
    themselves.

    """
    

    def __init__(
            self,
            filename: str,
            name: str = "",
            base_heading_level: int = 1,
            toc_begin: int = 1,
            toc_end: int = 3):
        R"""Initialize a Python module documentation object

        Initialize a Python module documentation object, including
        loading the Python module (Python source code) and prepare the
        document generation.

        Arguments:

        `filename`: The file name of the module to document

        `name`: The name of the module (default generated from the
        `filename`)

        `base_heading_level`: All generated headings are at this level
        or above (default 1)
        
        `toc_begin`: Include items in table of contents from this
        level (relative to `base_heading_level`, default 1)

        `toc_end`: Include items in table of contents to this level
        (relative to `base_heading_level`, default 2)

        """

        # Initiate object values from the constructor arguments (or defaults)
        self.filename = filename
        self.name = name
        self.base_heading_level = base_heading_level
        self.toc_begin = base_heading_level + toc_begin - 1
        self.toc_end = base_heading_level + toc_end - 1

        # The documentation can contain a set of table of contents
        self.mktoc = set()

        # Save toc items here (for each toc set)
        self.tocpart = {}
        self.doc_tocpart = {}

        # A list of used ids (to ensure the we generate unique ids)
        self.idlist = []

        # How different level of headers are created (pre, post), 0
        # means no header
        self.hmarkers = [
            ("", ""),		# 0
            ("# ", ""),		# 1
            ("## ", ""),	# 2
            ("### ", ""),	# 3
            ("#### ", ""),	# 4
            ("**", "**"),	# 5
            ("*", "*")]		# > 5

        # Name of the module to document (either given or from the file name)
        if not self.name:
            mpn = _pysrcname.match(self.filename)
            if mpn:
                self.name = mpn["name"]
            else:
                raise PyPiMDocError(
                    f"Unable to determine module: {self.filename}")

        # Load the module to document
        spec = importlib.util.spec_from_file_location(self.name, self.filename)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

        # Make namespaces used by the MD-macros
        self.mgns = vars(self.module)
        self.mlns = {
            "mdoc_doc": self._mdoc_doc,
            "mdoc_title": self._mdoc_title,
            "mdoc_body": self._mdoc_body,
            "eval": self._md_eval,
            "cmd": self._md_cmd
        }
        # Are the names above safe to use?

        # List all MD-macros (from this class starting with "_md_")
        self.md_macros = _list_md_macros(
            self, rm_pre = True, qualname = False, sort_order = None)


    def _get_real_hlevel(self, hlevel: int) -> int:
        R"""Calibrate levels with the base heading level

        Calibrate all references to heading levels by added the base
        headings level to the given heading level (except when the
        given heading level is zero).

        Arguments/return value:

        `hlevel`: The given heading level

        `returns`: The calibrated (adjusted) heading level

        """
        if hlevel > 0:
            hlevel +=  self.base_heading_level - 1
        return hlevel

    
    def _get_title_and_doc(self, obj: object | None = None) -> tuple:
        R"""Split title and body of documentation string
        
        The first line could be the title of the documentation string if
        it is a single line of text followed by an empty line.
        
        Arguments/return value:
        
        `obj`: An object to get the documentation string from, or `None`
        meaning the documentation string of the module

        `returns`: If the first line of the documentation string of the
        object is separate, return the first line and the rest of the
        documentation string as a two-tuple, otherwise retrun `None` and
        the unchanged documentation string as a two-tuple
        
        """

        # If no object, it is the module
        if not obj:
            obj = self.module

        # Get documentation string from object
        try:
            doc = _getdoc(obj)
        except:
            doc = None
            title = None

        # If documentation, try to split it into a title and a body
        if doc:
            doclist = doc.strip().splitlines()
            if (len(doclist) > 1 and (title:=doclist[0].strip())
                and (doclist[1].strip() == "")):
                doc = "\n".join(doclist[1:]).strip()
            else:
                title = None

        # Return title and body of documentation string
        return title, doc

    
    def _raw_mdoc(self, obj: object | None, sel: Callable) -> str:
        return sel(self._get_title_and_doc(obj))
        

    def _mdoc_doc(self, obj: object | None = None) -> str:
        R"""The documentation string of an object

        The fuction returns the complete documentation string of the
        object, including the title (the first line), the following
        empty line and the body. The function takes one optional
        argument, the object to get the documentation string from. If
        no argument is given, the documentation string of the module
        is used.

        Arguments/return value:

        `obj`: The object to get the documentation string from
        (default `None`, meaning get the documentation string of the
        module)

        `returns`: The documentation string of the object

        """
        return self._raw_mdoc(obj, _combined)
    
    
    def _mdoc_title(self, obj: object | None = None) -> str:
        R"""The title of the documentation string of an object

        A function returning the first line of documentation string,
        often considered the title of the documentation string. This
        only succeeds if the first line is followed by an empty
        line. The function takes one optional argument, the object to
        get the documentation string from. If no argument is given,
        the documentation string of the module is used.

        Arguments/return value:

        `obj`: The object to get the documentation string title from
        (default `None`, meaning get the documentation string title of
        the module)

        `returns`: The documentation string title of the object

        """
        return self._raw_mdoc(obj, _title)
    
    
    def _mdoc_body(self, obj: object | None = None) -> str:
        R"""The body of the documentation string of an object
        
        The body of the documentation string, meaning the
        documentation string except the title (the first line) and the
        empty line between the between the title and the body. The
        function takes one optional argument, the object to get the
        documentation string from. If no argument is given, the
        documentation string of the module is used.

        Arguments/return value:

        `obj`: The object to get the documentation string body from
        (default `None`, meaning get the documentation string body of
        the module)

        `returns`: The documentation string body of the object

        """
        return self._raw_mdoc(obj, _body)
    
    
    def _mk_h(
            self,
            title: str,
            hlevel: int,
            hid: str = "",
            in_doc: bool = False,
            no_toc: bool = False) -> str:
        R"""Create a heading and add it to the table of contents

        Create a heading at the given level `hlevel` with the given
        title. If a table of contents is generated, add an id to the
        title and add an entry to the table of contents.

        Arguments/return value:

        `title`: The title (text) of the heading (section)

        `hlevel`: The heading level, where 1 is the highest level

        `hid`: Optional heading id that might be modified to ensure
        uniqueness (if not given, it will generated if needed)

        `in_doc`: Handle a heading in documentation string (default
        `False`)

        `no_toc`: If `True` do not add to table of contents
        (default `False`)

        `returns`: A heading typeset to the correct heading level

        """

        # If we should add table of contents
        if not no_toc:

            # Create `hid` if not given
            if hid:
                hid = _mkid(hid, self.idlist)
            else:
                hid = _mkid(title, self.idlist)

            # If it is inside a documentation string, handle it differently
            if in_doc:
                tocpart = self.doc_tocpart
            else:
                tocpart = self.tocpart

        # Create header markers
        hlevelpre, hlevelpost = self.hmarkers[hlevel]
            
        # Add to table of content
        if not no_toc:
            if (self.mktoc and hlevel >= self.toc_begin
                and hlevel <= self.toc_end):
                for t in self.mktoc:
                    ilevel = hlevel - self.toc_begin
                    tocpart[t]["items"].append({
                        "ilevel": ilevel,
                        "content": f"[{title}](#{hid})"})
                    
        # Create and return header
        if hid:
            idtxt = f'<a id="{hid}"></a>'
        else:
            idtxt = ""
        return f'\n{hlevelpre}{idtxt}{title}{hlevelpost}\n'


    def _flush_h(self):
        R"""Add the toc part of documentation string to toc

        This method appends the temporarly saved table of contents
        itmes from a documentation string to the givne (global) table
        of contents items and then empties the list of temporarly
        saved table of contents itmes.

        """
        for t in self.mktoc:
            if self.doc_tocpart[t]["items"]:
                self.tocpart[t]["items"] += self.doc_tocpart[t]["items"]
                self.doc_tocpart[t]["items"] = []

    
    def process_template(
            self, template: TextIOBase,
            macro_types: str = "block") -> str:
        R"""Read and process template

        The template file is the driver of the document generation. In
        its simplest form, the template is a markdown document that
        becomes the module documentation. The template includes some
        special commands (MD-macros) used to fetch documentation from
        the module (including the documentation strings in the
        module).

        Arguments/return value:

        `template`: The README template file

        `macro_types`: Either `"block"` or `"inline"`, where
        `"block"` means that the MD-macros are inside HTML comment
        blocks and `"inline"` means that MD-macros are directly
        inline in the markdown documentation strings (default
        `"block"`)

        `returns`: The processed markdown README file content

        """

        # Start the README file with produced-by/where-to-find comments 
        mdoc = f"<!-- {produced_by} -->\n"
        mdoc += f"<!-- {where_to_find}  -->\n"

        # We are not in a code block
        in_code_block = False
        code_block = ""

        # We are not in a for-loop in the beginning
        in_loop = False
        loop_body = ""
        
        # We are not in inline code mode in the beginning
        inline = False

        # Go through each line
        for line in template:

            # A code block?
            if _md_code[macro_types]["begin"].match(line):
                in_code_block = True
                continue

            # End code block
            elif in_code_block and _md_code[macro_types]["end"].match(line):
                self._md_code(code_block)
                in_code_block = False
                code_block = ""
                continue

            # Inside code block
            elif in_code_block:
                code_block += line
                continue

            # A for-loop?
            elif (loop_info := _md_forloop[macro_types]["begin"].match(line)):
                in_loop = True
                in_loop_var_str = loop_info["var"] 
                in_loop_list_str = loop_info["listexpr"]
                continue

            # End of for-loop
            elif in_loop and _md_forloop[macro_types]["end"].match(line):
                mdoc += self._md_for_in(
                    in_loop_var_str, in_loop_list_str, loop_body)
                in_loop = False
                loop_body = ""
                continue
            
            # Inside for-loop
            elif in_loop:
                loop_body += line
                continue

            # Is this inline code in the markdown text?
            if _inline_code.match(line):
                if inline:
                    inline = False
                else:
                    inline = True
                mdoc += line
                continue
            elif inline:
                mdoc += line
                continue

            # Is this a command
            mcmd = _md_macro[macro_types].match(line)
                
            # Yes, a command
            if mcmd:

                # Process the found MD-macro
                res = self.process_macro(mcmd["macro"], mcmd["args"])

                # If it produce text, add it to the documentation
                if res:
                    mdoc += res 

            # No
            else:

                # Just save the documentation line
                mdoc += line

        # Add toc
        if self.tocpart:

            # Go through every toc (we can have more than one)
            for t in self.tocpart:

                # Might need this to adjust indent
                min_i = min([i["ilevel"] for i in self.tocpart[t]["items"]])

                # For each text item in the current toc
                toc = []

                # Each toc text item starts with this
                start = self.tocpart[t]["toc_item_start"]

                # Each item in the toc
                for item in self.tocpart[t]["items"]:

                    # Calculate the indent size and make the indentation
                    indentsize = \
                        self.tocpart[t]["toc_item_indent"] * \
                        (item["ilevel"] - min_i)
                    indent = " " * indentsize

                    # Add the text item 
                    toc.append(f'{indent}{start}{item["content"]}')

                # Insert the toc in the documentation string
                mdoc = mdoc.replace(
                    f"%({t})s",
                    self.tocpart[t]["toc_item_end"].join(toc))

        # Return doc
        return mdoc

    
    def process_macro(self, macro_name: str, args_str: str) -> str:
        R"""Process a MD-macro

        Process a MD-macro with the given name and arguments.

        Arguments/return value:

        `macro_name`: MD-macro name

        `args_str`: the arguments to the MD-macro as a string

        `returns`: returns the documentation part generated by the MD-macro

        """

        # Get MD-macro
        full_name = "_md_" + macro_name
        if macro_name in self.md_macros and hasattr(self, full_name):
            macro = getattr(self, full_name)
        else:
            raise PyPiMDocError(f"Unknown MD-macro: {macro_name}")

        # Get the arguments
        _args_kw = lambda *args, **kw: (args, kw)
        args, kw = eval(
            f"_args_kw({args_str})",
            globals = self.mgns, locals = self.mlns | {"_args_kw": _args_kw})

        # Perform the macro
        return macro(*args, **kw)

    
    def _md_h(self, title: str, hlevel: int, 
              hid: str = "", no_toc: bool = False) -> str:
        R"""Insert a heading

        Insert a heading at the given level (including adjustment
        from base level).

        Arguments/return value:

        `title`: A title

        `hlevel`: The heading level for the title

        `hid`: An id for the title that is used to be able to link to
        it (default empty, meaning it will be generated from the title)

        `no_toc`: Set this to `True` if the heading should not be
        included in the table of contents (default `False`)

        `returns`: The formatted heading

        """

        # Level is relative
        hlevel = self._get_real_hlevel(hlevel)

        # Create and return the header
        return self._mk_h(title, hlevel, hid, no_toc)
            
     
    def _md_doc(
            self,
            obj: object | str | list | None = None,
            name: str = "",
            title: str = "",
            hid: str = "",
            hlevel: int = 0,
            sig: str = "",
            init: bool = False,
            complete: bool | list = False,
            init_title: str = "Initialize",
            skip_firstline: bool = False,
            doc_headings: bool = True,
            name_transform: Callable = lambda n: n,
            title_transform: Callable = lambda n: n) -> str:
        R"""Insert the documentation of the given object

        Returns the documentation for the given object (class, method,
        function). If no object is given, the documentation of the
        module is returned.

        Arguments/return value:

        `obj`: The object (function, method, class) to prepare and
        return the documentation for. If `obj` is a list, the
        documentation for all objects in the list are prepared and
        returned (in separate paragraphs). If no object is given, the
        documentation for the module is prepared and returned
        (optional).
        
        `name`: The name of the object (optinal; we can find it)

        `title`: A title for the documentation if the heading is
        generated (optional; we will generate a proper title if
        `hlevel` is higher than zero and no title is given)

        `hid`: An id for the title that is used to be able to link to
        it (optional; will be genrated if needed and not given)

        `hlevel`: The heading level, cf. HTML h tag level (default 0,
        meaning no heading generated)

        `sig`: A signature can be provided for methods/functions, but
        this is usualy not needed since the MD-method is able to
        generate this from the method/function (default `""`)

        `init`: Include the documentation and signature of the
        `__init__` method in the documentation of the object if the
        object is a class and has an `__init__` method (default
        `False`)

        `complete`: If the objetc is a class, include the
        documentation for the class, its constructor (the `__init__`
        method) and all non-hidden methods, when complete is `True`,
        or the listed methods, when complete is a list of methods
        (default `False`)

        `init_title`: If `complete` is set (`True` or a list) and the
        objetc is a class, use this combined with the class name as
        the title for the constructor (the `__init__` method)

        `skip_firstline`: The first line of the documentation string
        might have a specific meaning, like a title or a sub-title,
        and sometimes we might want to skip this part in the generated
        documentation.

        `doc_headings`: if `True`, detect and handle headings in the
        documentation string, otherwise do nothing (default `True`)

        `name_transform`: a function that takes a text string as an
        argument and returns a text string; the function can be used
        to transform the (found) name

        `title_transform`: a function that takes a text string as an
        argument and returns a text string; the function can be used
        to transform the (found) title

        `returns`: The documentation of the given object (or the module)

        """

        # The documentation of the module attribute
        adoc = ""

        # The special case, if `obj` is a list
        if type(obj) is list:

            # For each object, get the documentation
            for an_obj in obj:
                adoc += f"\n{self._md_doc(an_obj, hlevel=hlevel).strip()}\n"

            # Return the combined documentation
            return adoc
        
        # Level is relative
        org_hlevel = hlevel
        hlevel = self._get_real_hlevel(hlevel)

        # Get the object (attribute)
        if obj:
            if type(obj) is str:
                attr = _get_nested_attr(self.module, obj)
            else:
                attr = obj
            if not name:
                name = name_transform(attr.__qualname__)
        else:
            attr = self.module
            if not name:
                name = name_transform(self.name)
        
        # Get documentation string

        # First line often have a special meaning (title or sub-title)
        firstline, raw_doc = self._get_title_and_doc(attr)

        # Should we detect and handle headings in documentation strings?
        if raw_doc and doc_headings:

            # Initialize variables
            doc = ""		# The handled documentation string
            inline_code = False	# Inside an inline code block

            # Go through each line of the documentation string
            for line in raw_doc.splitlines():

                # Is the line the start or end of an inline code
                # block? And if so, toggle the `inline_code` flag
                if _inline_code.match(line):
                    inline_code = True if inline_code is False else False

                # If inside an inline code block
                if inline_code:

                    # Inline code block content is unmodified
                    doc += f"{line}\n"

                # If not inside an inline code block
                else:
                    
                    # Is this a heading
                    heading = _md_heading.match(line)
                    if heading:

                        # Create a heading
                        level = self._get_real_hlevel(len(heading["level"]))
                        doc += self._mk_h(
                            heading["title"], level, in_doc = True)

                    # Otherwise, just add the unmodified line
                    else:
                        doc += f"{line}\n"
        
        # Do nothing with the raw documentation string
        else:
            doc = raw_doc

        # If `hlevel` < 1 and a title, we don't need `hid` (and levelmarkers)
        
        # If `hlevel` >= 1, a title (and maybe `hid`) has to be is added
        if hlevel > 0 and not title:

            # Create `title` (and `hid`) from attribute
            for (ttype, ttest) in [
                    ("Class", isclass),
                    ("Method", _ismethod),
                    ("Function", isfunction),
                    ("Module", ismodule)]:
                if ttest(attr):
                    title = f"{ttype} `{name}`"
                    if hid:
                        hid = _mkid(hid, self.idlist)
                    else:
                        hid = _mkid(f"{name.lower()}", self.idlist)
                    break

            # Not able to create `title`, use first line as `title`
            else:

                # Get first line from `doc` and make it `title` + make `hid`
                if firstline:
                    title = firstline
                    firstline = None
                    if hid:
                        hid = _mkid(hid, self.idlist)
                    else:
                        hid = _mkid(title, self.idlist)
                else:
                    raise PyPiMDocError("Unable to find title for doc string")

        # Get signature of method 
        if not sig and isfunction(attr):
            sig = _signature(attr)

        # Signture of class from `__init__` (and its documentation string)
        elif isclass(attr) and hasattr(attr, "__init__") and init:
            fline, init_doc = self._get_title_and_doc(attr.__init__)
            if fline:
                init_doc = f"**{fline}**\n\n{init_doc}"
            if init_doc:
                doc += f"\n\n{init_doc}"
            if not sig:
                sig = _signature(attr.__init__)
            
        # Add the title to the module doc
        if title:
            adoc += self._mk_h(title_transform(title), hlevel, hid)

        # Flush documentation string headings to table of content list
        self._flush_h()

        # Add signature
        if sig:
            if "." in name:
                fname = name.split(".")[-1]
            else:
                fname = name
            adoc += f"\n```python\n{fname}{sig}\n```\n"

        # Arguments/Returns headers in the documentation string
        doc = _margsheader.sub(r'\n\n{{\1}}\n\n', doc, re.MULTILINE)
        doc = doc.replace("{{", "**").replace("}}", "**")
        
        # Complete class, including methods
        if complete and isclass(attr):

            # Include the constructor (`__init__`) if implemented
            if (not init and hasattr(attr, "__init__")
                and _ismethod(attr.__init__)):
                method_kw_list = [
                    {"obj": attr.__init__,
                     "name": name,
                     "title": f"{init_title} `{name}`"}]
            else:
                method_kw_list = []

            # The methods are listed
            if type(complete) is list:
                method_kw_list += [{"obj": m} for m in complete]

            # If complete is not a list, find all public methods
            else:
                for n in dir(attr):
                    m = getattr(attr, n)
                    if _ismethod(m) and m.__name__[0] != "_":
                        method_kw_list.append({"obj": m})

            # Add the documentation for the methods of the class
            for kw in method_kw_list:
                kw["hlevel"] = org_hlevel + 1 if org_hlevel > 0 else 0
                kw["name_transform"] = name_transform
                doc += "\n\n" + self._md_doc(**kw)

        # Add the documentation string to the module doc
        if firstline and not skip_firstline:
            doc = f"*{firstline}*\n\n{doc}"
        adoc += f"\n{doc}\n"

        # Return the documentation of the object (or module)
        return adoc
    

    def _md_toc(self, name: str = "toc", btoc: bool = True,
            toc_item_start: str = " - ", toc_item_end: str = "\n",
            toc_item_indent: int = 4) -> str:
        R"""Insert a table of contents

        Insert a table of contents with all headings following this
        MD-macro until the end of document or until a matching `etoc`
        MD-macro. If the `btoc` argument is `False`, the table of
        contents will be inserted here but items (headings) for the
        table of contents will not be registered yet. You then need to
        insert a `btoc` MD-macro in the README template to start
        collcting items for the table of contents.

        Is is also possible to have different sets of table of
        contents.  To do this, give each set a unique name (the
        default name is `"toc"`).
        
        Arguments/return value:

        `name`: The name of this specific table of contents; only
        needed if you have different sets og groups of table of
        contents in the README template (optional, default `"toc"`)

        `btoc`: If `False`, do not start to collect items for the
        table of contents here (default `True`)

        `toc_item_start`: The text string preceeding every item in the
        table of contents (default `" - "`)

        `toc_item_end`: The text string following every item in the
        table of contents (default `"\n"`)

        `toc_item_indent`: (default 4)

        `returns`: The formatted version of the table of contents

        """

        # Start collecting items to table of contents (with the given name)
        if btoc:
            self._md_btoc(name)

        # The datastructure for this table of contents
        self.tocpart[name] = {
            "items" : [],
            "toc_item_start": toc_item_start,
            "toc_item_end": toc_item_end,
            "toc_item_indent": toc_item_indent
            }

        # For items inside documentation strings
        self.doc_tocpart[name] = {
            "items" : [],
            "toc_item_start": toc_item_start,
            "toc_item_end": toc_item_end,
            "toc_item_indent": toc_item_indent
            }
        
        # Return a placeholder for the table of contents
        return f"%({name})s"

    
    def _md_btoc(self, name: str = "toc"):
        R"""Start to collect items to table of contents

        Start to collect items to table of contents (with the given
        name).  From now on and until the matching `etco` MD-macro or
        the end of the file, every heading will be added as an item to
        the table of contents (with the exceptions of headings marked
        not to be added to table of contents).

        Arguments:

        `name`: The name of this specific table of contents; only
        needed if you have different sets og groups of table of
        contents in the README template (optional, default `"toc"`)

        """
        self.mktoc.add(name)
        
        
    def _md_etoc(self, name: str = "toc"):
        R"""Stop collecting items to table of contents

        Stop collecting items to table of contents (with the given
        name).
        
        Arguments:
        
        `name`: The name of this specific table of contents; only
        needed if you have different sets og groups of table of
        contents in the README template (optional, default `"toc"`)
        
        """
        self.mktoc.discard(name)


    def _md_for_in(self, loop_var: str, loop_list: str, loop_body: str) -> str:
        R"""Loop through a list of documentation elements

        Loop documentation

        """
        mdoc = ""
        save_mlns = self.mlns.copy()
        for x in eval(loop_list, globals=self.mgns, locals=self.mlns):
            self.mlns[loop_var] = x
            mdoc += self.process_template(StringIO(loop_body), "inline")
        self.mlns = save_mlns
        return mdoc
        
        
    def _md_eval(self, code: str) -> str:
        R"""Insert the text output of the Python code

        Insert the text output of the Python code evaluated in the
        name space of the module and the MD-macros’ local name space.
        
        Arguments/return value:

        `code`: The Python code to evaluate

        `returns`: The resulting text

        """
        return eval(code, globals=self.mgns, locals=self.mlns)

    
    def _md_code(self, code: str):
        R"""Execute the code 

        Execute the code to populate the MD-macros’ local name space
        that later can be used in MD-macros arguments and in the code
        of the MD-macro `eval`.

        Arguments:

        """
        exec(code, globals=self.mgns, locals=self.mlns)

        
    def _md_cmd(self, cmd: str) -> str:
        R"""Insert the text output of the command

        Insert the text output of the (shell) command.

        Arguments/return value:

        `cmd`: The shell command

        `returns`: The output of the command
        
        """
        cmdl = cmd.split()
        res = subprocess.run(cmdl, text=True, capture_output=True)
        if res.returncode != 0:
            raise PyPiMDocError(f"Command failed: {cmd}")
        else:
            return res.stdout.strip()
        

    def _md_cmd_cb(self, cmd: str) -> str:
        R"""Insert the text output of the command as a code block

        Insert the text output of the (shell) command as a code block.

        Arguments/return value:
        
        `cmd`: The shell command

        `returns`: The output of the command in a code block
        
        """
        return f"```\n{self._md_cmd(cmd)}\n```\n"
    

    def _md_help(self, cmd: str = "", sub_cmd: str = "",
                 title: str = "", hlevel: int = 0, hid: str = '',
                 no_toc: bool = False) -> str:
        R"""Insert the output from a help command

        Insert the output from a help command reformatted as markdown.
        The output of the help command is expected to be formated as
        the Python module `argparse` formats the help text.
        
        Arguments/return value:

        `cmd`: The help command (default empty, meaning execute the
        current moudule's file module with the command line argument
        `"-h"`)

        `sub_cmd`: The sub-command (default empty, meaning the help
        message of the main command)
        
        `title`: The title used in the heading (create a default title
        if this is not provided)

        `hlevel`: The heading level for the title (default 0, meaning
        no heading)

        `hid`: An id for the title that is used to be able to link to
        it (default empty, meaning it will be generated from the
        title)

        `no_toc`: Set this to `True` if the heading should not be
        included in the table of contents (default `False`)

        `returns`: The heading and output of the help command formated

        """

        # A sub command?
        if sub_cmd:
            sub = f" {sub_cmd}"
        else:
            sub = ""

        # Make the heading (with title), if needed
        if hlevel > 0:
            if not title:
                title = f"Command `{self.name}{sub}`"
            heading = self._md_h(title, hlevel, hid, no_toc) + "\n\n"
        else: 
            heading = ""

        # Get the help text
        if not cmd:
            cmd = f"{sys.executable} {self.filename}{sub} -h"

        # Get help text and convert it to markdown
        help_txt = self._md_cmd(cmd)
        md_txt = help2md(help_txt)
        
        # Return heading and help text
        return heading + md_txt


#
# More help functions
#

def _list_md_macros(
        cls: object = PyPiMDoc,
        pre: str = "_md_",
        rm_pre: bool = False,
        qualname: bool = True,
        sort_order: list | None = [
            "^h$", "([be])?doc", "([be])?toc", "eval", "([lbe])?code",
            "[l]?cmd", "help"
        ]) -> list:
    R"""List all the MD-macros

    List all the MD-macros if the given object or class.

    Arguments/return value:

    `cls`: Class or object to list the MD-macros from (default `PyPiMDoc`)

    `pre`: The pre-string of all MD-macros (default `"_md_"`)

    `rm_pre`: Remove the pre-string from the name of ech macro in the
    list (default `False`)

    `qualname`: Use the fully qualified name of the macros (include
    the class name, default `True`)

    `sort_order`: A list of regular expressions specifing the sort
    order in the returned list of macro names; if this is `None` no
    extra sorting is done (for the regular expression with a group,
    names with an empty group are put in front of the other ones
    matching the same regular expressions; see the default value in
    the method definition)

    `returns`: The list of MD-macro names

    """

    # Find the MD-macros (with the names starting with `pre`)
    psize = len(pre)
    mdm = [m for m in dir(cls) if m[:psize] == pre]

    # Use the fully qualified name?
    if qualname:
        mdm = [getattr(cls, m).__qualname__ for m in mdm]

    # Or remove the first part of the name, the `pre` string
    elif rm_pre:
        mdm = [m[psize:] for m in mdm]

    # Should the macro names be sorted in a specific order?
    if sort_order:

        # Do the sorting by groups (the sort order groups)
        mdm_sort = {so: [] for so in sort_order}
        rest = []
        for m in mdm:
            for so in sort_order:
                ma = m.split(".")[-1]
                if ma[:psize] == pre:
                    ma = ma[psize:]
                if me:=re.match(so, ma):
                    if me.groups() and not me.group(1):
                        mdm_sort[so] = [m] + mdm_sort[so]
                    else:
                        mdm_sort[so].append(m)
                    break
            else:
                rest.append(m)

        # Morge the groups to a single sorted list
        mdm = []
        for so in sort_order:
            mdm += mdm_sort[so]
        mdm += rest

    # Return a list of the (sorted) macro names
    return mdm


#
# The rest of the code is to run the module as an interactive command
#
        
# Execute this module as a program
def main():

    # Formatters
    formatters = ["markdown", "html", "latex"]

    # Create overall argument parser
    import argparse
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0])
    parser.add_argument(
        "pysrc", metavar="PYSRC",
        help="module source code file")
    parser.add_argument(
        "-V", "--version", action="version",
        version=f"%(prog)s " + version)
    parser.add_argument(
        "-t", "--template",
        type=argparse.FileType("r"),
        help="markdown template (default 'README.template')")
    parser.add_argument(
        "-o", "--outfile", default=sys.stdout, type=argparse.FileType("w"),
        help="output file (default stdout)")
    #parser.add_argument(
    #    "-f", "--formatter", default=None, choices=formatters,
    #    help="formatter to use (default guessed by filename or 'markdown')")
    #parser.add_argument(
    #    "-s", "--style", default="emacs",
    #    help="style (default 'emacs')")
    parser.add_argument(
        "-l", "--base-heading-level", default=1, type=int,
        help="base (start) level of headings " + \
          "(default 1, like '<h1></h1>' in HTML)")
    parser.add_argument(
        "-i", "--inline-md-macros", action="store_true",
        help="MD-macros are inline in the markdown template " + \
        "(and not inside HTML-comments)")
    parser.add_argument(
        "-n", "--name", default=None,
        help="name of module (default source code filename without '.py')")
    
    # Parse arguments
    args = parser.parse_args()

    # Choose formatter (html or latex)
    # if args.formatter:
    #     if args.formatter == "html":
    #         formatter = HtmlFormatter()
    #     elif args.formatter == "latex":
    #         formatter = LatexFormatter()
    #     else:
    #         formatter = None
    # else:
    #     if Path(args.outfile.name).suffix in [".html", ".htm"]: 
    #         formatter = HtmlFormatter()
    #     elif Path(args.outfile.name).suffix in [".ltx", ".tex", ".latex"]: 
    #         formatter = LatexFormatter()
    #     else:
    #         formatter = None
            
    # Choose style
    #try:
    #    style = get_style_by_name(args.style)
    #except ClassNotFound:
    #    print(f"{sys.argv[0]}: unknown style {args.style}", file=sys.stderr)
    #    sys.exit(1)

    # MD-macros inline or in HTML comment blocks
    if args.inline_md_macros:
        macro_types = "inline"
    else:
        macro_types = "block"
        
    # Create `PyPiMDoc` instance and create the documentation
    pypimdoc = PyPiMDoc(args.pysrc, base_heading_level=args.base_heading_level)
    md = pypimdoc.process_template(args.template, macro_types)
    print(md, file=args.outfile)


# execute this module as a program
if __name__ == '__main__':
    main()


# Extra appended code for pypi dist
