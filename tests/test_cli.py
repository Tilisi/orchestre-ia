import os
import subprocess
import sys


def test_cli_help_fonctionne_sans_dotenv_installe():
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    resultat = subprocess.run(
        [sys.executable, "-m", "orchestre", "--help"],
        cwd=os.path.dirname(os.path.dirname(__file__)),
        env=env,
        text=True,
        capture_output=True,
        timeout=10,
    )
    assert resultat.returncode == 0
    assert "Orchestre d'agents IA" in resultat.stdout
    assert "--sujet" in resultat.stdout
