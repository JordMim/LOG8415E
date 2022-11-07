#!/bin/bash
cat $1 | tr '[:space:]' '\n' | sort | uniq -c