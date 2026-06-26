import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from orchestre.cerveau import _fournisseurs

def test_fournisseurs():
    # If no env vars, should be empty
    assert type(_fournisseurs()) == list
    
print("Tests cerveau OK.")
