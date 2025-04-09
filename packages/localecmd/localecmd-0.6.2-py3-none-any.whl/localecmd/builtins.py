#!/usr/bin/env python3
"""
General functions in a command-line program.
"""

from rich import print as rprint
from rich.markdown import Markdown
from rich.table import Table

from localecmd.cli import CLI, change_cli_language
from localecmd.func import programfunction
from localecmd.localisation import _, f_, language_list
from localecmd.parsing import args_to_line, parse_line
from localecmd.topic import Topic

__translator_function__ = f_  # This line disables W0611

types = Topic(
    'types',
    """
    The type of positional and keyword arguments is converted to correct type 
    when the function is executed. 
    
    To see which types a function takes, look at its helptext with `help <function name>`.
    
    To get help about the type, write `help <type>`.
    """,
)
Bool = Topic.from_type(
    bool,
    """Boolean value
    
    The following strings are interpreted as `True`: 'yes'
    
    The following strings are interpreted as `False`: 'no'
    """,
)
Int = Topic.from_type(int, "Integer\n\nThe formatting is locale-aware.")
Float = Topic.from_type(float, "Floating-point number\n\nThe formatting is locale-aware.")
String = Topic.from_type(str, "String\n\nUnicode characters are allowed.")


@programfunction()
def help(*topic: str):
    """Get help

    :param str topic: Function/Topic to get help on. If empty, a list of all
    functions and topics is shown.

    :::{rubric} Examples
    :::
    :::{code} python
    Show list of all functions and topics
    >>> help()
    (...)
    Show helptext on function help.
    >>> help('help')
    (...)
    :::
    """

    functions = CLI.functions

    if not topic:
        print(_("Available topics:"))
        print(' '.join(CLI.topics.keys()))
        print()
        print(_("Available commands:"))
        print(' '.join(CLI.functions.keys()))
        print()

    elif topic[0] in functions:
        # Print docstring of one function
        func = functions[topic[0]]
        rprint(Markdown(func.program_doc))
    elif topic[0] in CLI.topics:
        # Print docstring of one function
        help_topic = CLI.topics[topic[0]]
        rprint(Markdown(help_topic.program_doc))
    else:
        print(_("Command {0} does not exist!").format(topic[0]))


@programfunction()
def quit():
    """Terminate program

    :raises SystemExit: Always
    """
    raise SystemExit


@programfunction()
def change_language(language: str = ""):
    """Change language of program

    :param str language: Folder name containing the translation strings.
    Must be subfolder of folder specified by CLI.localedir.
    Defaults to '' meaning the fallback language English.
    """
    change_cli_language(language)


@programfunction()
def list_languages(include_fallback: bool = True) -> None:
    """Print list of available program languages"""
    langs = language_list(include_fallback=include_fallback)
    table = Table(title=_("Supported languages in command line:"))
    table.add_column(_("Language code"), justify='left')
    table.add_column(_("Language name"), justify='left')
    for code in langs:
        table.add_row(code, code)  # Todo: reinsert the language name
    rprint(table)
    print()
    print(_('To change the language, type "change_language <language code>"'))


@programfunction()
def list_distributors() -> None:
    """Print list of distributor functions"""
    function_names = list(CLI.functions.keys())
    distributors = CLI.distributors

    table = Table(title=_("List of distributor functions"))
    table.add_column(_("Distributor"), justify='left')
    table.add_column(_("Functions"), justify='left')
    for dist in distributors:
        fns = ', '.join([n for n in function_names if n.startswith(dist + '_')])
        table.add_row(dist, fns)
    rprint(table)
    print()


@programfunction()
def complete(*words) -> None:
    """
    Predict command completion of the given words

    :::{rubric} Examples
    :::
    >>> complete complet
    complete
    >>> complete l l
    list_languages

    """
    line = ' '.join(words)
    ret = parse_line(line, CLI.functions, CLI.distributors)
    if ret is None:
        # Everything is printed already
        return
    func, args, kwargs = ret
    print(args_to_line(func.name, *args, **kwargs))
    # print(complete_command(words, CLI.functions.keys(), CLI.distributors)[0])
