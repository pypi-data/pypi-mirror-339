import typing
import shutil
import sys

from lawyer.exceptions import ParameterError, ArgumentError, ParseError

# ----------------------------LICENSE---------------------------------------------

# MIT License

# Copyright (c) 2025 Soumyo Deep Gupta

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ------------------------------END-----------------------------------------------

default = typing.TypeVar('default')


class singlet(typing.Generic[default]):


    # These attributes are available to access using sqare brackets on any
    # instance of `singlet` class.


    __attrs__ = ('name', 'notations', 'capture-type', 'helptext', 'default', 'required', 'reference', 'auto-help', 'help-notations',
                 'application-name', 'application-version', 'application-description', 'present', 'notation', 'notpresent', 'index')


    # These values are the only allowed values that the `capture` parameter
    # can take


    __allowed_capture_types__ = ('auto', 'single', 'boolean')


    # This is a special `__getitem__` method which facilitates accessing attributes
    # or custom named properties using square brackets.
    # All attributes in __attrs__ are allowed to be fetched.


    def __getitem__(self, name, /):
        if name not in self.__attrs__:
            raise AttributeError(
                f"'{name}' attribute cannot be accessed using square brackets.")
        if name is 'present':
            return self.__present__
        if name is 'notpresent':
            return self.__notpresent__
        if name is 'notation':
            return self.__notation__
        if name is 'index':
            return self.__index__
        return getattr(self, name.replace('-', '_'), None)


    # This is a special __setitem__ method which facilitates assignment of attributes
    # and custom named properties using square brackets.
    # Only some of the properties and attributes can be modified such as
    # ('present', 'notpresent', 'notation', 'index') cannot be modified.
    # After every change the __partial__ initialization method is called to retrieve
    # new information about the argument from self.reference.


    def __setitem__(self, name, value, /) -> None:
        if name in ('present', 'notpresent', 'notation', 'index') or name not in self.__attrs__:
            raise AttributeError(
                f"'{name}' attribute cannot be set using square brackets.")
        if name is 'name' and not isinstance(value, str):
            raise AttributeError(f"name attribute must be of type <class 'str'>.")
        if name is 'notations' and not (isinstance(value, typing.Iterable) and not isinstance(value, str) and all(isinstance(notation, str) for notation in value)):
            raise AttributeError(f"notations attribute must be an iterable of strings.")
        if name is 'capture-type' and value not in ['auto', 'single', 'boolean']:
            raise AttributeError(f"capture-type must be any one of 'auto', 'single' or 'boolean'.")
        if name is 'helptext' and not isinstance(value, str):
            raise AttributeError(f"helptext attribute must be of type <class 'str'>.")
        if name is 'required' and not isinstance(value, bool):
            raise AttributeError(f"required attribute must of type <class 'bool'>.")
        if name is 'reference' and not (isinstance(value, typing.Iterable) and not isinstance(value, str) and all(isinstance(ref, str) for ref in value)):
            raise AttributeError(f"reference attribute must be an iterable of strings.")
        if name is 'auto-help' and not isinstance(value, bool):
            raise AttributeError(f"auto-help attribute must be of type <class 'bool'>.")
        if name is 'help-notations' and not (isinstance(value, typing.Iterable) and not isinstance(value, str) and all(isinstance(help_notation, str) for help_notation in value)):
            raise AttributeError(f"help-notations must be an iterable of strings.")
        if name is 'application-name' and not isinstance(value, str):
            raise AttributeError(f"application-name attribute must be of type <class 'str'>.")
        if name is 'application-version' and not self.__version_format_checker__(value):
            raise AttributeError(f"application-version attribute must be of type <class 'str'> and in valid version format.")
        if name is 'application-description' and not isinstance(value, str):
            raise AttributeError(f"application-description attribute must be of type <class 'str'>.")
        setattr(self, name.replace('-', '_'), value)
        self.__partial__(raise_error=True)


    # No attribute or custom named properties will be allowed to be deleted
    # using square brackets.


    def __delitem__(self, name, /) -> None:
        raise AttributeError(
            f"attributes cannot be deleted using square brackets.")


    # The str function will return `singlet(*notations)`


    def __str__(self) -> str:
        return 'singlet(' + ', '.join(self.notations) + ')'


    # The string representation will return what str function will return when
    # used on self.


    def __repr__(self) -> str:
        return str(self)


    # The __readonly__ property construct is designed to be immutable and its core job is
    # to raise an AttributeError upon any kind of access/ assignment/ deletion.
    # This property will be used by other properties to generate exception when assignment
    # or deletion is being performed.


    @property
    def __readonly__(self) -> typing.NoReturn:
        raise AttributeError(f"No attribute named __readonly__ found for singlet class.")

    @__readonly__.setter
    def __readonly__(self, value) -> typing.NoReturn:
        raise AttributeError(f"properties of singlet class are read-only and doesn't support assignment.")

    @__readonly__.deleter
    def __readonly__(self) -> typing.NoReturn:
        raise AttributeError(f"properties of singlet class are read-only and doesn't support deletion.")


    # This method checks if any given object is a valid version string such as '1.0', '1.2.3',
    # and is currently half assed, will be removed further.


    @staticmethod
    def __version_format_checker__(candidate) -> typing.TypeGuard[str]:
        if not isinstance(candidate, str):
            return False
        if not '.' in candidate:
            return False
        # later on add more checks here.
        return True


    # The __init__ method will check all parameters and and store them. Additionally,
    # it will perform partial parsing where it will identify the presence status,
    # index and notation that is present in the reference.


    def __init__(self, name, *notations, capture='auto', helptext='', required=False, default: default = ..., reference=sys.argv,
                 skip=1, auto_help=False, help_notations=(), application_name=sys.argv[0], application_version='1.0', application_description='') -> None:
        if not isinstance(name, str):
            raise ParameterError(ParameterError.__strerror__.format('name'))
        if not all(isinstance(notation, str) for notation in notations):
            raise ParameterError(
                ParameterError.__strerror__.format('notations'))
        if not capture in self.__allowed_capture_types__:
            raise ParameterError(
                ParameterError.__capturetyperror__.format(
                    self.__allowed_capture_types__))
        if not isinstance(helptext, str):
            raise ParameterError(
                ParameterError.__strerror__.format('help-text'))
        if not isinstance(required, bool):
            raise ParameterError(
                ParameterError.__boolerror__.format('required parameter'))
        if not isinstance(reference, typing.Iterable) or not all(
                isinstance(ref, str) for ref in reference):
            raise ParameterError(
                ParameterError.__iterablerror__.format('reference'))
        if not isinstance(skip, int):
            raise ParameterError(
                'skip parameter must be of type <class \'int\'>.')
        if not isinstance(auto_help, bool):
            raise ParameterError(
                'auto-help parameter must be of type <class \'bool\'>.')
        if not isinstance(help_notations, typing.Iterable) or not all(
                isinstance(help_notation, str) for help_notation in help_notations):
            raise ParameterError(
                ParameterError.__iterablerror__.format('help-notations'))
        if not isinstance(application_name, str):
            raise ParameterError(
                ParameterError.__strerror__.format('application-name'))
        if not isinstance(application_version, str) or not self.__version_format_checker__(
                application_version):
            raise ParameterError(
                "application-version provided is not in valid version format such as 1.0, 2.8.9, etc.")
        if not isinstance(application_description, str):
            raise ParameterError(
                ParameterError.__strerror__.format('application-description'))

        self.name = name
        self.notations = notations
        self.capture_type = capture
        self.helptext = helptext
        
        if default is ... and self.capture_type is 'boolean':
            self.default = False
        elif (default is not ... and self.capture_type is 'boolean') or default is not ...:
            self.default = default

        self.required = required
        self.reference = reference[skip:]
        self.auto_help = auto_help
        self.help_notations = help_notations or ('--help', '-h')
        self.application_name = application_name
        self.application_version = application_version
        self.application_description = application_description
        self.__partial__(raise_error=True)


    # The __helptext__ method is responsible for printing current singlet object's
    # help text.


    def __helptext__(self, exit, exit_code=0) -> None:
        print(f"\n{self.application_name} v{self.application_version}")
        print(f"{self.application_description}\n")

        adder = ''.join(
            f"[{notation}]" for notation in self.help_notations) if self.help_notations else ''

        print(f"usage: {self.application_name} {self.__usage__}{adder}\n")

        helptext = ' | '.join(
            self.help_notations) if self.help_notations else ''

        selftext = ' | '.join(self.notations)
        maxlength = max(len(helptext), len(selftext), 0)

        if helptext:
            print(f"{helptext.ljust(maxlength + 3)} : show this helptext and exit.")
        print(f"{selftext.ljust(maxlength + 3)} : {self.helptext}")

        if exit:
            sys.exit(exit_code)


    # The __present__ property returns True if the singlet argument is found in the
    # reference else False


    @property
    def __present__(self) -> bool:
        return self.__ispresent__

    @__present__.setter
    def __present__(self, value) -> typing.NoReturn:
        self.__readonly__ = value

    @__present__.deleter
    def __present__(self) -> typing.NoReturn:
        del self.__readonly__


    # The __notation property returns the notation variant found in the reference
    # for this singlet argument, If not found returns an empty string


    @property
    def __notation__(self) -> str:
        if hasattr(self, '__notation_in_ref__'):
            return self.__notation_in_ref__
        return ''

    @__notation__.setter
    def __notation__(self, value) -> typing.NoReturn:
        self.__readonly__ = value

    @__notation__.deleter
    def __notation__(self) -> typing.NoReturn:
        del self.__readonly__


    # The __index__ property returns the index of reference where the singlet
    # object's one of the notation has been found. If not found, returns -1.


    @property
    def __index__(self) -> int:
        if hasattr(self, '__index_in_ref__'):
            return self.__index_in_ref__
        return -1

    @__index__.setter
    def __index__(self, value) -> typing.NoReturn:
        self.__readonly__ = value

    @__index__.setter
    def __index__(self) -> typing.NoReturn:
        del self.__readonly__


    # The __partial__ method is responsible for extracting information such as
    # the index, notation and presence status of the argument in the given reference
    # and is triggered as early as __init__. Updation of class attributes using square
    # brackets also triggers it.


    def __partial__(self, raise_error=True) -> None:

        if hasattr(self, '__notation_in_ref__'):
            del self.__notation_in_ref__
        if hasattr(self, '__index_in_ref__'):
            del self.__index_in_ref__

        if self.capture_type is 'boolean' and not hasattr(self, 'default'):
            self.default = False

        self.__ispresent__ = False
        for notation in self.notations:
            if notation in self.reference:
                self.__ispresent__ = True
                self.__notation_in_ref__ = notation
                self.__index_in_ref__ = self.reference.index(notation)
                break

        if self.__present__ and self.auto_help and self.help_notations:
            possible_help_trigger = self.__parse__(
                self, capture_type='single', raise_errors=False)
            if possible_help_trigger and possible_help_trigger in self.help_notations:
                self.__helptext__(exit=True, exit_code=0)

        if self.required and not self.__present__ and not hasattr(
                self, 'default') and raise_error:
            raise ArgumentError(
                f"Any one of {
                    self.notations} is a mandatory argument in this context!")


    # The __usage__ property returns only the usage of this particular argument in string
    # format.


    @property
    def __usage__(self) -> str:

        string = '[ '
        if len(self.notations) == 1:
            if self.capture_type is 'boolean':
                return string + self.notations[0] + ' ]'
            elif self.capture_type is 'single':
                return string + self.notations[0] + ' [VALUE] ]'
            else:
                return string + self.notations[0] + ' [...] ]'

        for notation in self.notations:
            if self.capture_type is 'boolean':
                string += f"[{notation}]"
            elif self.capture_type is 'single':
                string += f'[{notation} [VALUE]]'
            else:
                string += f'[{notation} [...]]'
        return string + ' ]'

    @__usage__.setter
    def __usage__(self, value) -> typing.NoReturn:
        self.__readonly__ = value

    @__usage__.deleter
    def __usage__(self) -> typing.NoReturn:
        del self.__readonly__


    # A function that checks if a given value is present in any of notations of any of the singlet/ singlets
    # objects in provided reference.


    @staticmethod
    def __value_in_reference__(*reference, value) -> bool:
        for ref in reference:
            if isinstance(ref, singlet) and ref.__present__ and value in ref.notations:
                return True
            elif isinstance(ref, singlets):
                is_true = singlet.__value_in_reference__(
                    *ref.collection.values(), value=value)
                if is_true:
                    return True
        return False


    # A function that returns a tuple of indices from self.reference for the known singlet/ singlets
    # notations where their index > index_to_check.
    # Meaning: return all indices for singlet/ singlets objects (that are provided in the reference
    # parameter) such that they are positionally on the right of the index_to_check parameter.


    @staticmethod
    def __indices_of_reference__(
            *reference, index_to_check) -> typing.Tuple[int, ...]:
        # will return indices of objects greater than index_to_check
        indices = []
        for ref in reference:
            if isinstance(
                    ref, singlet) and ref.__present__ and ref.__index__ > index_to_check:
                indices.append(ref.__index__)
            elif isinstance(ref, singlets):
                tree_indices = singlet.__indices_of_reference__(
                    *ref.collection.values(), index_to_check=index_to_check)
                for idx in tree_indices:
                    if idx not in indices:
                        indices.append(idx)
        return tuple(indices)


    # The __parse__ method is responsible for fully parsing the current singlet argument based on relative
    # reference and return the result.


    def __parse__(self, *reference, capture_type=None,
                  raise_errors=True) -> typing.Union[bool, str, typing.Tuple[str, ...], default, None]:
        if capture_type is None:
            capture_type = self.capture_type

        if self.__present__:

            if capture_type is 'boolean':
                return self.__present__

            elif capture_type is 'single':

                if not reference:
                    if raise_errors:
                        raise ParseError(
                            f"a reference is required for parsing capture-type='single'.")
                    else:
                        return None

                try:
                    potential_value = self.reference[self.__index__ + 1]
                    if self.__value_in_reference__(
                            *reference, value=potential_value):
                        if raise_errors:
                            raise ParseError(
                                f"'{self.__notation__}' expects a value.")
                        else:
                            return None
                    return potential_value
                except IndexError:
                    if raise_errors:
                        raise ParseError(
                            f"'{self.__notation__}' expects a value.")
                    else:
                        return None

            elif capture_type is 'auto':
                if not reference:
                    if raise_errors:
                        raise ParseError(
                            f"a reference is required for parsing capture-type='auto'.")
                values = self.reference[self.__index__ +
                                        1: min(self.__indices_of_reference__(*
                                                                             reference, self.__index__), default=len(self.reference))]
                if values:
                    if isinstance(values, typing.Iterable) and not isinstance(
                            values, str):
                        if len(values) > 1:
                            return tuple(values)
                        elif len(values) == 1:
                            return values[0]
                        else:
                            raise ParseError(
                                f"'{self.__notation__}' expects a value.")
                    else:
                        return values
                raise ParseError(
                    f"'{self.__notation__}' expects atleast one value.")

        elif hasattr(self, 'default'):
            return self.default

        return None


    # The __notpresent__ property is a compliment of __present__ property.


    @property
    def __notpresent__(self) -> bool:
        return not self.__present__

    @__notpresent__.setter
    def __notpresent__(self, value) -> typing.NoReturn:
        self.__readonly__ = value

    @__notpresent__.deleter
    def __notpresent__(self) -> typing.NoReturn:
        del self.__readonly__





class singlets:


    # All attributes that can be accessed via square brackets can be found in __attrs__.


    __attrs__ = ('name', 'parent', 'helptext', 'reference', 'auto-help', 'help-notations', 'application-name',
                 'application-version', 'application-description', 'collection', 'present', 'notpresent', 'base')


    # The __getitem__ method is responsible for providing access to the class attributes
    # using square brackets.


    def __getitem__(self, name, /):
        if name not in self.__attrs__:
            raise AttributeError(f"attribute {name} cannot be accessed using sqare brackets.")
        if name is 'present':
            return self.__ispresent__
        if name is 'notpresent':
            return not self.__ispresent__
        if name is 'base':
            return self.__base__

        return getattr(self, name.replace('-', '_'), None)


    # The __setitem__ method is responsible for enforcing assignment rules for class attributes
    # via square brackets.


    def __setitem__(self, name, value, /) -> None:
        if name in ('present', 'notpresent', 'collection') or name not in self.__attrs__:
            raise AttributeError(f"attribute {name} cannot be set using sqare brackets.")
        if name is 'name' and not isinstance(value, str):
            raise AttributeError(f"name of the singlets collection must be of type <class 'str'>.")
        if name is 'parent' and not (isinstance(value, singlets) or value is None):
            raise AttributeError(f"parent of a singlets object can only be another singlets object, or None.")
        if name is 'helptext' and not isinstance(value, str):
            raise AttributeError(f"help-text of singlets object must be of type <class 'str'>.")
        if name is 'reference' and not (isinstance(value, typing.Iterable) and all(isinstance(ref, str) for ref in value)):
            raise AttributeError(f"reference attribute of singlets object must be an iterable of strings.")
        if name is 'auto-help' and not isinstance(value, bool):
            raise AttributeError(f"auto-help attribute expects a bool value.")
        if name is 'help-notations' and not (isinstance(value, typing.Iterable) and all(isinstance(help_notation, str) for help_notation in value)):
            raise AttributeError(f"help-notations attribute expects an iterable of strings.")
        if name is 'application-name' and not isinstance(value, str):
            raise AttributeError(f"application-name attribute expects a string value.")
        if name is 'application-version' and not singlet.__version_format_checker__(value):
            raise AttributeError(f"application-version expects a string value which is in valid version format.")
        if name is 'application-description' and not isinstance(value, str):
            raise AttributeError(f"application-description attribute expects a string value.")
        if name is 'base' and not isinstance(value, singlet):
            raise AttributeError(f"base attribute expects a singlet object.")

        if name is 'base':
            if self.base is not None:
                del self.collection[self.base]
            self.base = value.name
            self.collection[self.base] = value
            return None

        setattr(self, name.replace('-', '_'), value)


    # The __delitem__ method prevents any deletion of attributes


    def __delitem__(self, name, /) -> typing.NoReturn:
        raise AttributeError(f"cannot delete attribute {name} of singlets class.")


    # The __readonly__ property is a construcy that restricts all kinds of modification
    # to any given property making it readonly.


    @property
    def __readonly__(self) -> typing.NoReturn:
        raise AttributeError(f"No property named __readonly__ found in singlets class.")

    @__readonly__.setter
    def __readonly__(self, value) -> typing.NoReturn:
        raise AttributeError(f"properties of singlets class are read-only and doesn't support assignment.")

    @__readonly__.deleter
    def __readonly__(self) -> typing.NoReturn:
        raise AttributeError(f"properties of singlets class are read-only and doesn't suport deletion.")


    # The __base__ property returns the base argument object (singlet) if defined, else
    # None.


    @property
    def __base__(self) -> typing.Union[singlet, None]:
        if self.base is None:
            return None
        return self.collection[self.base]

    @__base__.setter
    def __base__(self, value) -> typing.NoReturn:
        self.__readonly__ = value

    @__base__.deleter
    def __base__(self) -> typing.NoReturn:
        del self.__readonly__


    # The __init__ method in singlets' context only checks the parameters and stores them.

    def __init__(self, name, parent=None, helptext='', reference=sys.argv, skip=1, auto_help=False,
                 help_notations=(), application_name=sys.argv[0], application_version='1.0', application_description='') -> None:

        if not isinstance(name, str):
            raise ParameterError(ParameterError.__strerror__.format('name'))
        if not isinstance(helptext, str):
            raise ParameterError(
                ParameterError.__strerror__.format('help-text'))
        if not isinstance(reference, typing.Iterable) or not all(
                isinstance(ref, str) for ref in reference):
            raise ParameterError(
                ParameterError.__iterablerror__.format('reference'))
        if not isinstance(skip, int):
            raise ParameterError(
                'skip parameter must be of type <class \'int\'>.')
        if not isinstance(auto_help, bool):
            raise ParameterError(
                'auto-help parameter must be of type <class \'bool\'>.')
        if not isinstance(help_notations, typing.Iterable) or not all(
                isinstance(help_notation, str) for help_notation in help_notations):
            raise ParameterError(
                ParameterError.__iterablerror__.format('help-notations'))
        if not isinstance(application_name, str):
            raise ParameterError(
                ParameterError.__strerror__.format('application-name'))
        if not isinstance(application_version, str) or not singlet.__version_format_checker__(
                application_version):
            raise ParameterError(
                "application-version provided is not in valid version format such as 1.0, 2.8.9, etc.")
        if not isinstance(application_description, str):
            raise ParameterError(
                ParameterError.__strerror__.format('application-description'))
        
        if not isinstance(parent, singlets) and parent is not None:
            raise ParameterError(f"parent parameter must be of the type 'singlets' or None.")

        self.name = name
        self.parent = parent
        self.helptext = helptext
        self.reference = reference[skip:]

        self.collection: typing.Dict[str, typing.Union[singlet, singlets]] = {}
        self.base = None

        self.__ispresent__ = False
        self.auto_help = auto_help
        self.help_notations = help_notations
        self.application_name = application_name
        self.application_version = application_version
        self.application_description = application_description


    # The __singlet__ method is responsible for registering a singlet object into the
    # collection.


    def __singlet__(self, name, *notations, base=False, capture='auto',
                    helptext='', required=False, default=...) -> typing.Self:
        if not isinstance(base, bool):
            raise ParameterError(
                '\'base\' parameter must be of type <class \'bool\'>.')

        if base:
            if self.base is None:
                self.base = name
            else:
                raise RuntimeError(f"base argument for group '{self.name}' has already been registered.")

        self.collection[name] = singlet(
            name,
            *notations,
            capture=capture,
            helptext=helptext,
            required=required if base else False,
            default=default,
            reference=self.reference,
            skip=0,
            auto_help=False,
            help_notations=self.help_notations,
            application_name=self.application_name,
            application_version=self.application_version,
            application_description=self.application_description)
        
        if self.base is name:
            self.__ispresent__ = self.collection[self.base].__ispresent__


        # check for requirement
        # only for other arguments than the base, as it will be handled
        # by singlet itself.
        if not base and required and self.__present__ and self.collection[name].__notpresent__:
            raise ArgumentError(f"Any one of {notations} is mandatory in when using {self.collection[self.base].__notation__}.")

        return self


    # The __singlets__ method is responsible for registeing a singlets object into
    # the collection.


    def __singlets__(self, name, parent=None, helptext='') -> typing.Self:
        if parent is None:
            parent = self

        self.collection[name] = singlets(name, parent, helptext, self.reference, 0, self.auto_help,
                                         self.help_notations, self.application_name, self.application_version, self.application_description)
        return self


    # The __helptext__ method is responsible for printing the collective helptext of all objects
    # in the collection and exit.


    def __helptext__(self, exit, exit_code=0, acknowledgement=True, usage=True) -> None:
        if self.base is None:
            raise ArgumentError(f"No base argument defined for argument group '{self.name}'; Failure to generate heltext.")

        if acknowledgement:
            print(f"\n{self.application_name} v{self.application_version}")
            print(f"{self.application_description}\n")


        adder = ''.join(f"[{notation}]" for notation in self.help_notations) if self.help_notations else ''

        usage_string_list = []
        terminal_width = shutil.get_terminal_size().columns - 10 - len(self.application_name) - 1

        usage_text = ''
        notation_texts = [(f" | ".join(self.help_notations), "show this helptext and exit.")] if self.help_notations else []
        maxlength = max((len(n) for n, _ in notation_texts), default=0)

        groups: typing.List[singlets] = []

        # show info about the parent if present, that this group
        # can only be used with the parent group.

        usage_text += self.collection[self.base].__usage__
        
        for arg_or_grp in self.collection.values():
            if isinstance(arg_or_grp, singlet):
                if arg_or_grp.name is not self.base:
                    _local_usage_text = arg_or_grp.__usage__
                    if len(usage_text + _local_usage_text) > terminal_width:
                        usage_string_list.append(usage_text)
                        usage_text = _local_usage_text
                    else:
                        usage_text += _local_usage_text
                
                notation = ' | '.join(arg_or_grp.notations)
                notation_texts.append((notation, arg_or_grp.helptext))
                maxlength = max(maxlength, len(notation))

            else:
                groups.append(arg_or_grp)


        if len(usage_text + adder) > terminal_width:
            usage_string_list.extend([usage_text, adder])
        else:
            usage_string_list.append(usage_text + adder)

        if usage:
            print(f"usage:".ljust(9), self.application_name, usage_string_list[0])
            for line in usage_string_list[1:]:
                print(''.ljust(10 + len(self.application_name)), line)

        if self.parent is not None:
            print("\n" if usage else "", 'syntax: ...', '<' + self.parent.name + ' group (parent)>', '<' + self.name + ' group>')
            print("This argument group can only be used when the parent group is used.")

        print(f"\n{self.name}\n{self.helptext}\n")

        for notation, text in notation_texts:
            print(f"{notation.ljust(maxlength + 3)}: {text}")


        if groups:
            for grp in groups:
                grp.__helptext__(exit=False, acknowledgement=False, usage=False)

        if exit is True:
            sys.exit(exit_code)


    # The __parse__ method is responsible for handling full fledged parsing of all objects present
    # in the collection and return it.


    def __parse__(self, reference, order=None):
        # Format:
        # order = ( A, B, (C, a, b), D)
        # where A, B, D are singlet and (C, a, b) is a singlets object with C as its name.
        # Returns: (rA, rB, rC, rD), where r<anything> is result.


        if order:
            values = []
            for order_item in order:
                
                if isinstance(order_item, tuple):
                    name = order_item[0]
                    child_order = order_item[1:]

                    recursive_object = self.__object__(name)

                    # must exist
                    if recursive_object is None:
                        raise ParseError(f"no object with name {name} is registered in the collection pool.")
                    
                    # must be singlets
                    if not isinstance(recursive_object, singlets):
                        raise ParseError(f"object with name {name} is not a singlets object, a tuple structure is not necessary.")
                    
                    values.append(recursive_object.__parse__(reference, order=child_order))
                    continue

                obj = self.__object__(order_item)

                if obj is None:
                    raise ParseError(f"no object with name {name} is registered in the collection pool.")

                if isinstance(obj, singlet):

                    if obj.__present__ and self.auto_help and self.help_notations and obj.__parse__(*reference, capture_type='single', raise_errors=False) in self.help_notations:
                        self.__helptext__(exit=True)

                    values.append(obj.__parse__(*reference))
                else:
                    raise ParseError(f"singlets object with name {name} cannot be parsed fully as order is being used. Instead of providing just the name of the singlets object, provide a tuple, where the first element is the singlet's object name and all other elements represent the order of that particular singlets object.")
            return tuple(values)
        else:
            values = {}
            for name, obj in self.collection.items():
                if isinstance(obj, singlet):
                    if obj.__present__ and self.auto_help and self.help_notations and obj.__parse__(*reference, capture_type='single', raise_errors=False) in self.help_notations:
                        self.__helptext__(exit=True)

                    values[name] = obj.__parse__(*reference)
                else:
                    values[name] = obj.__parse__(reference)
            return values


    # The __object__ method is responsible for returning the object with given name,
    # no matter where and how deep it exists starting its search from the collection.


    def __object__(self, name, /) -> typing.Union[singlet, 'singlets', None]:
        for _, obj in self.collection.items():
            if isinstance(obj, singlet) and obj.name is name:
                return obj
            elif isinstance(obj, singlets):
                if obj.name is name:
                    return obj
                
                potential_object = obj.__object__(name)
                if potential_object:
                    return potential_object
        return None


    # The below method is responsible for registering a singlet object under
    # a given singlets object (the singlets object can be present anywhere under
    # the collection tree).


    def __register_singlet_for_this_singlets_object__(self, singlets_object_name, singlet_object_name, *notations,
                                                      base=False, capture='auto', helptext='', required=False, default=...) -> typing.Self:
        if singlets_object_name is self.name:
            return self.__singlet__(singlet_object_name, *notations, base=base, capture=capture,
                                    helptext=helptext, required=required, default=default)
        
        potential_object = self.__object__(singlets_object_name)
        if potential_object and isinstance(potential_object, singlets):
            potential_object.__singlet__(singlet_object_name, *notations, base=base, capture=capture, helptext=helptext, required=required, default=default)
            return self
        raise RuntimeError(f"Either singlets object with name {singlets_object_name} does not exist or is not a singlets object at all.")


    # The below method is responsible for registering a singlets object under
    # a given singlets object (the parent singlets object can be present anywhere
    # under the collection tree).


    def __register_singlets_for_this_singlets_object__(self, parent_singlets_object_name, child_singlets_object_name, helptext='') -> typing.Self:
        if parent_singlets_object_name is self.base:
            return self.__singlets__(child_singlets_object_name, self, helptext=helptext)
        
        potential_object = self.__object__(parent_singlets_object_name)
        if potential_object and isinstance(potential_object, singlets):
            potential_object.__singlets__(child_singlets_object_name, potential_object, helptext)
            return self
        raise RuntimeError(f"Either singlets object with name {parent_singlets_object_name} does not exist or is not a singlets object at all.")
