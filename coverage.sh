#!/bin/bash
coverage run --source=. --omit=tests/*.py,web/*.*,assets/*.* -m unittest discover -s tests/
coverage report -m
