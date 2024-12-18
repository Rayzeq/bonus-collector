{ pkgs ? import <nixos> { } }:
let
  python = pkgs.python3.override {
    self = python;
    packageOverrides = pyfinal: pyprev: {
      rbrapi = pyfinal.callPackage ./rbrapi.nix { };
    };
  };
in
pkgs.mkShell {
  packages = [
    (python.withPackages (python-pkgs: with python-pkgs; [
      rbrapi
    ]))
  ];
  shellHook = ''
  '';
}
