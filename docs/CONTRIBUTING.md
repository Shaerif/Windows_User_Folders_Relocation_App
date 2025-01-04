
# Contributing to Windows User Folders Relocation App

Thank you for your interest in contributing to the Windows User Folders Relocation App! We welcome all contributions that help improve the project. Whether it's fixing bugs, enhancing features, or improving documentation, your efforts are appreciated.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
  - [Reporting Issues](#reporting-issues)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Development Setup](#development-setup)
- [Running Tests](#running-tests)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)
- [License](#license)

## Code of Conduct

By contributing, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it to understand the standards we expect from all contributors.

## How to Contribute

### Reporting Issues

If you encounter bugs or have suggestions for improvements, please [open an issue](https://github.com/yourusername/windows-user-folders-relocation-tool/issues) on GitHub. When reporting an issue, please include:

- A clear and descriptive title.
- A detailed description of the problem or suggestion.
- Steps to reproduce the issue (if applicable).
- Any relevant screenshots or logs.

### Submitting Pull Requests

Pull requests are how you propose changes to the project. Here's how to submit one:

1. **Fork the Repository**

   Click the "Fork" button at the top right of the repository page to create your own fork.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/yourusername/windows-user-folders-relocation-tool.git
   ```

3. **Create a New Branch**

   It's best to create a new branch for each feature or bugfix.

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**

   Implement your feature or bugfix. Ensure your code follows the project's coding standards.

5. **Run Tests**

   Ensure all existing tests pass and add new tests for your changes if necessary.

6. **Commit Your Changes**

   Write clear and concise commit messages.

   ```bash
   git commit -m "Add feature X to improve Y"
   ```

7. **Push to Your Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

8. **Open a Pull Request**

   Navigate to your fork on GitHub and click the "Compare & pull request" button. Provide a detailed description of your changes and reference any related issues.

## Development Setup

To set up the development environment, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/windows-user-folders-relocation-tool.git
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

Write clear and descriptive commit messages. A good commit message should include:

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

Thank you for your contributions! 🙌