#!/usr/bin/env python3
from __future__ import annotations

import logging
import os
from typing import Iterable

import babel
from typing_extensions import Self

from localecmd.func import Function
from localecmd.localisation import N_, _, language_list, setup_translations
from localecmd.module import Module
from localecmd.parsing import convert_args, parse_line
from localecmd.topic import Topic

module_logger = logging.getLogger("cli")

DEFAULT_LOCALE_DIR = "locale"


def find_distributor_functions(function_names: Iterable[str] = []) -> set[str]:
    """
    Make list of distributor functions.

    These are functions that exist for convenience. Instead of having to
    type "edit_stops" one can type "edit stops". Here "edit" is the distributor.
    This behaviour is only implemented for one underscore so max two words can be
    concatenated.

    :param Iterable[str] function_names: Names of all functions. If dict, the list of keys are used.
    :returns: Set of distributor functions
    :rtype: set[str]

    """
    distributors = set()
    for fname in function_names:
        if "_" in fname:
            short_name = fname.split("_", 1)[0]
            distributors.add(short_name)
    module_logger.debug(f"Found distributor functions {distributors}")
    return distributors


class CLI:
    """
    Represents a command line interface (CLI).

    Only one CLI at the time can exist.

    To start the CLI and run it in an infinite loop, run
    :::{code} python
    >>> cli = CLI([])

    >>> cli.cmdloop() # doctest: +SKIP

    :::{note}
    The CLI comes without builtin functions. The functions the CLI should have
    are passed to class constructor [as described in the header](#add-functions-to-cli).
    :::

    To quit the CLI loop, the function must raise `SystemExit`.

    """

    modules: list[Module] = []
    "List of loaded modules"

    functions: dict[str, Function] = {}
    "Dictionary of functions the CLI knows"

    topics: dict[str, Topic] = {}
    "Dictionary of topics with help texts"

    distributors: set = set()
    """First word of functions."""

    # Should be a class property, but that does not exist in python...
    running = False
    "Tells if a CLI is running"

    language = ""
    "Language of CLI"

    localedir = "locale"
    "directory where translation files are"

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls.running:
            msg = "There is a CLI running already! Stop that before starting a new one"
            module_logger.info(msg)
            raise RuntimeError(msg)
        obj = super().__new__(cls)
        cls.running = True
        cls._instance = obj
        return obj

    def __init__(
        self,
        modules: list,
        language: str = "",
        prompt: str = N_("¤ "),
        greeting: str = "",
        localedir: str = "locale",
        gettext_domains: Iterable[str] = [],
    ) -> None:
        """
        Start command line interface.

        Loads correctly decorated function from within the modules. Modules must be
        prepared [as described](#add-functions-to-cli).

        Help and quit functions are built in to the CLI, but may be overwritten.

        :param list modules: List of modules to load functions from.
        :param str language: What language the console is in.
        :param str prompt: What to show when querying for input. Defaults to
        the generic currency sign "¤ " which also is a translatable string.
        :param str greeting: Message to show when starting the CLI
        :param str localedir: Directory where translation files for
        the program are.
        :param Iterable[str] gettext_domains: Gettext domains that are used
        in addition to those provided by localecmd.
        Their language will be changed along with the localecmd domains.
        """
        # Make sure that translations work when starting cli.
        # CLI must change language to user language when starting up
        # This does no checks for existing files since fallback is True
        setup_translations([""], localedir, gettext_domains)

        module_logger.info("Starting command-line interface")
        module_logger.debug(f"Language: {language}")
        module_logger.debug(f"Locale directory: {localedir}")
        module_logger.debug(f"Gettext domains: {gettext_domains}")

        # Must save the modules to be able to load them again (translated) at a later point
        for module in modules:
            if not isinstance(module, Module):
                module = Module.from_module(module)
            CLI.modules.append(module)

        CLI.localedir = localedir
        self.greeting = greeting

        self.prompt = prompt

        self.domains: set[str] = set(gettext_domains)

        self.log: list[str] = []
        change_cli_language(language)

    @staticmethod
    def get_cli() -> Self:  # type: ignore
        """
        Return instance of running CLI.

        :raises RuntimeError: If CLI is not running.
        """
        if not CLI.running:
            raise RuntimeError("CLI is not running!")
        return CLI._instance  # type: ignore

    def _load_functions(self) -> None:
        for module in CLI.modules:
            if CLI.language:
                # Load docstrings
                lines = module.load_docs_from_file(CLI.language, CLI.localedir)
                msg = "Assign loaded docs for module {module.name}"
                module_logger.info(msg)
                module.assign_docs(lines, "###")
            else:
                msg = "Load coded docstrings for module {module.name}"
                module_logger.info(msg)
                module.empty_docs()
            # Load functions
            for func in module.functions:
                fname = func.translated_name
                msg = f"Loading function {fname} from module {module.name}"
                module_logger.debug(msg)
                CLI.functions[fname] = func
            for topic in module.topics:
                name = topic.translated_name
                msg = f"Loading topic {name} from module {module.name}"
                module_logger.debug(msg)
                CLI.topics[name] = topic
        # Find distributors
        CLI.distributors.update(find_distributor_functions(CLI.functions))

    def reload_functions(self) -> None:
        """
        Clear all loaded functions and load them again.

        This is needed when switching language to get them in the current language.
        """
        CLI.functions.clear()
        CLI.distributors.clear()
        CLI.topics.clear()
        self._load_functions()

    def close(self) -> None:
        """
        Stop CLI from running and turn it off
        """
        module_logger.warning("Closing command-line interface")

        CLI.functions.clear()
        CLI.modules.clear()
        CLI.distributors.clear()
        CLI.running = False
        CLI.language = ""
        CLI.localedir = DEFAULT_LOCALE_DIR
        CLI._instance = None

    def runcmd(self, line: str, *, localed_input: bool = True) -> None:
        """
        Run a command as if it were the input to the prompt.

        :param str line: The input to the prompt
        :param bool localed_input: If True, it tells that the line is in the language of the cli.
        If False, it is the fallback language in which the functions are written
        (typically English).
        Default is True
        """
        self.log.append(line)
        try:
            ret = parse_line(line, self.functions, CLI.distributors)
        except ValueError:
            # Can be missing end quotation or EOF in escaping character.
            # Escaping is not supported, so it must be missing end quotation
            msg = N_("Missing end quotation mark.")
            module_logger.error(msg)
            print(_(msg))
            return

        if ret is None:
            msg = N_("Line could not be parsed!")
            module_logger.error(" ".join([msg, line]))
            print(_(msg))
            return

        func, args, kwargs = ret

        # Execute command
        try:
            if localed_input:
                args, kwargs = func.translate_call(*args, **kwargs)

            # Convert types
            args, kwargs = convert_args(func, *args, **kwargs)

            func(*args, **kwargs)
        except SystemExit as e:
            raise e
        except Exception as e:
            print(_("Error while executing:"), *e.args)

    def cmdloop(self) -> None:  # pragma: no cover
        """
        A loop querying user for commands. Uses python builtin `input` to query
        user.

        The loop stops when `input` raises `EOFError` or when a function raises
        `SystemExit`.
        """
        # Can't test this as it is querying for user input
        print(self.greeting)
        loop = True
        while loop:
            try:
                line = input(_(self.prompt))
            except EOFError:
                loop = False
                print()
                continue

            try:
                self.runcmd(line)
            except SystemExit:
                loop = False


def restart_cli(*args, **kwargs) -> CLI:
    """
    Close and restart CLI

    For parameter list, see CLI initialisation.
    :return: Object with CLI properties
    :rtype: CLI

    """
    if CLI.running:
        old_cli: CLI = CLI.get_cli()
        old_cli.close()

    new_cli: CLI = CLI(*args, **kwargs)
    return new_cli


def change_cli_language(language: str, fallback: bool = False) -> None:
    """Change language of program

    A message will be printed in the new language
    saying what is the current language of the CLI.


    :param str language: Folder name inside of `locale/` containing the
    translation strings.
    :param bool fallback: Fall back to English if language could not be loaded?
    Defaults to False if the specified language is non-empty, else True.
    """

    cli: CLI = CLI.get_cli()
    localedir = CLI.localedir

    # If language string is empty, automatically fall back to internals
    if len(language) == 0:
        fallback = True

    supported_languages = language_list(localedir, include_fallback=True)

    # Expand language
    full_lc = babel.negotiate_locale([language], supported_languages)
    # If no result, then use fallback since English is not implemented yet.
    if full_lc is None:
        if fallback:
            # Could not expand language since it is the fallback language
            full_lc = ""
        else:
            # Could not expand language code because it is not implemented
            path = os.path.join(localedir, language, "LC_MESSAGES")
            msg = N_(
                "Could not switch to language code {language}. Check that all files are in {path}."
            )
            module_logger.info(msg.format(path=path, language=language))
            print(_(msg).format(path=path, language=language))
            print(os.getcwd())
            return

    setup_translations([full_lc], localedir, cli.domains)

    CLI.language = full_lc
    cli.reload_functions()
    if full_lc:
        langname = str(babel.Locale.parse(full_lc).get_display_name())
    else:
        langname = "fallback language"
    msg = N_("The language of the command line is {langname}")
    print(_(msg).format(langname=langname))


def run_script(script: str, *, localed_input: bool = True):
    """
    Run every line of the script as its own command

    :param str script: The script to run. Commands are divided by newlines (\\n)
    :param bool localed_input: If True, it tells that the script is in the language of the cli.
    If False, it is the fallback language in which the functions are written (typically English).
    Default is True.


    """
    cli: CLI = CLI.get_cli()
    for line in script.split('\n'):
        cli.runcmd(line, localed_input=localed_input)


# Hard to test this automatically too. Is done manually...


def create_docs(directory: str = "docs/source/functions") -> None:  # pragma: no cover
    """
    Save in-program docstrings into files

    Function is not finished. Docs will come later. Look at code instead.
    """
    # Maybe this should be a parameter?
    modules = CLI.modules

    module_logger.debug("Create files with in-program documentation")
    if not os.path.isdir(directory):
        module_logger.debug(f"Creating directory {directory}")
        os.mkdir(directory)
    if os.listdir(directory):
        msg = f"The directory {directory} is not empty! Cannot proceed!"
        module_logger.warning(msg)
        return
    # We have guaranteed an empty directory, but keep this anyway
    for module in modules:
        filename = os.path.join(directory, module.name + ".md")
        if os.path.isfile(filename):
            msg = f"File {filename} exists and will be replaced"
            module_logger.warning(msg)
            os.remove(filename)

        # Actual work: Printing docstrings
        with open(filename, "w") as file:
            file.write("# Module " + module.name + "\n")
            file.write(module.exported_md)
            file.write("\n\n")
            # Should print overview of functions here

            for func in module.functions + module.topics:
                msg = f"Write doc of function {func.fullname} into {filename}"
                module_logger.debug(msg)
                file.write(func.exported_md + "\n\n")

    # Write index file
    filename = os.path.join(directory, "index.md")
    with open(filename, "w") as file:
        module_logger.debug("Write general index for the modules")
        file.write("# API of Functions in program\n")
        file.write(":::{toctree}\n")
        file.write(":caption: Modules\n\n")
        for module in modules:
            file.write(f"{module.name}.md\n")
        file.write(":::\n")
