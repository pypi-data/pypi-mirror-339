# CodeRoast

A Python library that insults programmers when their code throws errors. Because sometimes you need a reality check.

## Installation

```bash
pip install coderoast
```

## Usage

### Basic Usage

```python
from coderoast import CodeRoast

# Activate the roasting globally
CodeRoast.activate()

# Now any unhandled exception will trigger an insult
def broken_function():
    return 1 / 0

try:
    broken_function()
except:
    pass  # The exception will be printed with an insult
```

### Decorating Specific Functions

```python
from coderoast import CodeRoast

# Only roast specific functions
@CodeRoast.roast_function
def another_broken_function():
    x = [1, 2, 3]
    return x[10]  # Index error

try:
    another_broken_function()
except:
    pass  # This function will be roasted, but other exceptions won't be
```

### Sample Output

```
Traceback (most recent call last):
  File "example.py", line 10, in <module>
    broken_function()
  File "example.py", line 7, in broken_function
    return 1 / 0
ZeroDivisionError: division by zero

🔥 ROASTED 🔥
👉 Your code has more bugs than a tropical rainforest.
👉 Maybe try again when you know what you're doing.
```

## Customizing Insults

You can add your own insults to the library:

```python
from coderoast import CodeRoast

# Add your custom insults
CodeRoast.INSULTS.extend([
    "This code is so bad it made my CPU cry.",
    "Have you considered a career in interpretive dance instead?",
])

CodeRoast.activate()
```

## Why Use CodeRoast?

- To add humor to your debugging process
- To humble yourself or your teammates
- For educational purposes (teaching new programmers to handle exceptions)
- Because normal error messages are too polite

## License

MIT License