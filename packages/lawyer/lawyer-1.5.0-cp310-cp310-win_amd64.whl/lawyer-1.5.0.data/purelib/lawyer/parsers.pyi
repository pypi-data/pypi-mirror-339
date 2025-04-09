"""parsers [`Module`].

This module contains lawyer's argument parser classes for creating
individual and grouped arguments (`singlet` and `singlets` repectively).

The `singlet` object represents a single argument object whereas the `singlets` object
as the name suggests, is a collection of `singlet` objects or other nested `singlets` objects.
The `singlet` object supports an argument pool called `reference` parameter which is by default
set to `sys.argv` but can be changed to any iterable of strings making it versatile and extensible.
The `singlet` object implements partial parsing during object creation and information such as
argument's presence in the reference, index, notation and as such.

The `singlets` object acts as a highly customized linked list data structure that efficiently
manages nested argument group structures and their help text generation automatically.

Both `singlet` and `singlets` objects support accessible attributes using square brackets.

----------------------------------------
This module is under license as follows:
----------------------------------------

MIT License
-----------

Copyright (c) 2025 Soumyo Deep Gupta

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
---------------------------- END of LICENSE ----------------------------------
"""

from typing import Literal, Generic, TypeVar, Tuple, Iterable
from typing import Any, NoReturn, TypeGuard, Union, Dict, Self
from typing import overload
import sys


default = TypeVar('default')


class singlet(Generic[default]):

    """A class to represent a single argument.
    
    This class contains parameters for a single argument to make it self sufficient.
    Creating the object itself partially parses it and performs conditional checks
    placed to determine validity. It also contains internal mechanisms to fully
    parse this particular argument and return the value(s) as intended.

    Using `str` function on this class will return -> `singlet(*notations)`.

    Few of the attributes of this class are accessible using square brackets and are
    listed in `singlet.__attrs__`. Changing any attribute after creating an instance
    will automatically call the partial parsing method again.
    """


    __attrs__: Tuple[Literal['name'], Literal['notations'], Literal['capture-type'], Literal['helptext'], Literal['default'], Literal['required'], Literal['reference'],
                     Literal['auto-help'], Literal['help-notations'], Literal['application-name'], Literal['application-version'], Literal['application-description'],
                     Literal['present'], Literal['notation'], Literal['notpresent'], Literal['index']]


    __allowed_capture_types__: Tuple[Literal['auto'], Literal['single'], Literal['boolean']]



    @overload
    def __getitem__(self, name: Literal['name'], /) -> str: ...
    @overload
    def __getitem__(self, name: Literal['notations'], /) -> Iterable[str]: ...
    @overload
    def __getitem__(self, name: Literal['capture-type'], /) -> Literal['auto', 'single', 'boolean']: ...
    @overload
    def __getitem__(self, name: Literal['helptext'], /) -> str: ...
    @overload
    def __getitem__(self, name: Literal['default'], /) -> default: ...
    @overload
    def __getitem__(self, name: Literal['required'], /) -> bool: ...
    @overload
    def __getitem__(self, name: Literal['reference'], /) -> Iterable[str]: ...
    @overload
    def __getitem__(self, name: Literal['auto-help'], /) -> bool: ...
    @overload
    def __getitem__(self, name: Literal['help-notations'], /) -> Iterable[str]: ...
    @overload
    def __getitem__(self, name: Literal['application-name'], /) -> str: ...
    @overload
    def __getitem__(self, name: Literal['application-version'], /) -> str: ...
    @overload
    def __getitem__(self, name: Literal['application-description'], /) -> str: ...
    @overload
    def __getitem__(self, name: Literal['present'], /) -> bool: ...
    @overload
    def __getitem__(self, name: Literal['notpresent'], /) -> bool: ...
    @overload
    def __getitem__(self, name: Literal['notation'], /) -> str: ...
    @overload
    def __getitem__(self, name: Literal['index'], /) -> int: ...
    @overload
    def __getitem__(self, name: Any, /) -> NoReturn: ...


    @overload
    def __setitem__(self, name: Literal['name'], value: str, /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['notations'], value: Iterable[str], /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['capture-type'], value: Literal['auto', 'single', 'boolean'], /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['helptext'], value: str, /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['default'], value: default, /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['required'], value: bool, /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['reference'], value: Iterable[str], /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['auto-help'], value: bool, /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['help-notations'], value: Iterable[str], /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['application-name'], value: str, /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['application-version'], value: str, /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['application-description'], value: str, /) -> None: ...
    @overload
    def __setitem__(self, name: str, value: Any, /) -> NoReturn: ...


    def __delitem__(self, name: str, /) -> NoReturn: ...


    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


    @staticmethod
    def __version_format_checker__(candidate) -> TypeGuard[str]:
        """Checks a candidate for valid version format such as 1.0, 1.2.0, etc."""

    @staticmethod
    def __value_in_reference__(*reference: Union[singlet, singlets], value: str) -> bool:
        """Checks if a value is defined as a notation for any of the references."""

    @staticmethod
    def __indices_of_reference__(*reference: Union[singlet, singlets], index_to_check: int) -> Tuple[int, ...]:
        """Returns a tuple of indices for reference that is present and index of that reference is greater than the index
        to check (index in context of self.reference)."""

    def __init__(self, name: str, *notations: str, capture: Literal['auto', 'single', 'boolean'] = 'auto', helptext: str = ..., required: bool = False, default: default = ...,
                 reference: Iterable[str] = sys.argv, skip: int = 1, auto_help: bool = False, help_notations: Iterable[str] = ..., application_name: str = sys.argv[0], application_version: str = '1.0', application_description: str = ...) -> None:
        """Create a singlet object with given parameters.
        
        This singlet object created will solely base itself on the given parameters and will work by strictly
        abiding to the parameter specifications.

        Once created the attributes that can be modified using square brackets, will have type hints available.

        This class somewhat partially parses the argument upon object creation using the `__partial__` method
        and calls it again when any attribute is changed using square brackets.

        The `reference` parameter specifies the argument pool which will processed to extract parsing information.
        By default its the argument passed to the script (`sys.argv`) and `skip` parameter specifies the number of
        elements of `reference` to skip. In default case, `sys.argv[0]` is the script name and is not required,
        therefore, `skip` is `1`.

        The `default` and `required` parameters are optional and if both are present, it will override the
        `required` functionality because if there is a default value, then why does it need to be marked as
        required?

        ## Singlet Object Types:

        ### 1. A singlet argument that takes a single value.

        Example:

        ```zsh
        $ your-script.py --argument value
        ```

        Here the `--argument` takes a value `value` and to create this configuration,
        use the following code structure:

        ```python
        single_capture_argument = singlet('argument-1', '--argument', '-a', capture='single', ...)
        ```
    
        The `capture` parameter ensures only one value is captured when using `single` as it's value.
        If you are expecting indefinite values for an argument use `capture='auto'`.

        NOTE: This option requires for extra references while parsing, which is all other arguments
        or argument groups that are defined in the current context.

        For example,

        ```python
        argument1 = singlet(..., capture='single', ...)
        argument2 = singlet(...)
        argument3 = singlet(...)

        # to parse capture='single' and detect potential errors, a
        # reference is needed.
        value = argument1.__parse__(argument1, argument2, argument3) # and so on.
        ```

        All arguments (`singlet`) and argument groups (`singlets`) must be passed to the `__parse__`
        method as reference for it to detect potential issues and parse the arguments correctly.
        
        ### 2. A singlet argument that takes indefinite number of values.

        Example:

        ```zsh
        $ your-script.py --argument value1, value2, v3, ... # indefinite number of arguments
        ```

        Here, the `--argument` takes indefinite number of values and to create this configuration,
        use `capture='auto'`. Similar to `capture='single'` this will require a context reference
        (all created `singlet` and `singlets` object) during parsing. (see 1.)

        ### 3. A singlet argument that takes no values but its presence is stored as a boolean parameter.

        Example:
        
        ```zsh
        $ your-script.py --argument # signifies True if present else False
        ```

        To create this configuration, use `capture='boolean'` and parsing it does not require any context
        reference. The `default` value for this type of argument is automatically set to `False` unless
        specified otherwise.
        """

    @overload
    def __helptext__(self, exit: Literal[True], exit_code: int = ...) -> NoReturn:
        """print help text and exit with `exit_code`."""

    @overload
    def __helptext__(self, exit: Literal[False]) -> None:
        """print help text."""

    def __partial__(self, raise_error: bool = True) -> None:
        """Partially parse the argument to retreive information about it from the set reference such as its
        presence and location.

        If `raise_error` is `False`, it will avoid raising any errors (not recommended).
        """

    @overload
    def __parse__(self, *reference: Union[singlet, singlets], raise_error: bool = True) -> Union[Tuple[str, ...], str, bool, default, None]:
        """Fully parse the argument and return the result if any.
        
        Return Type is based on `capture-type` attribute:
        - `capture-type='boolean'` returns bool.
        - `capture-type='single'` returns either str or default or None.
        - `capture-type='auto'` returns str (if only one value), Tuple[str, ..] (if multiple value), default or None.
        """

    @overload
    def __parse__(self, *reference: Union[singlet, singlets], capture_type: Literal['single'], raise_error: bool = True) -> Union[str, default, None]:
        """Fully parse the argument with given `capture_type='single'`"""
    @overload
    def __parse__(self, *reference: Union[singlet, singlets], capture_type: Literal['boolean'], raise_error: bool = True) -> bool:
        """Fully parse the argument with given `capture_type='boolean'`"""
    @overload
    def __parse__(self, *reference: Union[singlet, singlets], capture_type: Literal['auto'], raise_error: bool = True) -> Union[str, default, Tuple[str, ...], None]:
        """Fully parse the argument with given `capture_type='auto'`.
        
        - Returns str if one value is present, else a tuple.
        - Returns default value if the argument is not present.
        - Else None.
        """

    @property
    def __present__(self) -> bool:
        """`True` if singlet argument is present in the argument pool, else `False`."""

    @property
    def __notpresent__(self) -> bool:
        """`True` if singlet argument is not present in the argument pool, else `False`."""

    @property
    def __index__(self) -> int:
        """Index of the singlet argument in the argument pool. If not present, `-1`."""

    @property
    def __notation__(self) -> str:
        """Notation variant of the singlet argument that is found in the argument pool. If not present, `''`."""

    @property
    def __usage__(self) -> str:
        """formatted usage string for this argument."""



class singlets:
    """A class to represent a collection of `singlet` arguments.
    
    The structure for creating `singlets`:

    - A base argument (that identifies this collection)
        - Any number of `singlet` arguments.
        - Any number of `singlets` collections.

    This class contains parameters for a collection of arguments such that a base argument that uniquely
    identifies this collection must be present.
    
    If that base argument is a required argument, then it will act as a simple `singlet` argument being required
    and will not affect any other arguments or colelctions withing this collection. If any `singlet` argument is
    set as required, it will behave different than the base argument: the required `singlet` argument will be
    required only if the base argument (this collection) is being used. Unless the base argument is present, any
    of the other arguments present in this collection will not raise errors for requirement.

    Similarly, unles the base argument is being used, using any other arguments under this collection will raise
    an exception.

    These same set of rules will also be followed by any nested collections under this collection. If a child
    collection's base argument is used but it's parent's base argument is not used, that will also raise an error.
    """


    __attrs__: Tuple[Literal['name'], Literal['parent'], Literal['helptext'], Literal['reference'], Literal['auto-help'], Literal['help-notations'], Literal['application-name'],
                     Literal['application-version'], Literal['application-description'], Literal['collection'], Literal['present'], Literal['notpresent'], Literal['base']]


    @overload
    def __getitem__(self, name: Literal['name'], /) -> str: ...
    @overload
    def __getitem__(self, name: Literal['parent'], /) -> Union['singlets', None]: ...
    @overload
    def __getitem__(self, name: Literal['helptext'], /) -> str: ...
    @overload
    def __getitem__(self, name: Literal['reference'], /) -> Iterable[str]: ...
    @overload
    def __getitem__(self, name: Literal['auto-help'], /) -> bool: ...
    @overload
    def __getitem__(self, name: Literal['help-notations'], /) -> Iterable[str]: ...
    @overload
    def __getitem__(self, name: Literal['application-name'], /) -> str: ...
    @overload
    def __getitem__(self, name: Literal['application-version'], /) -> str: ...
    @overload
    def __getitem__(self, name: Literal['application-description'], /) -> str: ...
    @overload
    def __getitem__(self, name: Literal['collection'], /) -> Dict[str, Union[singlet, 'singlets']]: ...
    @overload
    def __getitem__(self, name: Literal['present'], /) -> bool: ...
    @overload
    def __getitem__(self, name: Literal['notpresent'], /) -> bool: ...
    @overload
    def __getitem__(self, name: Literal['base'], /) -> Union[singlet, None]: ...


    @overload
    def __setitem__(self, name: Literal['name'], value: str, /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['parent'], value: singlets, /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['helptext'], value: str, /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['reference'], value: Iterable[str], /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['auto-help'], value: bool, /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['help-notations'], value: Iterable[str], /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['application-name'], value: str, /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['application-version'], value: str, /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['application-description'], value: str, /) -> None: ...
    @overload
    def __setitem__(self, name: Literal['base'], value: Union[singlet, None], /) -> None: ...
    @overload
    def __setitem__(self, name: Any, value: Any, /) -> NoReturn: ...


    def __delitem__(self, name: Any, /) -> NoReturn: ...


    @property
    def __base__(self) -> Union[singlet, None]:
        """The base argument object for this singlets object if present, else None."""


    def __init__(self, name: str, parent: Union[singlets, None] = ..., helptext: str = ..., reference: Iterable[str] = sys.argv, skip: int = 1, auto_help: bool = False,
                 help_notations: Iterable[str] = ..., application_name: str = sys.argv[0], application_version: str = '1.0', application_description: str = ...) -> None:
        """Create a singlets object with given parameters.
        
        The singlets object is collection of objects of type singlet or singlets.
        Any singlets object with parent attribute as `None` is the topmost singlets object in the collection tree, else
        has some other singlets object as it's parent.

        The `reference` parameter specifies the argument pool from which the arguments are parsed, by default set to `sys.argv`
        with `skip` set to `1` which strips the `sys.argv[0]` value (script name). The `reference` parameter can be set to any
        iterable of strings with `skip` parameter to specify how many values from left side to skip.

        The `parent` must be another `singlets` object or simply `None`.
        
        Each `singlets` object contains a base argument which uniquely identifies the `singlets` collection. If the base argument
        is marked as `required=True` then it simply acts as a required argument. However, if any other argument in the collection
        is marked `required=True` then it is only required to pass that argument if the base argument is present (meaning: If the
        collection is being used (identified by usage of base argument), then only any required arguments are required to be passed).
        
        This passively (without using `required` parameter) applies to all nested `singlets` objects such that, any child `singlets`
        object cannot be used until it's parent's base argument has been used.
        """


    def __singlet__(self, name: str, *notations: str, base=False,
                    capture: Literal['auto', 'single', 'boolean'] = 'auto',
                    helptext: str = ..., required=False, default: Any = ...) -> Self:
        """Add a singlet object into the collection pool."""


    def __singlets__(self, name: str, parent: Union[singlets, None] = ..., helptext: str = ...) -> Self:
        """Add a child singlets object into the collection pool.
        
        If `parent` parameter is `None`, current `singlets` object will be set as the parent.
        """


    @overload
    def __helptext__(self, exit: Literal[True], exit_code=0, acknowledgement=True, usage=True) -> NoReturn:
        """Print helptext for the entire collection pool and exit."""

    @overload
    def __helptext__(self, exit: Literal[False], exit_code=0, acknowledgement=True, usage=True) -> None:
        """Print helptext for the entire collection pool."""


    @overload
    def __parse__(self, reference: Iterable[Union[singlet, singlets]]) -> Dict[str, Union[Dict[str, Any], Any]]:
        """Parse the entire collection pool and return a dict with names of objects as keys and their respective
        parsed values as keys. The `reference` parameter expects an iterable of all defined `singlet` and `singlets`
        object in the context."""

    @overload
    def __parse__(self, reference: Iterable[Union[singlet, singlets]], order: Iterable[Union[str, Tuple[Union[Tuple[Any, ...], str], ...]]]) -> Tuple:
        """Parse the entries from collection pool in given order where the `order` parameter accepts,
        object names. Returns a tuple with parsed values in sequence.
        
        This method is a bit complex but is very powerful in terms of retreiving parsed values of highly
        nested `singlets` objects.

        As an example, if you have 3 arguments named arg1, arg2 and arg3 and another `singlets` object as
        a child with name, say, child_singlet. Now that child_singlet further has arg4 and arg5.

        To get the parsed values in order of -> arg1, arg2, arg3, arg4, arg5

        ```python
        # you can either use:
        obj.__parse__(reference, order=('arg1', 'arg2', 'arg3', 'arg4', 'arg5'))
        # will return (v1, v2, v3, v4, v5)

        # or
        obj.__parse__(reference, order=('arg1', 'arg2', 'arg3', ('child_singlet', 'arg4', 'arg5')))
        # will return (v1, v2, v3 (v4, v5)).
        ```

        and so on.
        """


    def __object__(self, name: str, /) -> Union[singlet, singlets, None]:
        """`singlets` class' native object search function that returns the object with given name if found, else `None`."""


    def __register_singlet_for_this_singlets_object__(self, singlets_object_name: str, singlet_object_name: str, *notations: str,
                                                      base=False, capture: Literal['auto', 'single', 'boolean'] = 'auto', helptext: str = ..., default: Any = ...) -> Self:
        """Add a `singlet` object under given `singlets` object. If the `singlets` object name provided is of the current object then current object's `__singlet__`
        method will be called instead."""


    def __register_singlets_for_this_singlets_object__(self, parent_singlets_object_name, child_singlets_object_name, helptext: str = ...) -> Self:
        """Add a `singlets` object under given parent `singlets` object. If the parent `singlets` object name is of the current object then current object's
        `__singlets__` method will be called."""