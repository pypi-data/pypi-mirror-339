import sys
import random
import functools
import traceback

class JediDebug:
    QUOTES = [
        "Do or do not. There is no try. But seriously, try adding some print statements.",
        "The Force is strong with this one. The bug? Not so much.",
        "In my experience, there's no such thing as luck. But there is such a thing as a well-placed debugger.",
        "Your focus determines your reality. Focus on line 42, perhaps?",
        "The ability to destroy a planet is insignificant next to the power of fixing this bug.",
        "These aren't the bugs you're looking for. Look elsewhere in your code.",
        "You will find that many of the bugs we encounter depend greatly on our own point of view.",
        "Judge me by my code size, do you? And well you should not.",
        "Patience you must have, my young developer.",
        "Always pass on what you have learned. Especially about this bug.",
        "I find your lack of comments disturbing.",
        "The greatest teacher, failure is.",
        "Never tell me the odds of fixing this on the first try!",
        "Stay on target... stay on target!",
        "This is the way... to debug your code.",
        "Difficult to see. Always in motion is the future of this code.",
        "Help me debugger, you're my only hope.",
        "I've got a bad feeling about this variable.",
        "Fear is the path to the dark side. Fear leads to anger. Anger leads to hate. Hate leads to spaghetti code.",
        "You must unlearn what you have learned. Try a different approach.",
        "No! Try not. Do. Or do not. There is no try. But really, just keep debugging.",
        "May the Force be with your debugging efforts.",
        "The dark side clouds everything. Impossible to see, this bug is.",
        "Luminous beings are we, not this crude exception.",
        "Remember, a Jedi can feel the Force flowing through clean code."
    ]
    
    @classmethod
    def get_motivational_quote(cls):
        """Return a random Star Wars quote from the collection."""
        return random.choice(cls.QUOTES)
    
    @classmethod
    def exception_handler(cls, exc_type, exc_value, exc_traceback):
        """Custom exception handler that adds motivational Star Wars quotes."""
        # Print the original traceback
        print("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)), file=sys.stderr)
        
        # Add the motivational quote
        print("\n✨ JEDI WISDOM ✨", file=sys.stderr)
        print(f"🌟 {cls.get_motivational_quote()}", file=sys.stderr)
        print("🌟 Trust your instincts, young Padawan. The solution is near.\n", file=sys.stderr)
    
    @classmethod
    def activate(cls):
        """Activate the JediDebug exception handler."""
        sys.excepthook = cls.exception_handler
        print("JediDebug activated! May the Force guide your debugging journey.")
    
    @classmethod
    def jedi_function(cls, func):
        """Decorator to provide Jedi wisdom if a function raises an exception."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"\n✨ JEDI FUNCTION GUIDANCE ✨", file=sys.stderr)
                print(f"🌟 {cls.get_motivational_quote()}", file=sys.stderr)
                print(f"🌟 The function '{func.__name__}' requires your attention, it does.", file=sys.stderr)
                raise
        return wrapper

# Example usage:
if __name__ == "__main__":
    # Activate the Jedi guidance
    JediDebug.activate()
    
    # Test with a deliberately broken function
    def broken_function():
        return 1 / 0
    
    try:
        broken_function()
    except:
        pass
    
    # Test with a decorated function
    @JediDebug.jedi_function
    def another_broken_function():
        x = [1, 2, 3]
        return x[10]  # Index error
    
    try:
        another_broken_function()
    except:
        pass