build:
	make clean
	python3 -m build

test:
	python3 src/test.py

clean:
	rm -rf dist
