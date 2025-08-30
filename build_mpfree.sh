#!/usr/bin/env bash

if [ ! -d ./bin ]; then
  mkdir bin
fi

REPO_DIR=./mpfree_src
BIN_NAME=mpfree

if [ ! -d "$REPO_DIR" ]; then
  git clone https://bitbucket.org/mkerber/mpfree.git "$REPO_DIR"
fi

cd "$REPO_DIR"

cmake .
make

# Copy binary to workspace
cp ./mpfree_sequential "../bin/$BIN_NAME"

cd ..

# Clean up
rm -rf "$REPO_DIR"

