# JediDebug

A Python library that motivates programmers with Star Wars quotes when bugs occur. May the Force be with your debugging!

## Installation

```bash
pip install jedidebug
```

## Usage

### Basic Usage

```python
from jedidebug import JediDebug

# Activate the Jedi wisdom globally
JediDebug.activate()

# Now any unhandled exception will trigger a motivational Star Wars quote
def broken_function():
    return 1 / 0

try:
    broken_function()
except:
    pass  # The exception will be printed with Jedi wisdom
```

### Decorating Specific Functions

```python
from jedidebug import JediDebug

# Only provide Jedi guidance for specific functions
@JediDebug.jedi_function
def another_broken_function():
    x = [1, 2, 3]
    return x[10]  # Index error

try:
    another_broken_function()
except:
    pass  # This function will receive Jedi wisdom, but other exceptions won't
```

### Sample Output

```
Traceback (most recent call last):
  File "example.py", line 10, in <module>
    broken_function()
  File "example.py", line 7, in broken_function
    return 1 / 0
ZeroDivisionError: division by zero

✨ JEDI WISDOM ✨
🌟 I find your lack of comments disturbing.
🌟 Trust your instincts, young Padawan. The solution is near.
```

## Customizing Quotes

You can add your own Star Wars quotes to the library:

```python
from jedidebug import JediDebug

# Add your custom Star Wars quotes
JediDebug.QUOTES.extend([
    "The bug is strong with this one.",
    "You were the chosen one! You were supposed to destroy the bugs, not create them!",
])

JediDebug.activate()
```

## Why Use JediDebug?

- To add some fun to your debugging process
- To maintain motivation during frustrating bug hunts
- To bring the wisdom of Star Wars to your development workflow
- Because even Jedi Masters encounter bugs in their code

## Pair with CodeRoast

For a good cop/bad cop debugging experience, try pairing JediDebug with its harsher counterpart, [CodeRoast](https://github.com/yourusername/coderoast)!

## License

MIT License