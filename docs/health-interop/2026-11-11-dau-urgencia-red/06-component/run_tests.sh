#!/bin/sh
# Corre la suite de tests del componente DAU (solo stdlib, sin pytest).
cd "$(dirname "$0")" || exit 1
PYTHONPATH=src python3 -m unittest discover -s tests -v
