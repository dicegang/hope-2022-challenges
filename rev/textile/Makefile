PYTHON ?= python3

mangled.tex map.json &: src.tex mangle.py names.json
	$(PYTHON) mangle.py --names names.json --mangle-map-out map.json src.tex mangled.tex
