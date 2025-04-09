"""lawyer [`Module`].

This module contains the `Judge` class which is a safe implementation of collective
`lawyer.parsers.singlet` and `lawyer.parsers.singlets` classes. It also contains a
method named `minimal_traceback` which the `Judge` class uses for creating highly
focussed exception tracebacks to specify the exact high level line where error
occured.

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



from lawyer.parsers import singlet, singlets
from typing import Iterable, Literal, Type, NoReturn, Dict
from typing import Union, overload, Any, Self, Tuple
import sys


original_excepthook = sys.excepthook

def minimal_traceback(exception: Type[BaseException], *args: object) -> NoReturn:
    """Raise the `exception` with given `args` limiting output to exactly last call of error."""


class Judge:
    """A safe implementation of argument + group parsing.
    
    This class covers a safe code implementation to avoid most errors and show the root cause
    of where the error actually occurred and why. Instead of maining a long definition of
    `singlet` and `singlets` objects to create argument parsing, this class acts as a wrapper
    class that handles most operations internally and provides high level user callable methods.

    `Judge` allows addition of any number of single or grouped arguments (which can be nested) and parsing
    in any order or individually. Most attributes and properties in this class are made read-only to prevent
    failure due to mishandling. Some properties allow modification such as `__application__` (application name),
    `__version__` (application version), `__description__` (application description), `__autohelp__` (whether to
    show help text automatically) and `__help_notations__` (the argument notation that denotes help).

    `Judge` also allows accessing internal `singlet` and `singlets` objects using the `object` method which requires
    the object's name.

    `Judge` class is not thread-safe. Creation of a single instance and using it across threads will result in
    malfuction.
    """

    @property
    def __application__(self) -> str:
        """The application name to be used during helptext generation. If not set, the default is
        set to `sys.argv[0]` (the script name)."""

    @property
    def __version__(self) -> str:
        """The application version to be used during helptext generation. If not set, the default is
        set to `1.0`."""

    @property
    def __description__(self) -> str:
        """The application description to be used during helptext generation. If not set, the default is
        empty and will not be shown."""

    @property
    def __reference__(self) -> Iterable[str]:
        """The argument pool from which arguments and groups are parsed. Once set using the `__init__`
        method, this property becomes read-only."""

    @property
    def __collection__(self) -> Dict[str, Union[singlet, singlets]]:
        """The internal argument/group collection tree; read-only."""

    @property
    def __autohelp__(self) -> bool:
        """The internal flag that determines whether to show helptext automatically. If set to `True`, requires
        to update `__help_notations__` property else will default to `--help` and `-h`."""

    @property
    def __help_notations__(self) -> Iterable[str]:
        """The notations to use for help argument detection. Defaults to `--help` and `-h`."""

    def __setattr__(self, name: str, value: Any, /) -> None: ...
    def __getattribute__(self, name: str, default: Any = None, /) -> Any: ...


    def __init__(self, application_name: str = ..., application_version: str = ...,
                 application_description: str = ..., reference: Iterable[str] = ...,
                 skip: int = ..., auto_help=False, help_notations: Iterable[str] = ...) -> None:
        """Create a `Judge` instance with given parameters. Some of these parameters become
        read-only upon object creation and therefore pay utmost attention to those.
        
        Attributes that becomes read-only:
        - `reference`: The argument pool from which argument(s)/group(s) will be parsed. By default it assumes
        the value of `sys.argv` with `skip` number of elements skipped from it from the left. By default `skip`
        assumes the value of `1` and therefore the resultant default argument pool is `sys.argv[1:]`. Can be
        accessed later using the `__reference__` property, but cannot be changed or deleted.

        Attributes the does not become read-only:
        - `application_name`: This is the application name to be used for helptext generation. If not set during
        `__init__`, can be set or modified later using the `__application__` property. If not changed throughout,
        will use `sys.argv[0]` as its default value.

        - `application_version`: This is the application version to be used for helptext generation. If not set
        during `__init__`, can be set or modified later using `__version__` property. If not changed throughout,
        will use `1.0` as its default value.

        - `application_description`: This description will be used during helptext generation if given as is totally
        optional. If not set during `__init__`, can be set or modified later using `__description__` property. If not
        changed throughout, will be empty and will not be used.

        - `auto_help`: Specifies whether to automatically show helptext and exit the script if any of the `help_notations`
        are found after an argument/group-argument. If set to `True`, and `help_notations` are not set, default help
        notations will be used: `('--help', '-h')`. Can be changed or set later using the `__autohelp__` property.

        - `help_notations`: Specifies a set of notations that do not collide with other argument/group definitions, that
        uniquely identifies if the user is asking for helptext for any given argument/group. By default, assumes notations:
        `--help` and `-h` for helptext, but wont be triggered until `auto_help` is set to `True`. Can be changed or set later
        using `__help_notations__` property.
        """

    def object(self, name: str, /) -> Union[singlet, singlets, None]:
        """Returns the underlying object with given name. If not found, returns `None`."""

    def add_argument(self, name: str, *notations: str, capture: Literal['auto', 'single', 'boolean'] = 'boolean',
                     helptext: str = ..., required=False, default: Any = ..., parent: str = ..., base=False) -> Self:
        """Add an argument into the collection. The parameters are very strict and cannot be changed through this
        class. However, the `object` method of this class can be used to retreive the internal underlying argument/
        group object and then parameters can be modified.
        
        Parameters:
        - `name`: name of the argument, make this unique as the argument will be accessed using this parameter only. Acts as
        an identifier for the argument.

        - `*notations`: argument notations to look for in the argument pool such as `--argument`. There is no constraint over
        how the argument notations needs to be and therefore simple words such as `argument` can also be used or any custom
        kind such as `@argument`. supports intermixed or multiple signatures.

        ```zsh
        $ your-script.py @argument1 --argumemt2 value # example.
        ```

        - `capture`: This parameter sets the argument capture mode. If the argument is supposed to take some value(s), use either
        `'single'` (expects exactly one value after the argument) or `'auto'` (expects atleast one value after the argument).
        Else if the argument needs to act as a flag such that it's presence in the argument pool represents boolean `True` and absence
        represents `False`, use `'boolean'` capture mode.

        - `helptext`: The help description for this particular argument which will be shown along with its notations to the user when
        help is triggered.

        - `parent`: If this argument is supposed to be registered under a specific group that is already registered using the `add_group`
        method, then specify the group name here.

        - `base`: This parameter is only valid when using `parent` parameter to specify a parent argument group. The `base` parameter
        specifies if the current argument is to be set as the group's base argument. If the base argument is present, only then all
        other arguments in that group is valid. Also, if any group's base argument is present but the group's parent (another group)'s
        base argument is not present, will raise an error. For more information regarding nested groups, refer documentation.

        - `default`: This is only valid when using capture mode as `'single'` or `'auto'` as for `'boolean'`, it will be automatically
        set to `False`. However, that `False` value can still be overridden if the default value is specified. This paramater holds no
        value when the `required` parameter is set to True.

        - `required`: This parameter sets an internal mechanism which makes sure that the current argument is mandatorily present in the
        argument pool else generates an exception. This works differently for grouped arguments: if the group's base argument is marked
        as a required argument, it acts similar to a single argument being marked required, however, all other arguments if marked
        required, the requirement mechanism is only triggerd if the base argument is present in the argument pool, else doesn't matter.

        This is the sole method that has to be used to create arguments. If `object` method is used to access underlying `singlet` or
        `singlets` object to create arguments, it wont be parsed as intended.
        """


    def add_group(self, name: str, parent: str = ..., helptext: str = ...) -> Self:
        """Create an empty argument group with given parameters.
        
        Parameters:

        - `name`: name uniquely identifies the group and is the only value that can be used to
        access it.

        - `parent`: This parameter accepts another group's name under which this new group will be created.
        If left untouched, the group will be created independently at topmost level.

        - `helptext`: The helptext description to show users along with all arguments' helptexts under this group when
        help is triggered.

        This is the sole method that has to be used to create argument groups. If `object` method is used to access underlying
        `singlets` object to create another sub-group, it wont be parsed as intended.
        """

    @overload
    def parse(self) -> Dict[str, Any]:
        """Parse all arguments and argument groups and return their parsed value in the form of a dictionary where,
        the keys are names of objects and values are their parsed value from the argument pool. All groups will have
        another dictionary as their value, where the keys will be the names of arguments/groups under that group and
        so on."""


    @overload
    def parse(self, order: Union[str, Tuple[str, ...]], /) -> Any:
        """Parses a single argument or group. If the motive is to parse an argument no matter how deep into the object tree,
        just mention the name of the argument (str), if it is a group, use a tuple where the first element is the group name,
        followed by the order in which the contents are inteded to be parsed and returned. The order in which the group needs
        to be parsed must contain atleast one element.

        Example:

        ```python
        value = judge_instance.parse('argument1')
        value2 = judge_instance.parse(('arg_grp', 'arg_grp_arg1', 'arg_grp_arg2'))
        ```
        
        If parsing an argument, may return bool (if capture mode is boolean), str (if capture mode is single), tuple[str, ...]
        (if the capture mode is auto, however, if only one value is found, returns str) or the default value set for the argument
        if not present. If no default value is present, and the argument is not passed in the argument pool, returns None.

        If parsing a group, A tuple will be returned with contents in the order as specified, where each individual argument will
        follow the above mentioned return types and any sub-groups will just repeat this.
        """


    @overload
    def parse(self, *order: Union[str, Tuple[str, ...]]) -> Union[Tuple[Any, ...], Any]:
        """Parse any number of objects all at once in the given order.
        
        For arguments, just use their names to specify them, but for argument groups, use a tuple where the first element is the
        group name followed by the order of objects inside that group. If the group has subgroups, use the same tuple format for
        the same. The group construct requires atleast one entry after the group name.

        Example:
        
        ```python
        value = judge_instance.parse('arg1', 'arg2', ('grp1',)) # not valid, expects atleast one value for order after the group name.
        value = judge_instance.parse('arg1', ('grp1', 'grp1-arg1'), 'arg2') # valid
        value = judge_instance.parse('arg1', ('grp1', ('grp2', 'grp2-arg1'))) # valid
        ```
        """