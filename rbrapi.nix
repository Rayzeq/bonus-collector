{ buildPythonPackage
, fetchFromGitHub
, setuptools
, wheel
, requests
}:
buildPythonPackage {
  pname = "rbrapi";
  version = "0.6";

  src = fetchFromGitHub {
    owner = "Rayzeq";
    repo = "rbr-api";
    rev = "main";
    sha256 = "sha256-2uKYEb0pop5bf2MEl7MFKvvF4Q3Qqx3fTVnN3MZzN24=";
  };

  dependencies = [
    requests
  ];

  doCheck = false;

  pyproject = true;
  build-system = [
    setuptools
    wheel
  ];
}
