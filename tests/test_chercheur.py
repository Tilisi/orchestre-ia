import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from orchestre.chercheur import _extraire_liens_duckduckgo, _nettoyer_html, chercher_web


class FakeResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


def test_extraire_liens_duckduckgo_result_a_et_uddg():
    html = '''
    <html><body>
      <a class="result__a" href="/l/?uddg=https%3A%2F%2Fexample.com%2Farticle">Article</a>
      <a class="result__a" href="https://duckduckgo.com/about">Duck</a>
      <a class="result__url" href="https://example.org/page">Page</a>
    </body></html>
    '''
    assert _extraire_liens_duckduckgo(html) == [
        "https://example.com/article",
        "https://example.org/page",
    ]


def test_nettoyer_html_supprime_script_nav_footer():
    html = """
    <html><body><nav>Menu</nav><h1>Titre</h1><script>alert(1)</script><p>Contenu utile</p><footer>Bas</footer></body></html>
    """
    texte = _nettoyer_html(html)
    assert "Titre" in texte
    assert "Contenu utile" in texte
    assert "alert" not in texte
    assert "Menu" not in texte
    assert "Bas" not in texte


def test_chercher_web_scrape_pages(monkeypatch):
    search_html = '''
    <a class="result__a" href="/l/?uddg=https%3A%2F%2Fexample.com%2Fa">A</a>
    <a class="result__a" href="https://example.com/b">B</a>
    '''

    def fake_post(*args, **kwargs):
        return FakeResponse(search_html)

    def fake_get(url, *args, **kwargs):
        return FakeResponse(f"<html><body><h1>{url}</h1><p>Texte source</p></body></html>")

    monkeypatch.setattr("orchestre.chercheur.requests.post", fake_post)
    monkeypatch.setattr("orchestre.chercheur.requests.get", fake_get)

    resultat = chercher_web("test")
    assert "--- SOURCE : https://example.com/a ---" in resultat
    assert "--- SOURCE : https://example.com/b ---" in resultat
    assert "Texte source" in resultat
