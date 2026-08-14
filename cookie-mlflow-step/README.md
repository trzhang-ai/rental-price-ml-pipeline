# Cookiecutter template for MLflow steps

Use this template to create a consistent MLflow Project component with W&B
artifact initialization and command-line parameters.

## Usage

```bash
cookiecutter PATH_TO_TEMPLATE -o DESTINATION_DIRECTORY
```

The prompt collects the step name, script name, descriptions, job type, and a
comma-separated parameter list without spaces. The rendered directory contains
an MLflow project, Conda environment, and runnable Python entry point.

Generated command-line parameters default to strings. Specialize their types
and descriptions when needed, implement the component-specific artifact
workflow, and add any additional packages to `conda.yml`.
