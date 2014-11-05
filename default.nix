#!/usr/bin/env nix-shell
#! nix-shell --arg "pkgs" "import <nixpkgs> {}"
{ pkgs ? import (builtins.fetchTarball
  "https://github.com/nixos/nixpkgs-channels/archive/nixos-16.09.tar.gz") {}
, pythonPackages ? pkgs.python3Packages
, buildout ? "buildout292"
}:

let self = rec {
  version = builtins.replaceStrings ["\n"] [""] (builtins.readFile ./VERSION);

  buildout171 = pythonPackages.buildPythonPackage rec {
    name = "zc.buildout-1.7.1";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/9c/24/b64b142285eb890ab8501235606facc60eb0593647404864b670de8e149d/zc.buildout-1.7.1.tar.gz";
      sha256 = "a5c2fafa4d073ad3dabec267c44a996cbc624700a9a49467cd6b1ef63d35e029";
    };
  };

  buildout201 = pythonPackages.buildPythonPackage rec {
    name = "zc.buildout-2.0.1";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/b6/03/68b4a7c80fecd9f44c0174aed9146df1d41e6064040a4db0c9d4ffac3014/zc.buildout-2.0.1.tar.gz";
      sha256 = "b9fc1ea9f8da076f1e9a671102a3c701a57ee98686a87565cfaa40a70b317c65";
    };
  };

  buildout225 = pythonPackages.buildPythonPackage rec {
    name = "zc.buildout-2.2.5";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/35/f7/d8ecc2333993bd9c252c492f368218d185beb65dfb155563eec1904bc0fc/zc.buildout-2.2.5.tar.gz";
      sha256 = "fb08f24f9e51e647e29d714f6e9ad51a4ea28673dddeed831315617bb5a805d0";
    };
  };

  buildout231 = pythonPackages.buildPythonPackage rec {
    name = "zc.buildout-2.3.1";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/87/41/591d2acd643c311f351fb7d273011fd6373f3ad1a938f685e87c7d6caf03/zc.buildout-2.3.1.tar.gz";
      sha256 = "3295b8944c637f65db3d6c2ded239b7b41a7f2df0e0bceb8b092247edf1866fb";
    };
  };

  buildout253 = pythonPackages.buildPythonPackage rec {
    name = "zc.buildout-2.5.3";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/e4/7b/63863f09bec5f5d7b9474209a6d4d3fc1e0bca02ecfb4c17f0cdd7b554b6/zc.buildout-2.5.3.tar.gz";
      sha256 = "3e5f3afcc64416604c5efc554c2fa0901b60657e012a710c320e2eb510efcfb9";
    };
  };

  buildout292 = pythonPackages.buildPythonPackage rec {
    name = "zc.buildout-2.9.2";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/d9/a7/e0d48d47c5c71df71cdef6522c6287d304ef64d1c1f241a106b57b6a2b94/zc.buildout-2.9.2.tar.gz";
      sha256 = "513916fef5a99db0a6a03ca210c734746f42b59ff6cc4b87b4947fdb9d6641a8";
    };
  };

  coveralls = pythonPackages.buildPythonPackage {
    name = "coveralls-1.1";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/12/50/5c1034eb92e5bc3d824a3745ca9162f2e4846c6ab5f96dccb5f84f77e98f/coveralls-1.1.tar.gz";
      sha256 = "34160385c13b0c43691ab11c080d4b10dabe3280fc0b2173c731efc5db836808";
    };
    propagatedBuildInputs = [
      pythonPackages.docopt
      pythonPackages.coverage
      pythonPackages.requests2
      pythonPackages.pyyaml
    ];
    doCheck = false;
  };
};

in pythonPackages.buildPythonPackage rec {
  namePrefix = "";
  name = "buildout.sendpickedversions-${self.version}";
  src = builtins.filterSource
    (path: type: baseNameOf path != ".git"
              && baseNameOf path != "result")
    ./.;
  buildInputs = with self; [
    coveralls
    pythonPackages.zope_testing
    pythonPackages.coverage
    pythonPackages.check-manifest
  ];
  propagatedBuildInputs = [
    (builtins.getAttr buildout self)
    pythonPackages.requests2
  ];
  postShellHook = ''
    buildout -Nc qa.cfg
  '';
}
