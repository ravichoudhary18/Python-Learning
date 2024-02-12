from icecream import ic
import inspect

def ic(*args):
    frame = inspect.currentframe().f_back
    lineno = frame.f_lineno
    print(f"Line {lineno}: {', '.join(map(repr, args))}")
    
__builtins__.ic = ic