# docbuddy (DEPRECATED)

**IMPORTANT: This package is deprecated. Please use [ask-docs](https://pypi.org/project/ask-docs/) instead.**

This package now serves as a compatibility layer that will automatically install `ask-docs` when installed.

## Migration

To migrate from docbuddy to ask-docs, simply update your imports and dependencies:

```python
# Old way
import docbuddy

# New way
import ask_docs
```

And update your requirements:

```
# Old requirement
docbuddy>=0.1.3

# New requirement
ask-docs>=0.1.0
```