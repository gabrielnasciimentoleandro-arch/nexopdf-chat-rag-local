.PHONY: install run test lint samples check

install:
	python -m pip install -r requirements.txt

run:
	streamlit run app.py

test:
	pytest

lint:
	ruff check src tests app.py scripts

samples:
	python scripts/generate_sample_pdfs.py

check: lint test
