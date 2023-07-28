#!/bin/bash

# Loop through uppercase letters (ASCII 65 to 90)
for ((i=65; i<=90; i++)); do
    letter=$(printf \\$(printf '%03o' "$i"))
    mkdir "$letter"
done

# Loop through lowercase letters (ASCII 97 to 122)
for ((i=97; i<=122; i++)); do
    letter=$(printf \\$(printf '%03o' "$i"))
    mkdir "$letter"
done

# Loop through numbers 0-9 (ASCII 48 to 57)
for ((i=48; i<=57; i++)); do
    num=$(printf \\$(printf '%03o' "$i"))
    mkdir "$num"
done

mkdir "!"
mkdir "&"
mkdir "'"
mkdir "("
mkdir ")"
mkdir "*"
mkdir ","
mkdir "-"
mkdir "_."
mkdir "_/"
mkdir ":"
mkdir ";"
mkdir "?"
mkdir "^"
mkdir "~"
mkdir "\""
