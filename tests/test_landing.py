import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("landing_streamlit_app", REPO_ROOT / "streamlit_app.py")
assert SPEC is not None and SPEC.loader is not None
landing_app = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(landing_app)


def test_build_landing_html_default():
    html = landing_app.build_landing_html()
    assert "Pathology Smart Gateway" in html
    assert "https://pathomorphology.streamlit.app" in html
    assert 'data-set-product="ki67"' in html
    assert 'data-set-product="her2"' in html
    assert 'data-set-product="panel"' in html
    assert "--img-dna:" in html
    assert "--img-tissue:" in html
    assert "--img-hero-cells:" in html
    assert "--img-chart-glow:" in html
    assert "/* __PLATES_CSS__ */" not in html


def test_build_landing_html_her2_and_deck():
    html_her2 = landing_app.build_landing_html(initial_product="her2", initial_view="deck")
    assert "window.setGatewayProduct('her2')" in html_her2
    assert "document.body.setAttribute('data-view', 'deck')" in html_her2
