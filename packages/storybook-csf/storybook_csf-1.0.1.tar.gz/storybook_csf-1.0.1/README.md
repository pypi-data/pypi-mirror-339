# storybook-csf

[![PyPI - Version](https://img.shields.io/pypi/v/storybook-csf)](https://pypi.org/project/storybook-csf/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/storybook-csf)](https://pypi.org/project/storybook-csf/) [![PyPI - License](https://img.shields.io/pypi/l/storybook-csf)](https://github.com/jurooravec/storybook-csf/blob/main/LICENSE) [![PyPI - Downloads](https://img.shields.io/pypi/dm/storybook-csf)](https://pypistats.org/packages/storybook-csf) [![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/jurooravec/storybook-csf/tests.yml)](https://github.com/jurooravec/storybook-csf/actions/workflows/tests.yml)

Write Storybook stories in Python - Typings for Storybook's [Component Story Format (CSF) v3](https://storybook.js.org/docs/api/csf).

The types defined in this package allow you to write Storybook's CSF format in your Python projects.
[See included types here](https://github.com/jurooravec/storybook-csf/blob/main/src/storybook_csf/story.py).

> NOTE: The types defined in this package are a JSON-compatible subset of CSF. Fields that require
> JS-specific types are not included.

```python
from storybook_csf import ComponentAnnotations, ProjectAnnotations, StoryAnnotations

# This will be typed
data: ComponentAnnotations = {
    "title": "Component",
    "parameters": {
        "options": { "component": "my_widget" }
    },
    # `stories` field is specific to Storybook for Server
    # See https://github.com/storybookjs/storybook/tree/next/code/frameworks/server-webpack5
    "stories": [
        {
            "name": "Default",
            "parameters": {
                "server": { "id": "path/of/your/story" }
            }
        }
    ]
}
```

## Installation

```bash
pip install storybook-csf
```

## Release notes

Read the [Release Notes](https://github.com/jurooravec/storybook-csf/tree/main/CHANGELOG.md)
to see the latest features and fixes.

## Development

### Tests

To run tests, use:

```bash
pytest
```
