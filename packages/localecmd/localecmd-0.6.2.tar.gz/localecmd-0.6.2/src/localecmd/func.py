# !/usr/bin/env python3
from __future__ import annotations

import inspect
import logging
from typing import Callable

from localecmd.doc_translation import translate_examples, translate_parameters
from localecmd.localisation import _, f_
from localecmd.topic import Topic

BRAILLE_PATTERN_BLANK = "⠀"

module_logger = logging.getLogger("Function")


class Function(Topic):
    """
    Function callable from the CLI.

    This is a wrapper around the python builtin function with the advantage that
    function name, parameters and types can be translated. It adds some properties
    that are useful for translation.

    Attributes `__name__` and `__doc__` are left unchanged. To access the shown
    name, use {py:attr}`Function.name` (untranslated) or
    {py:attr}`Function.translated_name`.

    To call the function from python, use the function as every other function.
    Then, args and kwargs are passed directly.

    :param Callable func: The original function
    :param str name: Untranslated name as it will be shown in the program
    :param list[str] parameters: Untranslated function parameters
    """

    def __init__(self, func: Callable, name: str = "", translate_function: Callable = f_) -> None:
        """
        Initialize function.

        :param Callable func: Actual function that will be called
        :param str name: Name of the function as shown in program.
        If empty, the name will be as shown in python.
        :param Callable | None translate_function: Function to translate function
        name and parameter names. For more information, see below.
        Defaults to {py:func}`localecmd.localisation.f_`.

        The translation function must take two arguments: First the context,
        then the string to translate.
        For functions, the context is the module name, for parameter names, this
        is `<module name>.<funcion name>`.
        """
        # Mypy likes this
        assert inspect.isfunction(func)
        self.func = func

        # Tell Python where to find signature, annotations etc.
        self.__wrapped__ = func

        # Keep name, module and doc
        self.__name__ = func.__name__
        self.__module__ = func.__module__
        self.__doc__ = func.__doc__

        # For translation
        self.__translated_doc__ = ""

        # Function name in the program
        if not name:
            name = func.__name__

        super().__init__(name, func.__doc__)
        self.f_ = translate_function
        self.sphinx_directive = 'py:function'

        self.signature = inspect.signature(func)
        # Function parameters
        self.parameters = list(self.signature.parameters.keys())

    def __call__(self, *args, **kwargs):
        """
        Call wrapped function directly.

        raises TypeMismatch: If type of arguments does not comply with function type annotations.
        """
        # Todo: Add logging
        return self.func.__call__(*args, **kwargs)

    def translate_call(self, *args, **kwargs):
        # Translate kwargs
        try:
            kwargs = {self.parameter_dictionary[k]: v for k, v in kwargs.items()}
        except KeyError as e:
            msg1 = _("Function '{fname}' has no parameter '{param}'!")
            msg2 = _("Possible parameters are: {params}")
            fmsg = '\n'.join([msg1, msg2]).format(
                fname=self.translated_name,
                param=e.args[0],
                params=list(self.parameter_dictionary.keys()),
            )
            raise KeyError(fmsg) from e

        return args, kwargs

    @property
    def exported_md(self) -> str:
        """The helptext exported into markdown format.

        For export to sphinx documentation.
        Myst Markdown with colon fences is used.

        The sphinx directive used is
        """
        # Title is calling plus blank Braille-pattern
        header = ':::{' + self.sphinx_directive + '} ' + f'{self.title}\n\n'
        body = translate_examples(
            translate_parameters(self.doc, self.fullname),
            self.translated_name,
            self.fullname,
        )
        footer = '\n:::'
        return header + body + footer

    @property
    def calling(self) -> str:
        """Generate signature of function

        Signature is on the form\n
        func positional args... -kwarg1 -kwargs...
        """
        s = self.translated_name + " "
        sig = inspect.signature(self)

        for p in sig.parameters.values():
            if p.kind in [
                inspect.Parameter.KEYWORD_ONLY,
                inspect.Parameter.VAR_KEYWORD,
            ]:
                s += "-"
            s += self.f_(self.fullname, p.name)
            if p.kind == inspect.Parameter.VAR_POSITIONAL:
                s += "..."
            if p.kind == inspect.Parameter.VAR_KEYWORD:
                s += "..."
            s += " "
        return s

    @property
    def parameter_dictionary(self) -> dict[str, str]:
        """Dictionary with translated -> untranslated parameter names

        :rtype: dict[str, str]

        """
        return {self.f_(self.fullname, p).replace('_', '-'): p for p in self.parameters}

    @property
    def translated_name(self) -> str:
        """Translated name"""
        return self.f_(self.modulename, self.name)

    @property
    def title(self) -> str:
        """Header for the section in the docs"""
        return self.calling + BRAILLE_PATTERN_BLANK


def programfunction(name: str = "", translate_function: Callable = f_) -> Callable:
    """
    Wrap function such that it becomes a {py:class}`Function`.

    The decorator must be used with parentheses also when no arguments are passed:
    :::{code} python
    @programfunction()
    def some_function():
        (...)
    :::
    See {py:class}`there <Function>` under Initialization for argument description.

    """

    def decorator(func: Callable) -> Function:
        f = Function(func, name, translate_function)
        return f

    return decorator
