# Django Project Initializer

**Author:** AdrianJames27

## Overview

The Django Project Initializer is a Python script that automates the setup of a new Django project. It performs the following tasks:

1. **Prompts** the user for a project name.
2. **Clones** a base Django template repository from [GitHub](https://github.com/AdrianJames27/django_template).
3. **Removes** the `.git` directory from the cloned repository to eliminate version control history.
4. **Renames** the project directory to the specified project name.

## Requirements

- **Python 3.12**: Ensure Python is installed on your system.

## Error Handling
- The script includes basic error handling for common interruptions:
* KeyboardInterrupt: Handles manual interruption (e.g., pressing Ctrl+C).
* EOFError: Handles unexpected end of input.
* General Exceptions: Catches other unforeseen errors and provides an error message.

## License
- This project is licensed under the MIT License - see the LICENSE file for details.