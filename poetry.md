Setting up a project using Poetry, a dependency management tool for Python, is straightforward. Here’s a step-by-step guide to get you started:

### 1. Install Poetry

First, you need to install Poetry. You can do this using the following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Alternatively, you can use pip:

```bash
pip install poetry
```

### 2. Create a New Project

Once Poetry is installed, you can create a new project. Navigate to the directory where you want your project to be and run:

```bash
poetry new my_project
```

Replace `my_project` with your desired project name. This will create a new directory with the same name and set up the basic project structure.

### 3. Navigate to Your Project Directory

Move into your project directory:

```bash
cd my_project
```

### 4. Add Dependencies

To add dependencies to your project, use the `add` command:

```bash
poetry add requests
```

You can replace `requests` with any other package you need. For development dependencies, use the `--dev` flag:

```bash
poetry add --dev pytest
```

### 5. Activate the Virtual Environment

Poetry automatically creates a virtual environment for your project. To activate it, run:

```bash
poetry shell
```

### 6. Install Dependencies

If you have an existing `pyproject.toml` file with dependencies listed, you can install them all at once:

```bash
poetry install
```

### 7. Run Your Project

With your virtual environment active, you can run your project scripts. If you have a script entry point defined in `pyproject.toml`, you can use:

```bash
poetry run python your_script.py
```

### 8. Managing Your Project

- **Update Dependencies**: To update all dependencies to the latest versions:

  ```bash
  poetry update
  ```

- **Remove Dependencies**: To remove a dependency:

  ```bash
  poetry remove requests
  ```

- **List Dependencies**: To see all installed dependencies:

  ```bash
  poetry show
  ```

### Example `pyproject.toml`

Here's a basic example of what your `pyproject.toml` might look like:

```toml
[tool.poetry]
name = "my_project"
version = "0.1.0"
description = ""
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.25.1"

[tool.poetry.dev-dependencies]
pytest = "^6.2.2"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

### Conclusion

Poetry simplifies dependency management and project setup for Python projects. By following these steps, you can easily set up and manage your project using Poetry.