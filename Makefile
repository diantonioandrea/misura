build:
	make clean
	python3 -m build

test:
	make build
	pip install dist/*.tar.gz
	python3 tests/tests.py

clean:
	rm -rf dist
