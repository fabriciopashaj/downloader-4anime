import os, sys
sys.path.append(os.path.expandvars(os.path.dirname(__file__) + '/..'))
from src.util import unimplemented

@unimplemented
def foo():
	pass

foo()
