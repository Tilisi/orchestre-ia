import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from orchestre.routeur import _classification_rapide, router

def test_classification_rapide():
    assert _classification_rapide("écris un script python") == "code"
    assert _classification_rapide("analyse ces données csv") == "data"
    assert _classification_rapide("rédige un email pour mon patron") == "contenu"
    assert _classification_rapide("quelque chose de vague") is None

def test_routeur_fallback():
    # If no keywords match and no API is provided, the mock should handle it 
    # but we just want to ensure it doesn't crash on keywords
    assert router("script python") == "code"

print("Tests routeur OK.")
