import sys
import random
import functools
import traceback

class CodeRoast:
    INSULTS = [
        "Seriously? That's the code you wrote? My calculator has better logic.",
        "ERROR: Brain not found. Have you tried turning it on and off again?",
        "Your code is like a mystery novel, except the only mystery is how it ever worked.",
        "I've seen better code written by a cat walking on a keyboard.",
        "If your code was any more broken, it would qualify for workers' compensation.",
        "Ah, I see the problem. You're trying to program while being stupid.",
        "Did you get your programming license from a cereal box?",
        "Your algorithm is so inefficient, it makes government bureaucracy look fast.",
        "Your code has more bugs than a tropical rainforest.",
        "ERROR: Intelligence module failed to load. User incompetence detected.",
        "This code is why Stack Overflow exists.",
        "Maybe programming isn't for everyone. Have you considered gardening?",
        "I'm not saying your code is bad, but it made Skynet reconsider its attack on humanity.",
        "Your variable naming convention appears to be 'keyboard smash'.",
        "This function is more convoluted than the plot of a telenovela.",
    ]
    
    @classmethod
    def get_insult(cls):
        """Return a random insult from the collection."""
        return random.choice(cls.INSULTS)
    
    @classmethod
    def exception_handler(cls, exc_type, exc_value, exc_traceback):
        """Custom exception handler that adds insults."""
        # Print the original traceback
        print("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)), file=sys.stderr)
        
        # Add the insult
        print("\n🔥 ROASTED 🔥", file=sys.stderr)
        print(f"👉 {cls.get_insult()}", file=sys.stderr)
        print("👉 Maybe try again when you know what you're doing.\n", file=sys.stderr)
    
    @classmethod
    def activate(cls):
        """Activate the CodeRoast exception handler."""
        sys.excepthook = cls.exception_handler
        print("CodeRoast activated! Prepare to be roasted for your mistakes.")
    
    @classmethod
    def roast_function(cls, func):
        """Decorator to roast a specific function if it raises an exception."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"\n🔥 FUNCTION ROASTED 🔥", file=sys.stderr)
                print(f"👉 {cls.get_insult()}", file=sys.stderr)
                print(f"👉 Function '{func.__name__}' failed spectacularly.", file=sys.stderr)
                raise
        return wrapper

# Activate CodeRoast by default when the module is imported
# (Comment this out if you want it to be explicitly activated)
# CodeRoast.activate()

# Example usage:
if __name__ == "__main__":
    # Activate the roaster
    CodeRoast.activate()
    
    # Test with a deliberately broken function
    def broken_function():
        return 1 / 0
    
    try:
        broken_function()
    except:
        pass
    
    # Test with a decorated function
    @CodeRoast.roast_function
    def another_broken_function():
        x = [1, 2, 3]
        return x[10]  # Index error
    
    try:
        another_broken_function()
    except:
        pass