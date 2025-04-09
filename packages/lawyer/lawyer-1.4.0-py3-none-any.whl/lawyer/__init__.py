
from lawyer.parsers import singlet, singlets
from lawyer.exceptions import InstanceError, ParameterError, ExistsError, ArgumentError, ParseError
import sys, typing, traceback, linecache


_modify = False
original_excepthook = sys.excepthook

def minimal_traceback(exception: typing.Type[Exception], *args: object) -> typing.NoReturn:
    
    def internal_callback(exc_type, exc_value, exc_tb):

        # Get full traceback frames
        tb_list = traceback.extract_tb(exc_tb)

        # Get the outermost user-call frame (first frame in the traceback)
        user_frame = tb_list[0]  # index 0 = where error was triggered in user code

        # Print traceback header
        print("Traceback (most recent call last):")

        # Show only user's line (not internal frames)
        if sys.platform in ('darwin', 'linux'):
            import colorama
            colorama.init()
            print(f'  File "{colorama.Fore.RED}{user_frame.filename}{colorama.Fore.RESET}", line {colorama.Fore.RED}{user_frame.lineno}{colorama.Fore.RESET}, in {colorama.Fore.RED}{user_frame.name}{colorama.Fore.RESET}')
        else:
            print(f'  File "{user_frame.filename}", line {user_frame.lineno}, in {user_frame.name}')

        code_line = user_frame.line or linecache.getline(user_frame.filename, user_frame.lineno).strip()
        print(f'    {code_line}')
        if sys.platform in ('darwin', 'linux'):
            print('    ' + colorama.Fore.RED + ''.join('^' if c != ' ' else ' ' for c in code_line) + colorama.Fore.RESET)
        else:
            print('    ' + ''.join('^' if c != ' ' else ' ' for c in code_line))

        # Print final exception message
        if sys.platform in ('darwin', 'linux'):
            if exc_value:
                print(f"{colorama.Fore.RED}{exc_type.__name__}{colorama.Fore.RESET}: {colorama.Fore.RED}{exc_value}{colorama.Fore.RESET}")
            else:
                print(f"{colorama.Fore.RED}{exc_type.__name__}{colorama.Fore.RESET}")
            colorama.deinit()
        else:
            if exc_value:
                print(f"{exc_type.__name__}: {exc_value}")
            else:
                print(f"{exc_type.__name__}")

        global original_excepthool
        sys.excepthook = original_excepthook

    sys.excepthook = internal_callback
    raise exception(*args)


class Judge:


    @property
    def __readonly__(self) -> None:
        return None


    @__readonly__.setter
    def __readonly__(self, value, /) -> typing.NoReturn:
        return minimal_traceback(AttributeError, f"attributes of Judge class are read-only, cannot assign '{value}' to attribute.")


    @__readonly__.deleter
    def __readonly__(self) -> typing.NoReturn:
        return minimal_traceback(AttributeError, f"attributes of Judge class are read-only and frozen, cannot delete attribute.")


    @property
    def __application__(self) -> str:
        global _modify
        _modify = True
        value = getattr(self, '-8645880369160574959', sys.argv[0])
        _modify = False
        return value


    @__application__.setter
    def __application__(self, name, /) -> typing.NoReturn:
        if not isinstance(name, str):
            return minimal_traceback(AttributeError, f"application name must be of type <class 'str'>.")
        
        global _modify
        _modify = True
        setattr(self, '-8645880369160574959', name)
        _modify = False


    @__application__.deleter
    def __application__(self) -> typing.NoReturn:
        del self.__readonly__


    @property
    def __version__(self) -> str:
        global _modify
        _modify = True
        value = getattr(self, '-8059281209987537947', '1.0')
        _modify = False
        return value


    @__version__.setter
    def __version__(self, version, /) -> typing.NoReturn:
        if not singlet.__version_format_checker__(version):
            return minimal_traceback(AttributeError, f"version must be in valid format and must be of type <class 'str'>.")
        
        global _modify
        _modify = True
        setattr(self, '-8059281209987537947', version)
        _modify = False


    @__version__.deleter
    def __version__(self) -> typing.NoReturn:
        del self.__readonly__


    @property
    def __description__(self) -> str:
        global _modify
        _modify = True
        value = getattr(self, '-7681659577293593483', '')
        _modify = False
        return value


    @__description__.setter
    def __description__(self, desc, /) -> typing.NoReturn:
        if not isinstance(desc, str):
            return minimal_traceback(AttributeError, f"description must be of type <class 'str'>.")
        
        global _modify
        _modify = True
        setattr(self, '-7681659577293593483', desc)
        _modify = False


    @__description__.deleter
    def __description__(self) -> typing.NoReturn:
        del self.__readonly__


    @property
    def __reference__(self) -> typing.Iterable[str]:
        global _modify
        _modify = True
        value = getattr(self, '-4799753283422340294', sys.argv)
        _modify = False
        return value


    @__reference__.setter
    def __reference__(self, value, /) -> typing.NoReturn:
        self.__readonly__ = value


    @__reference__.deleter
    def __reference__(self) -> typing.NoReturn:
        del self.__readonly__


    def __setattr__(self, name: str, value: typing.Any, /) -> None:
        global _modify
        allowed_hashes = ('-7868989330756850304', '-8645880369160574959', '-8059281209987537947', '-7681659577293593483', '-4799753283422340294', '-1473320931206488208', '8587656167592366246')
        allowed_properties = ('__reference__', '__collection__', '__application__', '__version__', '__description__', '__readonly__', '__autohelp__', '__help_notations__')
        if name in allowed_hashes and _modify is False:
            return minimal_traceback(AttributeError, f"cannot assign '{value}' to a placeholder.")
        elif name not in allowed_hashes + allowed_properties:
            return minimal_traceback(AttributeError, f"cannot assign '{value}' to attribute {name} as Judge class is read-only.")
        return super().__setattr__(name, value)


    def __getattribute__(self, name: str, default=None, /) -> typing.Any:
        global _modify
        denied_hashes = ('-7868989330756850304', '-8645880369160574959', '-8059281209987537947', '-7681659577293593483', '-4799753283422340294', '-1473320931206488208', '8587656167592366246')
        if name in denied_hashes and _modify is False:
            return minimal_traceback(AttributeError, f"cannot access attribute {name}. object with name {name} is just a placeholder.")
        try:
            return super().__getattribute__(name)
        except Exception:
            return default


    @property
    def __collection__(self) -> typing.Dict[str, typing.Union[singlet, singlets]]:
        global _modify
        _modify = True
        if hasattr(self, '-7868989330756850304'):
            value = getattr(self, '-7868989330756850304')
            _modify = False
            return value
        else:
            setattr(self, '-7868989330756850304', {})
            value = getattr(self, '-7868989330756850304')
            _modify = False
            return value


    @__collection__.setter
    def __collection__(self, col, /) -> typing.NoReturn:
        self.__readonly__ = col


    @__collection__.deleter
    def __collection__(self) -> typing.NoReturn:
        del self.__readonly__


    @property
    def __autohelp__(self) -> bool:
        global _modify
        _modify = True
        if hasattr(self, '-1473320931206488208'):
            value = getattr(self, '-1473320931206488208')
        else:
            setattr(self, '-1473320931206488208', False)
            value = False
        _modify = False
        return value


    @__autohelp__.setter
    def __autohelp__(self, auto_help) -> None:
        if not isinstance(auto_help, bool):
            return minimal_traceback(AttributeError, f"__autohelp__ accepts boolean values only.")
        global _modify
        _modify = True
        setattr(self, '-1473320931206488208', auto_help)
        _modify = False


    @__autohelp__.deleter
    def __autohelp__(self) -> typing.NoReturn:
        del self.__readonly__


    @property
    def __help_notations__(self) -> typing.Iterable[str]:
        global _modify
        _modify = True

        if hasattr(self, '8587656167592366246'):
            value = getattr(self, '8587656167592366246')
        else:
            setattr(self, '8587656167592366246', ('--help', '-h'))
            value = ('--help', '-h')
        _modify = False
        return value


    @__help_notations__.setter
    def __help_notations__(self, help_notations) -> None:
        if not (isinstance(help_notations, typing.Iterable) and all(isinstance(help_notation, str) for help_notation in help_notations)):
            return minimal_traceback(AttributeError, f"__help_notations__ accepts an iterable of strings.")
        
        global _modify
        _modify = True
        setattr(self, '8587656167592366246', help_notations)
        _modify = False


    @__help_notations__.deleter
    def __help_notations__(self) -> typing.NoReturn:
        del self.__readonly__


    def __init__(self, application_name=sys.argv[0], application_version='1.0',
                 application_description='', reference=sys.argv, skip=1, auto_help=False, help_notations=()) -> None:

        if not isinstance(application_name, str):
            return minimal_traceback(ParameterError, f"application-name parameter must be of type <class 'str'>.")
        if not singlet.__version_format_checker__(application_version):
            return minimal_traceback(ParameterError, f"application-version parameter must a valid version string.")
        if not isinstance(application_description, str):
            return minimal_traceback(ParameterError, f"application-description parameter must be of type <class 'str'>.")
        if not (isinstance(reference, typing.Iterable) and all(isinstance(ref, str) for ref in reference)):
            return minimal_traceback(ParameterError, f"reference parameter must be an iterable of strings.")
        if not isinstance(skip, int):
            return minimal_traceback(ParameterError, "skip parameter must be of type <class 'int'>.")

        global _modify
        _modify = True

        setattr(self, '-8645880369160574959', application_name)
        setattr(self, '-8059281209987537947', application_version)
        setattr(self, '-7681659577293593483', application_description)
        setattr(self, '-4799753283422340294', reference[skip:])
        setattr(self, '-1473320931206488208', auto_help)
        setattr(self, '8587656167592366246', help_notations or ('--help', '-h'))
        setattr(self, '-7868989330756850304', {})


        _modify = False


    def add_argument(self, name: str, *notations: str, capture: typing.Literal['auto', 'single', 'boolean'] = 'boolean',
                     helptext='', required=False, default: typing.Any = ..., parent=None, base=False) -> typing.Self:
        
        if not (isinstance(parent, str) or parent is None):
            return minimal_traceback(ParameterError, f"parent can either be an argument group name or None.")
        
        if parent is not None:
            parent_object = self.object(parent)
            if parent_object is None:
                return minimal_traceback(InstanceError, f"object with name '{parent}' not found in the object tree.")
            if not isinstance(parent_object, singlets):
                return minimal_traceback(InstanceError, f"object with name '{parent}' is not an argument group.")
            
            if name in parent_object.collection:
                return minimal_traceback(ParameterError, f"argument or group with name '{name}' already exists under parent '{parent}'")
            
            try:
                parent_object.__singlet__(name, *notations, base=base, capture=capture, helptext=helptext, required=required, default=default)
            except ParameterError as p_error:
                return minimal_traceback(ParameterError, *p_error.args)
            except ArgumentError as a_error:
                return minimal_traceback(ArgumentError, *a_error.args)
            except RuntimeError as r_error:
                return minimal_traceback(RuntimeError, *r_error.args)
            except Exception as e:
                return minimal_traceback(Exception, *e.args)
            return self


        if name in self.__collection__:
            return minimal_traceback(ExistsError, f"argument or group with name '{name}' already exists.")

        try:
            self.__collection__[name] = singlet(name, *notations, capture=capture, helptext=helptext, required=required,
                                                default=default, auto_help=self.__autohelp__, help_notations=self.__help_notations__, application_name=self.__application__,
                                                application_version=self.__version__, application_description=self.__description__)
        except ParameterError as p_error:
            return minimal_traceback(ParameterError, *p_error.args)
        except ArgumentError as a_error:
            return minimal_traceback(ArgumentError, *a_error.args)
        except RuntimeError as r_error:
            return minimal_traceback(RuntimeError, *r_error.args)
        except Exception as e:
            return minimal_traceback(Exception, *e.args)
        return self

    def object(self, name: str, /) -> typing.Union[singlet, singlets, None]:
        if name in self.__collection__:
            return self.__collection__[name]
        
        for _object in self.__collection__.values():
            if isinstance(_object, singlets):
                potential_object = _object.__object__(name)
                if potential_object is not None:
                    return potential_object
        return None


    def add_group(self, name: str, parent=None, helptext='') -> typing.Self:
        if not (isinstance(parent, str) or parent is None):
            return minimal_traceback(ParameterError, f"parent can either be an argument group name or None.")
        
        if parent is not None:
            parent_object = self.object(parent)

            if parent_object is None:
                return minimal_traceback(InstanceError, f"object with name '{parent}' not found in the object tree.")
            if not isinstance(parent_object, singlets):
                return minimal_traceback(InstanceError, f"object with name '{parent}' is not an argument group.")
            
            if name in parent_object.collection:
                return minimal_traceback(ParameterError, f"argument or group with name '{name}' already exists under parent '{parent}'.")
            
            try:
                parent_object.__singlets__(name, helptext=helptext)
            except ParameterError as p_error:
                return minimal_traceback(ParameterError, *p_error.args)
            except Exception as e:
                return minimal_traceback(Exception, *e.args)
            return self


        if name in self.__collection__:
            return minimal_traceback(ParameterError, f"argument or group with name '{name}' already exists.")
        
        try:
            self.__collection__[name] = singlets(name, None, helptext, self.__reference__, 0, self.__autohelp__, self.__help_notations__, self.__application__, self.__version__, self.__description__)
        except ParameterError as p_error:
            return minimal_traceback(ParameterError, *p_error.args)
        except Exception as e:
            return minimal_traceback(Exception, *e.args)
        return self


    def parse(self, *order):
        if order:

            values = []

            for item in order:

                if isinstance(item, tuple) and all(isinstance(item_item, str) for item_item in item):
                    item_name = item[0]
                    item_order = item[1:]
                    potential_object = self.object(item_name)
                    if potential_object is None:
                        return minimal_traceback(ParseError, f"no object with name '{item_name}' found registered.")
                    elif isinstance(potential_object, singlet):
                        return minimal_traceback(ParseError, f"for parsing single arguments, their name is enough.")
                    else:
                        values.append(potential_object.__parse__(self.__collection__.values(), item_order))
                elif isinstance(item, str):
                    potential_object = self.object(item)
                    if potential_object is None:
                        return minimal_traceback(ParseError, f"no object with name '{item}' found registered.")
                    elif isinstance(potential_object, singlets):
                        return minimal_traceback(ParseError, f"for parsing grouped arguments use a tuple instead of just the name; The tuple's first element must be the group name and the item(s) to be parsed inside it should be after that.")
                    else:
                        values.append(potential_object.__parse__(*self.__collection__.values()))
                else:
                    return minimal_traceback(ParseError, f"the parse method accepts objects of type <class 'str'> or <class 'tuple'>.")

            if len(values) == 1:
                return values[0]
            else:
                return tuple(values)
        else:
            values = {}
            for item, item_object in self.__collection__.items():
                if isinstance(item_object, singlet):
                    values[item] = item_object.__parse__(*self.__collection__.values())
                else:
                    values[item] = item_object.__parse__(self.__collection__.values())
            return values