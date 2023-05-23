# API key for testing purposes.
KEY ?= 

test:
	python3 src/test.py	$(KEY)