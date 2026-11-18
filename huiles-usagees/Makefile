.PHONY: all test

all:
	python3 run_all.py

test:
	python3 -m pytest -q tests
	cd 16_application && python3 -m pytest -q tests -p no:logging
