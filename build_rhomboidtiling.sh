#!/usr/bin/env bash

if [ ! -d ./bin]; then
  mkdir bin
fi

REPO_DIR=./rhomboidtiling_src
BIN_NAME=rhomboidtiling

if [ ! -d "$REPO_DIR" ]; then
  git clone https://github.com/geoo89/rhomboidtiling.git "$REPO_DIR" 
fi

cd "$REPO_DIR" 
cmake .
make

# Run tests
echo "Running tests..."
./tests_2d
./tests_3d

# Copy binary to workspace
cp ./main "../bin/$BIN_NAME"

cd ..

# Clean up
rm -rf "$REPO_DIR" 

