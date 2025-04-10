<!-- This documentation is generate using the `pypimdoc` module -->
<!-- Available from [PyPi](https://pypi.org/project/pypimdoc/)  -->


### <a id="module-pypimdoc"></a>A Python module for generating Python module documentation

When developing Python modules, documentation is important. The source
code of a Python module inludes a lot of documentation, including
documentation strings, comments and code. Instead of writing separate
documents describing the features of a Python module, the goal of the
`pypimdoc` module is to use the documentation found in the source code
and produced by the module itself to generate this
documentation. Based on a template file, the documentation is
generated from the source code of the module. As a consequence, when
the source code of the module (including the documentation strings) is
updated, the documentation of the module is also updated.

The `pypimdoc` module, including its console script, was developed to
generate the module documentation at [PyPi](https://pypi.org/) for my
own Python modules, including
[`pypimdoc`](https://pypi.org/project/pypimdoc/) (this module),
[`help2md`](https://pypi.org/project/help2md/)
[`webinteract`](https://pypi.org/project/webinteract/) and
[`onepw`](https://pypi.org/project/onepw/). The decissions made when
developing the module is influenced by this (and hence the name of the
module).

**<a id="Table+of+contents"></a>Table of contents**

 - [Introduction](#Introduction)
 - [Install the module and its console script](#Install+the+module+a)
 - [Module documentation macros](#Module+documentation)
     - [MD-macro `h`](#h1)
     - [MD-macro `doc`](#doc1)
     - [MD-macro `toc`](#toc1)
     - [MD-macro `btoc`](#btoc1)
     - [MD-macro `etoc`](#etoc1)
     - [MD-macro `eval`](#eval1)
     - [MD-macro `code`](#code1)
     - [MD-macro `cmd`](#cmd1)
     - [MD-macro `cmd_cb`](#cmd_cb1)
     - [MD-macro `help`](#help1)
     - [MD-macro `for_in`](#for_in1)
 - [Help functions for the MD-macros](#Help+functions+for+t)
     - [Help function `mdoc_body`](#mdoc_body1)
     - [Help function `mdoc_doc`](#mdoc_doc1)
     - [Help function `mdoc_title`](#mdoc_title1)
 - [To use the module as a console script](#To+use+the+module+as)
     - [Command `pypimdoc`](#Command+%60pypimdoc%60)
 - [Class `PyPiMDoc`](#pypimdoc1)
     - [Initialize `PyPiMDoc`](#Initialize+%60PyPiMDoc)
     - [Method `PyPiMDoc.process_macro`](#pypimdoc.process_ma1)
     - [Method `PyPiMDoc.process_template`](#pypimdoc.process_te1)

### <a id="Introduction"></a>Introduction


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



### <a id="Install+the+module+a"></a>Install the module and its console script

The easiest way to install the module is using `pip`:

```
pip install pypimdoc
```

This will install the module and the console script `pypimdoc`. The
source code of the module is also available from my [file
repository](https://www.pg12.org/dist/py/lib/pypimdoc/).

You can print the help message of the console script to learn how to
use it (or read the [console script section](#To+use+the+module+as)
below):

```
pypimdoc -h
```


### <a id="Module+documentation"></a>Module documentation macros

The module documentation macros (MD-macros) are used in the README
template to get documentation and information from the Python module
documented. For example, the following line creates the complete
documentation of the class `PyPiMDoc` (including all public methods):

```
<!-- doc(PyPiMDoc, hlevel = 1, complete = True) -->
```

In the [previous section](#pypimdoc1), the documentation of
the [Class `PyPiMDoc`](pypimdoc1), is the result of this
MD-macro example. Below follows the documentation of each MD-macro.

<!-- This documentation is generate using the `pypimdoc` module -->
<!-- Available from [PyPi](https://pypi.org/project/pypimdoc/)  -->


#### <a id="h1"></a>MD-macro `h`

```python
h(title: str, hlevel: int, hid: str = '', no_toc: bool = False) -> str
```

*Insert a heading*

Insert a heading at the given level (including adjustment
from base level).

**Arguments/return value:**

`title`: A title

`hlevel`: The heading level for the title

`hid`: An id for the title that is used to be able to link to
it (default empty, meaning it will be generated from the title)

`no_toc`: Set this to `True` if the heading should not be
included in the table of contents (default `False`)

`returns`: The formatted heading


<!-- This documentation is generate using the `pypimdoc` module -->
<!-- Available from [PyPi](https://pypi.org/project/pypimdoc/)  -->


#### <a id="doc1"></a>MD-macro `doc`

```python
doc(obj: object | str | list | None = None, name: str = '', title: str = '', hid: str = '', hlevel: int = 0, sig: str = '', init: bool = False, complete: bool | list = False, init_title: str = 'Initialize', skip_firstline: bool = False, doc_headings: bool = True, name_transform: collections.abc.Callable = <function PyPiMDoc.<lambda> at 0x10501ad40>, title_transform: collections.abc.Callable = <function PyPiMDoc.<lambda> at 0x10501ade0>) -> str
```

*Insert the documentation of the given object*

Returns the documentation for the given object (class, method,
function). If no object is given, the documentation of the
module is returned.

**Arguments/return value:**

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


<!-- This documentation is generate using the `pypimdoc` module -->
<!-- Available from [PyPi](https://pypi.org/project/pypimdoc/)  -->


#### <a id="toc1"></a>MD-macro `toc`

```python
toc(name: str = 'toc', btoc: bool = True, toc_item_start: str = ' - ', toc_item_end: str = '\n', toc_item_indent: int = 4) -> str
```

*Insert a table of contents*

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

**Arguments/return value:**

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


<!-- This documentation is generate using the `pypimdoc` module -->
<!-- Available from [PyPi](https://pypi.org/project/pypimdoc/)  -->


#### <a id="btoc1"></a>MD-macro `btoc`

```python
btoc(name: str = 'toc')
```

*Start to collect items to table of contents*

Start to collect items to table of contents (with the given
name).  From now on and until the matching `etco` MD-macro or
the end of the file, every heading will be added as an item to
the table of contents (with the exceptions of headings marked
not to be added to table of contents).

**Arguments:**

`name`: The name of this specific table of contents; only
needed if you have different sets og groups of table of
contents in the README template (optional, default `"toc"`)


<!-- This documentation is generate using the `pypimdoc` module -->
<!-- Available from [PyPi](https://pypi.org/project/pypimdoc/)  -->


#### <a id="etoc1"></a>MD-macro `etoc`

```python
etoc(name: str = 'toc')
```

*Stop collecting items to table of contents*

Stop collecting items to table of contents (with the given
name).

**Arguments:**

`name`: The name of this specific table of contents; only
needed if you have different sets og groups of table of
contents in the README template (optional, default `"toc"`)


<!-- This documentation is generate using the `pypimdoc` module -->
<!-- Available from [PyPi](https://pypi.org/project/pypimdoc/)  -->


#### <a id="eval1"></a>MD-macro `eval`

```python
eval(code: str) -> str
```

*Insert the text output of the Python code*

Insert the text output of the Python code evaluated in the
name space of the module and the MD-macros’ local name space.

**Arguments/return value:**

`code`: The Python code to evaluate

`returns`: The resulting text


<!-- This documentation is generate using the `pypimdoc` module -->
<!-- Available from [PyPi](https://pypi.org/project/pypimdoc/)  -->


#### <a id="code1"></a>MD-macro `code`

```python
code(code: str)
```

*Execute the code*

Execute the code to populate the MD-macros’ local name space
that later can be used in MD-macros arguments and in the code
of the MD-macro `eval`.

Arguments:


<!-- This documentation is generate using the `pypimdoc` module -->
<!-- Available from [PyPi](https://pypi.org/project/pypimdoc/)  -->


#### <a id="cmd1"></a>MD-macro `cmd`

```python
cmd(cmd: str) -> str
```

*Insert the text output of the command*

Insert the text output of the (shell) command.

**Arguments/return value:**

`cmd`: The shell command

`returns`: The output of the command


<!-- This documentation is generate using the `pypimdoc` module -->
<!-- Available from [PyPi](https://pypi.org/project/pypimdoc/)  -->


#### <a id="cmd_cb1"></a>MD-macro `cmd_cb`

```python
cmd_cb(cmd: str) -> str
```

*Insert the text output of the command as a code block*

Insert the text output of the (shell) command as a code block.

**Arguments/return value:**

`cmd`: The shell command

`returns`: The output of the command in a code block


<!-- This documentation is generate using the `pypimdoc` module -->
<!-- Available from [PyPi](https://pypi.org/project/pypimdoc/)  -->


#### <a id="help1"></a>MD-macro `help`

```python
help(cmd: str = '', sub_cmd: str = '', title: str = '', hlevel: int = 0, hid: str = '', no_toc: bool = False) -> str
```

*Insert the output from a help command*

Insert the output from a help command reformatted as markdown.
The output of the help command is expected to be formated as
the Python module `argparse` formats the help text.

**Arguments/return value:**

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


<!-- This documentation is generate using the `pypimdoc` module -->
<!-- Available from [PyPi](https://pypi.org/project/pypimdoc/)  -->


#### <a id="for_in1"></a>MD-macro `for_in`

```python
for_in(loop_var: str, loop_list: str, loop_body: str) -> str
```

*Loop through a list of documentation elements*

Loop documentation




### <a id="Help+functions+for+t"></a>Help functions for the MD-macros

The module also provides some functions avilable in the name space
where the MD-macros are executed. These fuctions can be used in the
arguments of MD-macros. In addition to the help functions documented
below, the two MD-macros [`eval`](#eval1) and [`cmd`](#cmd1) are also
available in the name space where the MD-macros are executed (and can
be used in arguments to other MD-macros).

The following help functions are provided:

<!-- This documentation is generate using the `pypimdoc` module -->
<!-- Available from [PyPi](https://pypi.org/project/pypimdoc/)  -->


#### <a id="mdoc_body1"></a>Help function `mdoc_body`

```python
mdoc_body(obj: object | None = None) -> str
```

*The body of the documentation string of an object*

The body of the documentation string, meaning the
documentation string except the title (the first line) and the
empty line between the between the title and the body. The
function takes one optional argument, the object to get the
documentation string from. If no argument is given, the
documentation string of the module is used.

**Arguments/return value:**

`obj`: The object to get the documentation string body from
(default `None`, meaning get the documentation string body of
the module)

`returns`: The documentation string body of the object


<!-- This documentation is generate using the `pypimdoc` module -->
<!-- Available from [PyPi](https://pypi.org/project/pypimdoc/)  -->


#### <a id="mdoc_doc1"></a>Help function `mdoc_doc`

```python
mdoc_doc(obj: object | None = None) -> str
```

*The documentation string of an object*

The fuction returns the complete documentation string of the
object, including the title (the first line), the following
empty line and the body. The function takes one optional
argument, the object to get the documentation string from. If
no argument is given, the documentation string of the module
is used.

**Arguments/return value:**

`obj`: The object to get the documentation string from
(default `None`, meaning get the documentation string of the
module)

`returns`: The documentation string of the object


<!-- This documentation is generate using the `pypimdoc` module -->
<!-- Available from [PyPi](https://pypi.org/project/pypimdoc/)  -->


#### <a id="mdoc_title1"></a>Help function `mdoc_title`

```python
mdoc_title(obj: object | None = None) -> str
```

*The title of the documentation string of an object*

A function returning the first line of documentation string,
often considered the title of the documentation string. This
only succeeds if the first line is followed by an empty
line. The function takes one optional argument, the object to
get the documentation string from. If no argument is given,
the documentation string of the module is used.

**Arguments/return value:**

`obj`: The object to get the documentation string title from
(default `None`, meaning get the documentation string title of
the module)

`returns`: The documentation string title of the object




### <a id="To+use+the+module+as"></a>To use the module as a console script


#### <a id="Command+%60pypimdoc%60"></a>Command `pypimdoc`


*A Python module for generating Python module documentation*

**Usage:**

```bash
pypimdoc [-h] [-V] [-t TEMPLATE] [-o OUTFILE] [-l BASE_HEADING_LEVEL] [-i] [-n NAME] PYSRC
```

**Positional arguments:**

Name | Description
---- | -----------
`PYSRC` | module source code file

**Options:**

Name | Description
---- | -----------
`-h, --help` | show this help message and exit
`-V, --version` | show program's version number and exit
`-t, --template TEMPLATE` | markdown template (default `README.template`)
`-o, --outfile OUTFILE` | output file (default stdout)
`-l, --base-heading-level BASE_HEADING_LEVEL` | base (start) level of headings (default 1, like `<h1></h1>` in HTML)
`-i, --inline-md-macros` | MD-macros are inline in the markdown template (and not inside HTML-comments)
`-n, --name NAME` | name of module (default source code filename without `.py`)


### <a id="pypimdoc1"></a>Class `PyPiMDoc`

*The Python module documentation class*

The class implementing the different MD-macros used in the
markdown template for the documentation of a Python module.

The most common usage of the module is as a console script.  As a
consequence, the users of the module seldom need to use this class
themselves.



#### <a id="Initialize+%60PyPiMDoc"></a>Initialize `PyPiMDoc`

```python
PyPiMDoc(filename: str, name: str = '', base_heading_level: int = 1, toc_begin: int = 1, toc_end: int = 3)
```

*Initialize a Python module documentation object*

Initialize a Python module documentation object, including
loading the Python module (Python source code) and prepare the
document generation.

**Arguments:**

`filename`: The file name of the module to document

`name`: The name of the module (default generated from the
`filename`)

`base_heading_level`: All generated headings are at this level
or above (default 1)

`toc_begin`: Include items in table of contents from this
level (relative to `base_heading_level`, default 1)

`toc_end`: Include items in table of contents to this level
(relative to `base_heading_level`, default 2)




#### <a id="pypimdoc.process_ma1"></a>Method `PyPiMDoc.process_macro`

```python
process_macro(macro_name: str, args_str: str) -> str
```

*Process a MD-macro*

Process a MD-macro with the given name and arguments.

**Arguments/return value:**

`macro_name`: MD-macro name

`args_str`: the arguments to the MD-macro as a string

`returns`: returns the documentation part generated by the MD-macro




#### <a id="pypimdoc.process_te1"></a>Method `PyPiMDoc.process_template`

```python
process_template(template: io.TextIOBase, macro_types: str = 'block') -> str
```

*Read and process template*

The template file is the driver of the document generation. In
its simplest form, the template is a markdown document that
becomes the module documentation. The template includes some
special commands (MD-macros) used to fetch documentation from
the module (including the documentation strings in the
module).

**Arguments/return value:**

`template`: The README template file

`macro_types`: Either `"block"` or `"inline"`, where
`"block"` means that the MD-macros are inside HTML comment
blocks and `"inline"` means that MD-macros are directly
inline in the markdown documentation strings (default
`"block"`)

`returns`: The processed markdown README file content





