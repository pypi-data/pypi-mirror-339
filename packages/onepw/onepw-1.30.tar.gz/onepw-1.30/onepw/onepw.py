#!/usr/bin/env python3

###############################################################################
#
# Copyright (c) 2022-2025, Anders Andersen, UiT The Arctic University
# of Norway. All rights reserved.
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


R"""The `onepw` Python module for 1Password integration

The `onepw` Python module implements a limited *1Password* integration
using *1Password CLI*:

 - https://developer.1password.com/docs/cli

To use the module, install the *1Password CLI* tool `op`:

 - https://1password.com/downloads/command-line/

(or install it with a package tool, e.g.,
*[HomeBrew](https://brew.sh)* on a Mac).

The `onepw` module is available from my software repository and from
PyPi:

 - https://www.pg12.org/software

 - https://pypi.org/project/onepw/

It is best to install the module and the companion console script
`onepw` with `pip`:

```bash
pip install onepw
```

It is recommended to integrated the *1Password CLI* tool with the
*1Password* desktop app (to use the desktop app to authenticate). See
Step 2 here for details:

 - https://developer.1password.com/docs/cli/get-started/

## Alternative 1Password modules

Other similar Python modules, with overlapping, extended or different
functionality, are available. The obvious first choice is the SDKs
from *1Password*:

 - https://developer.1password.com/docs/sdks/

Their Python SDK is in active development and should be considered
when integrating *1Password* with Python:

 - https://github.com/1Password/onepassword-sdk-python

Another option is to use the `keyring` module with the third-party
backend *OnePassword Keyring*:

 - https://pypi.org/project/keyring/

 - https://pypi.org/project/onepassword-keyring/

One downside of this approach is that when *OnePassword Keyring*
backend is installed, it replaces the default backend of the `keyring`
module. I prefer that the default behavior of `keyring` is unchanged
(using the system keychain/keyring) and use a specific module (like
`onepw`) for *1Password* integration in Python.

## Compatability notice

Version 1.22 of `onepw` introduces a *non-backwards compatible*
change. From version 1.22 of `onepw`, the return value format of the
method `get` has changed when the `field` argument has the value
`"all"` (or `True`). In this case, the returned dictionary only
includes the fields (and not other information about the 1Password
entry). To get more data about the 1Password entry, you now have to
use the new `info` argument of the `get` method.

In version 1.22, the console script command `onepw get` also has some
argument changes. The `--title` argument is replaced by the positional
argument `TITLE-OR-ID` and the `--field` and `--info` arguements are
updated to match the changes of the `get` method. The old usage of
`--title` instead of `TITLE-OR-ID` will still work but is not
documented in newer versions.

"""


# Use subprocess to perform the command line operations
import subprocess


# The 1Password command line program `op` uses JSON
import json


# Use `shutil.which()` to verify that the 1Password CLI is installed
import shutil


# When adding entries to 1Password, store it in a temporary file first
import tempfile


# Current version of module
version = "1.30"

# The commands implemented
cmds = ["get", "list", "read", "add", "delete"]


# On a Mac, the 1Password `op` tool is installed in "/usr/local/bin/"
# or "/opt/homebrew/bin/" (with HomeBrew)
op_path = ""	# We guess full path is not necessary (test: `shutil.which()`)
op_cmd = op_path + "op"


def _fetch_fields_op(field_list: list, what: str = "value") -> dict:
    R"""Fetch all fields of given type

    Fetch all fields from the field list in a dictionary where either
    `"id"` or `"label"` is the key for each field and either `"value"`
    or `"href"` is the value of each field.

    `field_list` -- a list of information for each field

    `return` -- a dictionary with field key-value pairs

    """
    fields = {}
    for v in field_list:
        for k in ["id", "label"]:
            if k in v and v[k]:
                if not v[k] in fields:
                    if what in v:
                        fields[v[k]] = v[what]
                break
        else:
            if what in v:
                if what in fields:
                    num += 1
                    fields[f"{what}{num}"] = v[what]
                else:
                    num = 0
                    fields[what] = v[what]
    return fields


class OnePWError(Exception):
    R"""Any error in the 1Password session"""
    def __init__(self, errmsg: str):
        self.errmsg = errmsg


class OnePW:
    R"""A Python class for 1Password sessions

    When an instance of this class is created, a *1Password* session
    is started.  With this session you can perform *1Password CLI*
    commands. The following methods for such commands are available:

     - `get`: get a field from a 1Password entry

     - `list`: list all entries from 1Password

     - `add`: add an entry to 1Password
    
     - `delete`: delete an entry from 1Password

     - `read`: read the value from a 1Password reference
    
    In the following example, a *1Password* session is created and the
    password from the `"An example"` entry in 1Password is fetched:

    ```python
    import onepw
    op = onepw.OnePW()
    pw = op.get("An example", field="password")
    ```

    In the next example, a new entry with the title `"A new example"`
    is created and an entry with the title `"An example"` is deleted:

    ```python
    import onepw
    from secrets import token_urlsafe
    op = onepw.OnePW()
    op.add("A new example", username="a@user.name", password=token_urlsafe(12))
    op.delete("An example")
    ```

    The `read` command is similar to the `get` command, but instead of
    a title of a field, we provide a [1Password secret reference](https://developer.1password.com/docs/cli/secret-reference-syntax/).
    In this example the `read` command returns a value matching the
    1Password secret reference `"op://Personal/Example/Passwd"`:

    ```python
    import onepw
    op = onepw.OnePW()
    pw = op.read("op://Personal/Example/Passwd")
    ```

    In the final example, all 1Password entries with duplicated titles
    are printed with their titles and all ids matching that title:

    ```python
    # Start 1Password session
    import onepw
    op = onepw.OnePW()

    # Get all 1Password entries as a list of id-title tuples
    l = op.list(return_format="id-title")

    # Create a new list only with the titles
    lt = [t for i, t in l]

    # Create a dictionary with all duplicated titles, where the titles
    # are keys and a list of entry ids with that title are the values
    dup = {t: [j for j, u in l if u == t] for i, t in l if lt.count(t) > 1}

    # Print out duplicated titles and the ids of their entries
    for t in dup:
        print(f"{t}: {','.join(dup[t])}")
    ```

    This is an example of what this code could print out, where each
    line is an entry title followed by a colon and multiple entry ids
    separated by commas (one for each duplicate with this title):

    ```python
    An Entry: auniqu4idfrom1p4ssw0rdapp1,4uni9ueidfromlpa22wordit3m
    Another Entry: auniqueidfrom1password1tem,aun19u316from16asswordapp9
    ```

    """


    def __init__(self, account: str | None = None, pw: str | None = None):
        R"""Instantiate a 1Password session

        When a *1Password* session is instantiated you are signed in
        to *1Password*. If the *1Password CLI* tool is integrated with
        the *1Password* desktop app, the desktop app is used to sign
        in to *1Password*. Otherwise, the password has to be provided,
        either as the argument `pw` (usually not recommended) or
        prompted for.

        Arguments:

        `account` -- The account to sign in to (usually, not needed;
        default `None`)

        `pw` -- The password used to sign in (usually, not needed;
        default `None`)

        """

        # Save for error messages
        self._last = "__init__"

        # Verify that the 1Password command `op` is installed
        if not shutil.which(op_cmd):
            errmsg = "\nInstall (and initialize) the 'op' command from " + \
                "1Password:\n" + \
                "  https://1password.com/downloads/command-line\n"
            raise OnePWError(errmsg)
        
        # Login (new session)
        if account:
            cmd =  [op_cmd, "signin", "--account", account, "--raw"]
        else:
            cmd =  [op_cmd, "signin", "--raw"]
        if pw:
            res = subprocess.run(
                cmd, input=pw, text=True, capture_output=True)
        else:
            res = subprocess.run(
                cmd, text=True, capture_output=True)
        if res.returncode != 0:
            errmsg = "1Password signin failed (error-code: " + \
                f"{res.returncode})\n  {res.stderr.strip()}"
            raise OnePWError(errmsg)

        # Save session token (empty if 1Password 8 CLI integration enabled)
        self.session_token = res.stdout.rstrip()


    def get(self,
            title: str,
            field: bool | str = False,
            info: bool | str = False,
            vault: str | None = None,
            return_format: str | None = None) -> str | dict:
        R"""Get a field from a 1Password entry

        Get the value of a field or other information from the
        1Password entry with the title or id `title`.  When using the
        method you should either use the `field` or the `info`
        argument (and not both at the same time). If `field` or `info`
        is not given, the value of the `"password"` field of the
        1Password entry is returned.

        When a specific field is specified, like `"username"`,
        `"password"` or `"email"`, the value of that specific field is
        returned (a text string). If `field` is set to `"all"` or
        `True`, a dictionary with all fields are returned. If `field`
        is `True` or `"all"`, and `return_format` *is not* set, the
        returned dictionary will have a format like this (numbers of
        items in the dictionary will vary):
        
        ```python
        {
          "username": "an@email.address",
          "password": "a s3cret p4ssw0rd"
        }
        ```

        It is possible to get a 1Password reference to the field(s)
        instead of the value(s). Set the `return_format` argument to
        `"reference"` to achieve this. This will work both when
        `field` is `True` or `"all"`, and when `field` spcecifies a
        specific field in the 1Password entry.

        If `field` is `False` and `info` is not `False`, information
        about the 1Password entry (and not the fields) is returned. If
        `info` is `True` or `"all"`, a dictionary with information
        about the entry, including id, title and more, is returned. If
        `info` is a text string, the specific information identified
        by this text string (key) is returned. If `field` is `False`
        and `info` is `True` or `"all"`, and `return_format` *is not*
        not set, the returned dictionary will have a format like this
        (numbers of items in the `"urls"` section will vary):
        
        ```python
        {
          "id": "auniqu4idfrom1p4ssw0rdapp1",
          "title": "An example",
          "vault": "Personal",
          "category": "LOGIN",
          "urls": {
            "website": "https://a.web.page/"
          }
        }
        ```

        If the `info` argument is `True` or `"all"` and the
        `return_format` argument is `"raw-dict"`, the raw dictionary
        containing all the details about the entry is returned
        (including all the fields and a much more).

        The `get` method raises a `OnePWError` exception if an entry
        with the given title and/or field/info is not found.
        
        Arguments/return value:

        `title` -- The title of the entry (can also be the id of the
        entry)

        `field` -- The field to get from the entry, where `True` or
        `"all"` will return all fields as a dictionary (default
        `False`, meaning that the `"password"` field of the entry is
        returned if `info` is `False`, too)

        `info` -- Get information about the entry, where `True` or
        `"all"` will return all information as a dictionary (default
        `False`)

        `vault` -- Look for entry in this vault (default `None`,
        meaning every vault)

        `return_format` -- Specifies an alternative format to the
        returned field/data from the entry (default `None`)

        `return` -- The value of field(s) in the entry or information
        about the entry

        """

        # Save for error messages
        self._last = "get"

        # Default is to get the "password" field
        if not field and not info:
            field = "password"

        # Build command
        cmd = [op_cmd, "--session", self.session_token, "item",
               "get", title, "--reveal"]
        if vault:
            cmd += ["--vault", vault]
        if type(field) is str and field != "all":
            cmd += ["--fields", field]
            if return_format == "reference":
                cmd += ["--format", "json"]
        else:
            cmd += ["--format", "json"]
        
        # Get entry for item from 1Password
        res = subprocess.run(cmd, text=True, capture_output=True)
        if res.returncode != 0:
            if field:
                if type(field) is str and field != "all":
                    what = f"field '{field}'"
                else:
                    what = "all fields"
            else:
                if type(info) is str and info != "all":
                    what = f"info '{info}'"
                else:
                    what = "all info"
            errmsg = f"Fetching {what} for entry '{title}' from 1Password " + \
                f"failed:\n  {res.stderr.strip()}"
            raise OnePWError(errmsg)
        
        # Decode the entry

        # Fetch return string
        value = res.stdout.rstrip()

        # Return all fields
        if field == True or field == "all":

            # Convert to Python dictionary
            value = json.loads(value)

            # Try to find all real fields of interest
            if "fields" in value:
                if return_format == "reference":
                    value = _fetch_fields_op(value["fields"], "reference")
                else:
                    value = _fetch_fields_op(value["fields"], "value")
            else:
                value = {}

        # Return a specific field
        elif field:

            # Returne reference to specific field instead of its value
            if return_format == "reference":
            
                # Convert to Python dictionary
                value = json.loads(value)

                # Get the reference
                if "reference" in value:
                    value = value["reference"]
                else:
                    errmsg = f"No reference for field '{field}' in " + \
                        f"1Password for entry '{title}'"
                    raise OnePWError(errmsg)
            
            # Return value of specific field
            else:            
                if not value:
                    errmsg = f"No field '{field}' in 1Password for entry " + \
                        f"'{title}'"
                    raise OnePWError(errmsg)

                
        # Return all information about the entry
        elif info == True or info == "all":

            # Convert to Python dictionary
            value = json.loads(value)

            # If "raw-json", no further decoding needed
            if return_format != "raw-dict":

                # Create a new return value fetching the values we want
                new = {}
                new["id"] = value["id"]
                new["title"] = value["title"]
                new["vault"] = value["vault"]["name"]
                new["category"] = value["category"]

                # Try to find all real urls of interest
                if "urls" in value:
                    new["urls"] = _fetch_fields_op(
                        value["urls"], "href")
                else:
                    new["urls"] = {}

                # The result (convert to JSON, if requested)
                value = new

        # Return specific info
        elif info:

            # Convert to Python dictionary
            value = json.loads(value)

            # Get the info
            if info in value:
                if info == "urls":
                    value = _fetch_fields_op(value["urls"], "href")
                else:
                    value = value[info]

            # Info not found
            else:
                errmsg = f"Specific info '{info}' not found in 1Password " + \
                    f"entry '{title}'"
                raise OnePWError(errmsg)

        # Return the value
        return value


    def list(self,
             categories: str | None = None,
             favorite: bool = False,
             tags: str | None = None,
             vault: str | None = None,
             return_format: str = "title") -> list | dict:
        R"""List all entries in 1Password

        List all the entries in 1Password with their titles, ids or as
        a dictionary representation.  By default, the method returns a
        list of all entry titles.

        If `return_format` is set to `"id"`, it returns a list of all
        entry ids. If `return_format` is set to `"title-id"`, it
        returns a list of all entries where each entry in the list is
        a title-id tuple. If `return_format` is set to `"id-title"`,
        it returns a list of all entries where each entry in the list
        is a id-title tuple.

        If `return_format` is set to `"dict"` or `"id-dict"`, it
        returns a dictionary of all entries and some data, where the
        key for each entry is the title (if `return_format` is
        `"dict"`) or the id (if `return_format` is `"id-dict"`) of the
        entry.

        If `return_format` is set to `"raw-dict"` or `"id-raw-dict"`,
        it returns a dictionary of all entries and all the details
        about each entry, where the key for each entry is the title
        (if `return_format` is `"raw-dict"`) or the id (if
        `return_format` is `"id-raw-dict"`) of the entry.

        Be aware that in the case where the argument `return_format`
        is `"dict"` or `"raw-dict"` and two or more entries have the
        same title, only one of them will be in the returned
        dictionary.

        Arguments/return value:

        `categories` -- only list items in these comma-separated
        categories (default `None`, meaning all entries)

        `favorite` -- only list favorite items (default `False`,
        meaning all entries)

        `tags` -- only list items with these comma-separated tags
        (default `None`, meaning all entries)

        `vault` -- only list items in this vault (default `None`,
        meaning all vaults)

        `return_format` -- the return format of the returned list or
        dictionary (default `"title"`, meaning a list of entry titles)

        `return` -- returns a list or a dictionary with all the
        entries

        """

        # Save for error messages
        self._last = "list"

        # Build command
        cmd = [op_cmd, "--session", self.session_token, "item", "list",
               "--format", "json"]
        if categories:
            cmd += ["--categories", categories]
        if favorite:
            cmd += ["--favorite"]
        if tags:
            cmd += ["--tags", tags]
        if vault:
            cmd += ["--vault", vault]
        
        # Get entries from 1Password
        res = subprocess.run(cmd, text=True, capture_output=True)
        if res.returncode != 0:
            errmsg = f"List entries from 1Password failed:\n" + \
                f"  {res.stderr.strip()}"
            raise OnePWError(errmsg)

        # The result dictionary
        value = json.loads(res.stdout.strip())

        # Id or title as key?
        if "id" in return_format:
            key = "id"
        else:
            key = "title"

        # Return list of titles or ids or combinations
        if return_format == "title-id":
            return [(e["title"], e["id"]) for e in value]
        elif return_format == "id-title":
            return [(e["id"], e["title"]) for e in value]
        elif return_format in ["title", "id"]:
            return [e[key] for e in value]

        # Return a dictionary with an item for each 1Password entry
        elif return_format in ["dict", "id-dict"]:
            return {
                e[key]: {
                    "id": e["id"],
                    "title": e["title"],
                    "vault": e["vault"]["name"],
                    "category": e["category"],
                    "urls": _fetch_fields_op(
                        e["urls"], "href") if "urls" in e else {}
                } for e in value
            }
        elif return_format in ["raw-dict", "id-raw-dict"]:
            return {e[key]: e for e in value}

        # Unknown `return_format`
        else:
            errmsg = f"List entries from 1Password failed: " + \
                f"unknown return format '{return_format}'"
            raise OnePWError(errmsg)


    def read(self, reference: str) -> str:
        R"""Read value of an entry field by reference

        Return the value of the entry field given by a 1Password
        reference. The following is an example of such a reference:

        ```
        op://Personal/Example/Passwd
        ```

        Arguments/return value:

        `reference` -- 1Password reference to a field in an entry

        `return` -- The value of the field

        """

        # Save for error messages
        self._last = "read"

        # Build command
        cmd = [op_cmd, "--session", self.session_token, "read", reference]
        
        # Get the field from 1Password
        res = subprocess.run(cmd, text=True, capture_output=True)
        if res.returncode != 0:
            errmsg = f"Read field {reference} from 1Password failed:\n" + \
                f"  {res.stderr.strip()}"
            raise OnePWError(errmsg)

        # The result value
        value = res.stdout.strip()

        # Did we get a value
        if not value:
            errmsg = f"Read field {reference} from 1Password returned " + \
                f"no value:\n  {res.stderr.strip()}"
            raise OnePWError(errmsg)

        # Return value
        return value


    def add(
            self, title: str, username: str, password: str,
            email: str | None = None, url: str | None = None):
        R"""Add a new entry to 1Password

        Add a new entry to 1Password with the provided values. A
        title, username and password are required. The method raises a
        `OnePWError` exception if adding the entry fails.

        Arguments:

        `title` -- The title of the entry

        `username` -- The username added to the entry

        `password` -- The password added to the entry

        `email` -- The email address added to the entry (default `None`)
        
        `url` -- The URL added to the entry (default `None`)

        """

        # Save for error messages
        self._last = "add"
        
        # Get template for new entry
        res = subprocess.run(
            [op_cmd, "--session", self.session_token,
             "item", "template", "get", "Login"],
            text=True, capture_output=True)
        if res.returncode != 0:
            errmsg = "Fetching template for 'Login' from 1Password " + \
                f"failed:\n  {res.stderr.strip()}"
            raise OnePWError(errmsg)

        # Fill in the form with username and password
        try:
            template = json.loads(res.stdout.rstrip())
            for field in template["fields"]:
                if field["id"] == "username":
                    field["value"] = username
                elif field["id"] == "password":
                    field["value"] = password
        except KeyError:
            errmsg = "Error in 1Password template?"
            raise OnePWError(errmsg)
        except:
            errmsg = "Unable to parse template output from 1Password"
            raise OnePWError(errmsg)

        # Add email if provided
        if email:
            template["fields"].append(
                {"id": "email", "label": "email", "purpose": "EMAIL",
                 "value": email, "type": "STRING"})

        # Add entry to 1Password via a temp json file
        with tempfile.NamedTemporaryFile(mode="w") as tmp:

            # Dump the json to a temp file
            json.dump(template, tmp)
            tmp.seek(0) # Go back to beginning of file

            # Create the `op` command
            cmd = [op_cmd, "--session", self.session_token,
                   "item", "create", "--template", tmp.name,
                   "--title", f"{title}"]
            if url:
                cmd.append("--url")        
                cmd.append(f"{url}")        

            # Actually add entry to 1Password
            res = subprocess.run(cmd, text=True, capture_output=True)

        # Did it go OK?
        if res.returncode != 0:
            errmsg = f"Adding entry in 1Password for '{title}' " + \
                f"failed:\n  {res.stderr.strip()}"
            raise OnePWError(errmsg)


    def delete(self, title: str, no_archive: bool = False):
        R"""Delete an entry from 1Password

        Delete an entry from 1Password with the given title. 

        Arguments:

        `title` -- The title of the entry to delete

        `no_archive` -- Do not archive entry when deleted (default
        `False`)

        """

        # Save for error messages
        self._last = "delete"

        # Build command
        cmd = [op_cmd, "--session", self.session_token,
               "item", "delete", title]
        if not no_archive:
            cmd.append("--archive")

        # Delete entry
        res = subprocess.run(cmd, text=True, capture_output=True)
        if res.returncode != 0:
            errmsg = f"Deleting entry '{title}' from 1Password failed:\n" + \
                f"  {res.stderr.strip()}"
            raise OnePWError(errmsg)


def d2na(kw: dict, sep: str = " ", pre: str = "--", asg: str = " ") -> str:
    R"""Convert dictionary to string representation of named arguments

    A simple help function converting a dictionary to a string
    representation of arguments.  It is possible to modify the
    separator `sep`, the pre-string before the name `pre`, and the
    asignment string `asg`.  The default values are matching command
    line arguments.

    Arguments/return value:

    `sep` -- Separator between each name/value pair (`sep`, default
    " ", but ", " is an alternative for named arguments to Python
    functions)

    `pre` -- A string added before the name of each argument (default
    "--", but '"' is an alternative for named arguments to Python
    functions)

    `asg` -- The string for assignment of the value to the named
    argument (default " ", but "=" is an alternative for named
    arguments to Python functions)

    `return` -- The string representation

    """
    na_str_list = []
    for k in kw:
        na_str_list.append(f"{pre}{k}{asg}{repr(kw[k])}")
    return sep.join(na_str_list)


def _print_sig(cmd: str, name: str | None = None):
    R"""Print the method signature

    Print the method signature of the method named `cmd` in the
    `OnePW` class.

    Arguments:

    `cmd` -- Name of the method to print the signature of

    """
    from inspect import signature
    method = getattr(OnePW, cmd)
    if not name: name = method.__name__
    sig = str(signature(method))
    if ", " in sig:
        sig = sig.replace("self, ", "", 1)
    else:
         sig = sig.replace("self", "", 1)
    print(f"{name}{sig}")


def _print_doc(method: str | list | None = None, prog: str = "onepw"):
    R"""Print the documentation of a single method or a list of methods

    Print the method documentation of the method named `method` in the
    `OnePW` class. If `method` is a list of method names, print the
    documention of the module, the `OnePW` class, and all the
    methods. If `method` is `None`, only print the documention of the
    module and the `OnePW` class.

    Arguments:

    `method` -- Name of a method, a list of method names, or `None` for
    no specific method

    """

    # Print documention for a single method
    if type(method) is str:
        m = getattr(OnePW, method)
        print(f"\n\033[1mMethod '{method}'\033[0m:\n")
        _print_sig(method)
        print("\n" + m.__doc__.strip() + "\n")

    # Print documention for the module
    else:

        # Print the module documention
        print(f"\n\033[1mModule 'onepw'\033[0m:\n")
        print(__doc__.strip() + "\n")

        # Print the class `OnePW` documention
        print(f"\033[1mClass 'OnePW'\033[0m:\n")
        _print_sig("__init__", "OnePW")
        print("\n" + OnePW.__doc__.strip() + "\n")
        init_doc_lines = OnePW.__init__.__doc__.strip().splitlines()[2:]
        print("\n".join(init_doc_lines) + "\n")

        # Print information about the list of methods
        if type(method) is list:
            print(f"\033[1mClass 'OnePW' methods\033[0m:\n")
            for m in method:
                print(f"\033[1m{m}\033[0m: {prog} --doc {m}\n")

    
def main():
    R"""Run module as a program

    Run the module as a program with these possible commands:

    - `get`: get the value of a field in an entry in 1Password (default
      field is password)

    - `list`: list all entries in 1Password

    - `add`: add an entry in 1Password

    - `delete`: delete an entry from 1Password

    """

    # Need `argv`, `stderr` and `exit`
    import sys

    # Help variables
    methods = cmds
    cmdchoices = "{" + ",".join(cmds) + "}"
    infokeys = ["id", "title", "vault", "category", "urls"]
    infochoices = ", ".join(infokeys)
    
    # A trick for a late binding of args.func (after the creation of
    # the 1Password session)
    method_dict = {}  # Will be populated with a method for each command
    get_func = lambda **kw: method_dict["get"](**kw)
    list_func = lambda **kw: method_dict["list"](**kw)
    read_func = lambda **kw: method_dict["read"](**kw)
    add_func = lambda **kw: method_dict["add"](**kw)
    delete_func = lambda **kw: method_dict["delete"](**kw)
    
    # Create overall argument parser
    import argparse
    parser = argparse.ArgumentParser(
        description="perform 1Password CLI commands",
        epilog=f"use '%(prog)s {cmdchoices} -h' " + \
          "to show help message for a specific command")
    parser.add_argument(
        "-V", "--version", action="version",
        version=f"%(prog)s " + version)
    parser.add_argument(
        "--doc", nargs='?', const=True, choices=methods,
        default=argparse.SUPPRESS, 
        help="print documentation of module or specific method")
    parser.add_argument(
        "-D", action="store_true", default=argparse.SUPPRESS, 
        help=argparse.SUPPRESS)
    parser.add_argument(
        "-L", action="store_true", default=argparse.SUPPRESS, 
        help=argparse.SUPPRESS)
    parser.add_argument(
        "-l", action="store_true", default=argparse.SUPPRESS, 
        help=argparse.SUPPRESS)
    parser.add_argument(
        "-M", nargs='?', const=True, choices=methods + ["OnePW"],
        default=argparse.SUPPRESS,
        help=argparse.SUPPRESS)
    parser.add_argument(
        "--account", default=None,
        help="the 1Password account (usually, not necessary)")
    parser.add_argument(
        "--pw", metavar="PASSWORD", default=None,
        help="the 1Password secret password (be careful using this)")
    subparsers = parser.add_subparsers(
        help="the command to perform")

    # Create argument parser for the `get` command
    parser_get = subparsers.add_parser(
        "get",
        description="get the value of a field from an entry in 1Password")
    arg_title_or_id = parser_get.add_argument(
        "title_or_id", metavar="TITLE-OR-ID",
        help="the title or id of the entry to get the value from")
    arg_title = parser_get.add_argument(
        "--title", help=argparse.SUPPRESS)
    parser_get.add_argument(
        "--field", nargs='?', const=True, default=False,
        help="the field of the entry to get the value from, or if 'all', " + \
          "return all fields in a JSON string (default 'password')")
    parser_get.add_argument(
        "--info", nargs='?', const=True, choices=infokeys, default=False,
        help="get information about the entry, instead of the value of a " + \
        f"field (it is possible to specify what info: {infochoices})")
    parser_get.add_argument(
        "--reference", action="store_true", dest="ref",
        default=argparse.SUPPRESS,
        help="get reference to field, not value")
    parser_get.set_defaults(func=get_func)

    # Create argument parser for the `list` command
    parser_list = subparsers.add_parser(
        "list",
        description="list all entries in 1Password")
    parser_list.add_argument(
        "--categories", default=argparse.SUPPRESS,
        help="only list items in these categories (comma-separated)")
    parser_list.add_argument(
        "--favorite", action="store_true", default=argparse.SUPPRESS,
        help="only list favorite items")
    parser_list.add_argument(
        "--tags", default=argparse.SUPPRESS,
        help="only list items with these tags (comma-separated)")
    parser_list.add_argument(
        "--vault", default=argparse.SUPPRESS,
        help="only list items in this vault")
    parser_list.set_defaults(func=list_func)

    # Create argument parser for the `read` command
    parser_read = subparsers.add_parser(
        "read",
        description="read the value from a 1Password reference")
    parser_read.add_argument(
        "reference", metavar="REFERENCE",
        help="the reference to a field in a 1Pasword entry")
    parser_read.set_defaults(func=read_func)

    # Create argument parser for the `add` command
    parser_add = subparsers.add_parser(
        "add", description='add an entry to 1Password')
    parser_add.add_argument(
        "--title", required=True,
        help="the title of the new entry")
    parser_add.add_argument(
        "--username", required=True,
        help="the user name in the new entry")
    parser_add.add_argument(
        "--password",
        help="the password in the new entry " + \
          "('%(prog)s' will ask for the password if it is not provided)")
    parser_add.add_argument(
        "--email", default=None,
        help="the email address in the new entry (optional)")
    parser_add.add_argument(
        "--url", default=None,
        help="the URL in the new entry (optional)")
    parser_add.set_defaults(func=add_func)

    # Create argument parser for the `delete` command
    parser_delete = subparsers.add_parser(
        "delete",
        description="delete an entry from 1Password")
    parser_delete.add_argument(
        "--title", required=True,
        help="the title of the entry to delete")
    parser_delete.add_argument(
        "--no-confirm", action="store_true",
        help="do not confirm before deleting entry (default `False`)")
    parser_delete.add_argument(
        "--no-archive", action="store_true",
        help="do not archive deleted entry (default `False`)")
    parser_delete.set_defaults(func=delete_func)

    # If old syntax with "--title" is used, update the argument parser
    if "--title" in sys.argv:
        arg_title.required = True
        arg_title.help = arg_title_or_id.help
        arg_title_or_id.help = argparse.SUPPRESS
        arg_title_or_id.default = argparse.SUPPRESS
        arg_title_or_id.nargs = 0
    
    # Parse arguments
    args = parser.parse_args()

    # Print documentation?
    if "doc" in args:
        if args.doc == True:
            _print_doc(cmds, sys.argv[0])
        else:
            _print_doc(args.doc)
        return

    # Print alternative (non-documented) documentation?
    if "D" in args:
        _print_doc()
        return

    # Print the available methods
    if "L" in args or "l" in args:
        if "L" in args:
            print("\n".join(cmds))
        else:
            print(repr(cmds))
        return
    
    # Print list of commands (non-documented)?
    if "M" in args:
        if args.M == True:
            print("\n".join(methods))
        elif args.M == "OnePW":
            _print_sig("__init__", args.M)
        else:
            _print_sig(args.M)
        return

    # If we have a password without a value in arguments, we ask for it
    if "password" in args:
        if not args.password:
            from getpass import getpass
            args.password = getpass()

    # Arguments are passed on to the methods; make them a dictionary
    kw = vars(args)

    # The `title_or_id` argument is converted to `title`
    if "title_or_id" in args:
        title_or_id = kw.pop("title_or_id")
        if title_or_id:
            args.title = title_or_id

    # Confirm?
    if "no_confirm" in args:
        no_confirm = kw.pop("no_confirm")
        if not no_confirm:
            response = input(
                f"Are you sure you want to delete entry '{args.title}' " + \
                "from 1Password? (yes/no) ")
            if response != "yes":
                return

    # Reference (instead of value)
    if "ref" in args and args.ref:
        ref = kw.pop("ref")
        kw["return_format"] = "reference"
            
    # Starte the 1Password session
    account = kw.pop("account")
    pw = kw.pop("pw")
    try:
        op = OnePW(account = account, pw = pw)
    except OnePWError as e:
        print(
            f">>> {sys.argv[0]}: Unable to sign in to 1Password:\n" + \
            f"--> {e.errmsg}", file = sys.stderr)
        sys.exit(1)

    # Bind methods to the commands
    for m in cmds:
        method_dict[m] = getattr(op, m)

    # Fetch command
    try:
        func = kw.pop("func")
    except KeyError:
        parser.print_usage(file = sys.stderr)
        print(
            f"{sys.argv[0]}: error: no command given: {','.join(cmds)}",
            file = sys.stderr)
        sys.exit(1)
        
    # Perform command
    try:
        res = func(**kw)
    except OnePWError as e:
        print(
            f">>> {sys.argv[0]}: Unable to do '{op._last}' command:\n" + \
            f"  {op._last} {d2na(kw)}\n" + \
            f"--> {e.errmsg}", file = sys.stderr)
        sys.exit(1)

    # Print result, if any
    if res:
        if type(res) is list:
            try:
                print("\n".join(res))
            except:
                print(json.dumps(res))
        elif type(res) is dict:
            print(json.dumps(res))
        else:
            print(res)


# Execute this module as a program
if __name__ == '__main__':
    main()
