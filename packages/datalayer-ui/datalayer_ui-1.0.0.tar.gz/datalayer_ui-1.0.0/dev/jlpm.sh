#!/usr/bin/env bash

# Copyright (c) 2021-2024 Datalayer, Inc.
#
# Datalayer License

echo
echo -e "\x1b[34m\x1b[JLPM $1\x1b[0m"
echo

echo "BEGIN ------------------------------ JLPM $1"

npm run $1

echo "END ------------------------------ JLPM $1"
