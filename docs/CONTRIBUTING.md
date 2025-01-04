# Contributing to Windows User Folders Relocation App

First off, thank you for considering contributing to our project! 🎉

## Table of Contents

- [Contributing to Windows User Folders Relocation App](#contributing-to-windows-user-folders-relocation-app)
  - [Table of Contents](#table-of-contents)
  - [Code of Conduct](#code-of-conduct)
  - [How Can I Contribute?](#how-can-i-contribute)
    - [Reporting Bugs](#reporting-bugs)
    - [Suggesting Enhancements](#suggesting-enhancements)
    - [Pull Requests](#pull-requests)
  - [Development Setup](#development-setup)
  - [Running Tests](#running-tests)
  - [Style Guidelines](#style-guidelines)
  - [Commit Messages](#commit-messages)
  - [License](#license)

## Code of Conduct

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming and respectful environment for all contributors.

## How Can I Contribute?

### Reporting Bugs

If you find a bug in the application, please open an issue in the [GitHub Issues](https://github.com/shaerif/windows-user-folders-relocation-tool/issues) section with detailed information about the problem and steps to reproduce it.

### Suggesting Enhancements

Have an idea to improve the project? Open an issue to discuss your proposal. We're open to new ideas and features that can benefit the project.

### Pull Requests

We welcome contributions in the form of pull requests. Here's how you can get started:

1. **Fork the Repository**

   Click the "Fork" button at the top right of the repository page to create your own fork.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/shaerif/windows-user-folders-relocation-tool.git
   ```

3. **Create a New Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**

   Implement your feature or bug fix. Ensure your code follows the project's style guidelines.

5. **Run Tests**

   Ensure all tests pass before submitting your changes.

6. **Commit Your Changes**

   Write clear and descriptive commit messages.

7. **Push to Your Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

8. **Open a Pull Request**

   Navigate to your fork on GitHub and click the "Compare & pull request" button.

## Development Setup

To set up the development environment, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/shaerif/windows-user-folders-relocation-tool.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd windows-user-folders-relocation-tool
   ```

3. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

4. **Activate the Virtual Environment**

   - **Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **Unix or MacOS:**

     ```bash
     source venv/bin/activate
     ```

5. **Install Dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Running Tests

The project includes both unit and integration tests. To run the tests, use the following commands:

- **Unit Tests:**

  ```bash
  python -m unittest discover -s tests -p 'test_folder_relocator.py'
  ```

- **Integration Tests:**

  ```bash
  python -m unittest discover -s tests -p 'test_integration_folder_relocator.py'
  ```

Ensure all tests pass before submitting a pull request.

## Style Guidelines

Please adhere to the following style guidelines to maintain code consistency:

- **PEP 8 Compliance:** Follow Python's PEP 8 style guide.
- **Typing:** Use type hints where appropriate.
- **Documentation:** Provide clear docstrings for modules, classes, and functions.
- **Naming Conventions:** Use descriptive names for variables, functions, and classes.

## Commit Messages

Write clear and concise commit messages. A good commit message should include:

- **Title:** A brief summary of the changes.
- **Body (optional):** A detailed description of the changes and the reasoning behind them.

Example:

```
Add integration tests for UserFolderRelocator

- Implemented tests to cover successful relocation
- Added tests for failure scenarios such as invalid paths and backup failures
```

## License

By contributing, you agree that your contributions will be licensed under the [Non-Commercial Educational and Non-Profit License](LICENSE).

Thank you for your contribution! 🙌