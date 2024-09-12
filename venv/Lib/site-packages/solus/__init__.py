"""Singleton types.

## Example

```python
from solus import Singleton

class Null(Singleton):
    ...

null = Null()
```
"""

__description__ = "Singleton types."
__url__ = "https://github.com/nekitdev/solus"

__title__ = "solus"
__author__ = "nekitdev"
__license__ = "MIT"
__version__ = "1.2.2"

from solus.core import (
    Singleton,
    SingletonType,
    UnsafeSingleton,
    UnsafeSingletonType,
    singleton,
    unsafe_singleton,
)

__all__ = (
    # singleton types
    "Singleton",
    "UnsafeSingleton",
    # singleton meta types
    "SingletonType",
    "UnsafeSingletonType",
    # singleton instances
    "singleton",
    "unsafe_singleton",
)
