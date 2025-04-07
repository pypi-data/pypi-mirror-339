# TUM Common X

A Django package providing common functionality for TUM projects.

## Installation

```bash
pip install tum-common-x
```

## Usage

Add `tum_common_x` to your `INSTALLED_APPS` in your Django settings:

```python
INSTALLED_APPS = [
    ...
    'tum_common_x',
    ...
]
```

Include the URLs in your project's `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path('', include('tum_common_x.urls')),
    ...
]
```

## Features

- Predefined Django apps and URLs
- Common functionality for TUM projects
- Easy integration with existing Django projects

## Development

To set up the development environment:

1. Clone the repository
2. Create a virtual environment
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 