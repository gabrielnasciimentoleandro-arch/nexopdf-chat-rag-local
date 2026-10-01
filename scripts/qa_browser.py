"""Smoke test opcional da interface real com Playwright.

Requer o app ativo em http://127.0.0.1:8501 e as dependências de documentação.
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto("http://127.0.0.1:8501", wait_until="networkidle", timeout=120_000)
    page.get_by_text("Converse com seus").wait_for(timeout=120_000)
    assert page.locator('[data-testid="stException"]').count() == 0

    page.get_by_role("button", name="Quais cuidados devo tomar ao usar IA no TCC?").click()
    page.get_by_text("Esta resposta está em modo extrativo").wait_for(timeout=120_000)
    assert page.get_by_text("Ver 5 trechos consultados").count() == 1
    assert page.locator('[data-testid="stException"]').count() == 0

    upload = page.locator('input[type="file"]')
    upload.set_input_files(str(ROOT / "inputs" / "uso_responsavel_ia_tcc.pdf"))
    page.wait_for_timeout(1_000)
    page.get_by_role("button", name="Indexar meus arquivos").click()
    page.get_by_text("Base atualizada.").wait_for(timeout=120_000)
    page.get_by_text("Base ativa · Meus documentos").wait_for(timeout=30_000)
    assert page.locator('[data-testid="stException"]').count() == 0
    assert not errors, errors
    browser.close()

print("QA do navegador: demonstração, chat e upload aprovados.")
