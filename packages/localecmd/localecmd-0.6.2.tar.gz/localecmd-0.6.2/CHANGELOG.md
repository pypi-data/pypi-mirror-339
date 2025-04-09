## 0.6.2 (2025-04-09)

### Fixes

- Fixed error that doctests were not detected in wrapped functions

## 0.6.1 (2025-04-05)

### Fixes

- Ignore empty type annotations
- Problems down to python 3.8
- Removed functionality that did not exist for python<3.11
- Support union type arguments with '|'

### Changes

- More linting and fix problems
- More linting with bug fixes

## 0.6.0 (2025-03-28)

### New features

- Add function that predicts command autocompletion

### Fixes

- Better error message when calling functions with wrong arguments

### Changes

- Factor out command completion to an own function
- Use dashes within kewyword arguments instead of underscores

## 0.5.0 (2025-03-26)

### Breaking change

- Translator function in module is no longer supported.

### New features

- Support boolean values
- Show list of distributor functions

## 0.4.0 (2025-03-22)

### New features

- Keyword arguments can now contain more than one argument per keyword

### Changes

- Type of arguments is now converted with function annotations (#2)

## 0.3.0 (2025-03-09)

### New features

- Allow handling of more domains than the internal ones

### Changes

- Switch to babel for gettext domain handling and language switching

## 0.2.0 (2025-03-06)

### New features

- Function to create all pot files at once
- Export module directly to library users
- Function t o run scripts
- Addability to optionally run commands in system/fallback language (typically english)
- **Function**: Give default translator function by library
- **Cli**: Allow to run commands directly with cli.runcmd
- **Cli**: Allow loading module objects in addition to modules
- **Pot**: Generate pot file for localecmd messages
- **Type-translation**: Create type list automatically
- **Pot**: Add function to generate pot files o ffunction names and parameters
- **Cli**: Add function to restart cli to start it even if it is running
- **Cli**: Include builtin functions and enable them by default
- Make important parts of library easier accessible

### Fixes

- **Parsing**: Negative numbers are not longer interpreted as keyword arguments
- **Parsing**: Solve name conflicts between function and distributor
- Load correct docstrings
- Markdown needs double newline to generate a newline and added missing type annotation
- **Docstrings**: Only show myst syntax in myst export
- Fix typing and removed missing imports
- **Cli**: Ensure that translators are enabled every time the cli starts
- Fix errors detected by mypy
- Stop overriding cli attributes when one tries to create second cli

### Changes

- Change default docstring folder
- Log executed commands
- Don't add space after command run
- Start_cli now retuns cli object
- **Pot**: Centralise pot file saving
- **Cli**: Closing cli now needs access to cli object
- **Cli**: Move cmdloop to method of cli but keep a wrapper of it
- **Cli**: Move static functions out of class
- Simplify calling
- **Function-translation**: Reorder if statements for better understanding
- **Language-switching**: Simplify fallback handling
