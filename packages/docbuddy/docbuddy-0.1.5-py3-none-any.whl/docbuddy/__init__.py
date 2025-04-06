import warnings
import importlib.util

__version__ = "0.1.5"

warnings.simplefilter('always', DeprecationWarning)
warnings.warn(
    "'docbuddy' is deprecated and will be removed in a future version. "
    "Please use 'ask-docs' instead.",
    DeprecationWarning,
    stacklevel=2
)

# Check if ask-docs is installed and import it
if importlib.util.find_spec("ask_docs") is not None:
    import ask_docs
else:
    warnings.warn(
        "The package 'ask-docs' should be installed as a dependency. "
        "If not, please install it manually with 'pip install ask-docs'.",
        RuntimeWarning
    )