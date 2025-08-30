{ pkgs ? import <nixpkgs> { } }:

let
  # Old packages for C++ stack
  oldPkgs = import (fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/eec050f3955d803dbee1ea66706f0bca7aa7ff88.tar.gz";
  }) { };

  # Latest Python version with required packages
  pythonEnv = pkgs.python3.withPackages(ps: with ps; [
    numpy
    matplotlib
    tadasets
    pip
  ]);

in
oldPkgs.mkShell {
  buildInputs = [
    # For building rhomboidtiling
    oldPkgs.cgal
    oldPkgs.gcc
    oldPkgs.boost
    oldPkgs.gmp
    oldPkgs.mpfr
    #oldPkgs.boost
    #oldPkgs.qt5.full
    oldPkgs.git
    oldPkgs.vim
    pythonEnv
    pkgs.cmake
    pkgs.ncurses
    pkgs.uv
  ];
  shellHook = ''
    export PATH=$PATH:$PWD/bin
  '';
}

