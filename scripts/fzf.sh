#!/usr/bin/env bash

read -r input

cat $1 | fzf -i -f "$input"
