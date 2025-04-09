import os, sys

LIB_PATH = os.path.dirname(os.path.abspath(__file__))
sys.append(LIB_PATH)

from encode import *
from decode import *
from k2p import *
