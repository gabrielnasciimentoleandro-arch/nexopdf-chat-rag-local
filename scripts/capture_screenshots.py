"""Captura telas reais da aplicação para o README.

Requer o app em http://127.0.0.1:8501 e Playwright com Chromium.
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "screenshots"

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
    page.goto("http://127.0.0.1:8501", wait_until="networkidle", timeout=120_000)
    page.get_by_text("Converse com seus").wait_for(timeout=120_000)
    page.wait_for_timeout(2_000)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=OUTPUT / "01-home.png", full_page=True)

    page.get_by_role("button", name="Quais cuidados devo tomar ao usar IA no TCC?").click()
    page.get_by_text("Esta resposta está em modo extrativo").wait_for(timeout=120_000)
    page.get_by_text("Ver 5 trechos consultados").click()
    page.wait_for_timeout(1_000)
    page.screenshot(path=OUTPUT / "02-resposta-com-fontes.png", full_page=True)
    browser.close()

print("Screenshots capturados em assets/screenshots/.")
