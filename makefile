dev:
	cd frontend && yarn build
	cd ..
	python -m uvicorn main:app --reload --host 0.0.0.0 --port 3000

test:
	pip install --upgrade pytest
	python -m pytest