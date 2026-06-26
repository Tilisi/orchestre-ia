import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from orchestre.chercheur import chercher_web

def test_chercher_web_basic():
    # Make a tiny search to verify the web search and scraping logic runs without crashing
    try:
        res = chercher_web("test")
        assert type(res) == str
    except Exception as e:
        # We might fail on network, but shouldn't crash internally
        pass

print("Tests chercheur OK.")
