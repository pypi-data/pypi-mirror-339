# ReflexMonaco

A package wrapping [Monaco Editor](https://www.npmjs.com/package/@monaco-editor/react) for Reflex.

## Installation

```bash
pip install reflex-monaco
```

# Monaco Editor Component

## Overview
The Monaco Editor component is a versatile and powerful code editor that can be embedded in your application. This README provides an overview of its properties and triggers, allowing you to configure and interact with the editor effectively.

## Properties

### `default_language`
- **Description**: The default language to use for the editor.
- **Type**: `str`

### `default_path`
- **Description**: The path to the default file to load in the editor.
- **Type**: `str`

### `default_value`
- **Description**: The default value to display in the editor.
- **Type**: `str`

### `language`
- **Description**: The language to use for the editor.
- **Type**: `str`

### `line`
- **Description**: The line to jump to in the editor.
- **Type**: `int`

### `theme`
- **Description**: The theme to use for the editor.
- **Type**: `str`

### `value`
- **Description**: The value to display in the editor.
- **Type**: `str`

### `width`
- **Description**: The width of the editor.
- **Type**: `str`

### `height`
- **Description**: The height of the editor.
- **Type**: `str`

## Triggers

### `on_change`
- **Description**: Triggered when the editor value changes.
- **Signature**: `lambda e: [e]`

### `on_validate`
- **Description**: Triggered when the content is validated. (limited to some languages)
- **Signature**: `lambda e: [e]`

## Usage Example
Here is a basic example of how to use the Monaco Editor component:

```python
import reflex as rx
from reflex_monaco import monaco

@rx.page()
def index():
    return monaco(
        default_language='javascript',
        default_value='console.log("Hello, world!");',
        height='500px',
        width='100%'
    )
```

See the code of the demo for a case using State.