"""
Streamlit Cloud entrypoint (`streamlit_app.py`) for the Pathology Smart Gateway
Landing Page & Interactive Product Showcase (Ki-67 & HER2).

Repository: https://github.com/Vishovan/Pathomorfology_lending_page
Main WSI Product: https://pathomorphology.streamlit.app
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import re

try:
    import streamlit as st
    import streamlit.components.v1 as components
except ImportError:  # pragma: no cover - allows unit testing without streamlit installed
    st = None  # type: ignore[assignment]
    components = None  # type: ignore[assignment]

REPO_ROOT = Path(__file__).resolve().parent
ASSETS_DIR = REPO_ROOT / "assets"
MAIN_PRODUCT_URL = "https://pathomorphology.streamlit.app"
_COMMENT_RE = re.compile(r"<!--(?!\s*\[if)[\s\S]*?-->")


@lru_cache(maxsize=4)
def build_landing_html(initial_product: str = "ki67", initial_view: str = "landing") -> str:
    """Assemble compact, pre-warmed landing page HTML for instant Streamlit startup."""
    landing_path = ASSETS_DIR / "landing.html"
    plates_path = ASSETS_DIR / "plates.css"

    html = landing_path.read_text(encoding="utf-8")
    plates_css = plates_path.read_text(encoding="utf-8") if plates_path.exists() else ""

    # Inline lightweight compressed plates & strip HTML comments cleanly outside <script>
    html = html.replace('<link rel="stylesheet" href="plates.css" />', "")
    html = html.replace("/* __PLATES_CSS__ */", plates_css)
    head_body, sep, tail_script = html.partition("<script>")
    head_body = _COMMENT_RE.sub("", head_body)
    html = head_body + sep + tail_script

    valid_products = {"ki67", "her2"}
    valid_views = {"landing", "deck"}
    prod = initial_product if initial_product in valid_products else "ki67"
    view = initial_view if initial_view in valid_views else "landing"

    if prod != "ki67" or view != "landing":
        boot_script = (
            f"<script>"
            f"window.addEventListener('DOMContentLoaded', function() {{"
            f"  if (window.setGatewayProduct) window.setGatewayProduct('{prod}');"
            f"  document.body.setAttribute('data-view', '{view}');"
            f"}});"
            f"</script></body>"
        )
        html = html.replace("</body>", boot_script)

    return html


# Pre-warm default HTML at server startup so visitors render with zero cold build lag
_PREWARMED_HTML = build_landing_html("ki67", "landing")


def main() -> None:
    if st is None or components is None:
        raise RuntimeError("Streamlit is required to run streamlit_app.py (`pip install -r requirements.txt`).")

    st.set_page_config(
        page_title="Pathology Smart Gateway — Цифровая патоморфология (Ki-67 & HER2)",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Full-bleed responsive desktop + mobile (100dvh + iOS/Android touch scroll) viewport
    st.markdown(
        """
        <style>
            html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, section.main {
                margin: 0 !important;
                padding: 0 !important;
                width: 100% !important;
                max-width: 100vw !important;
                min-height: 100vh !important;
                min-height: 100dvh !important;
                overflow-x: hidden !important;
                overflow-y: auto !important;
                -webkit-overflow-scrolling: touch !important;
                background: #000000 !important;
            }
            header[data-testid="stHeader"],
            footer,
            #MainMenu,
            [data-testid="stToolbar"],
            [data-testid="stDecoration"],
            [data-testid="stStatusWidget"] {
                display: none !important;
                height: 0 !important;
            }
            .block-container,
            [data-testid="stMainBlockContainer"],
            [data-testid="stVerticalBlock"],
            .element-container,
            [data-testid="element-container"],
            [data-testid="stCustomComponentV1"],
            [data-testid="stHtml"] {
                padding: 0 !important;
                margin: 0 !important;
                max-width: 100vw !important;
                width: 100% !important;
                gap: 0 !important;
            }
            iframe {
                display: block !important;
                border: none !important;
                width: 100% !important;
                max-width: 100vw !important;
                height: 100vh !important;
                height: 100dvh !important;
                -webkit-overflow-scrolling: touch !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    params = st.query_params
    initial_product = str(params.get("product", "ki67")).lower()
    initial_view = str(params.get("view", "landing")).lower()

    full_html = build_landing_html(initial_product=initial_product, initial_view=initial_view)
    components.html(full_html, height=1080, scrolling=True)


if __name__ == "__main__":
    main()
