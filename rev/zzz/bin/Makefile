CC := gcc
CFLAGS := -O3 -s -Wno-unused-result

zzz: zzz.c

zzz.c: constraints.json gen.py zzz.c.j2
	python3 gen.py

constraints.json: constraints.py
	python3 constraints.py
