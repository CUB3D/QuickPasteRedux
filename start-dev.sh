#!/bin/sh

STARTLETTE_CONFIG=.env hypercorn app/main.py:app -c Hypercorn-DEV.toml --access-log - --error-log -
