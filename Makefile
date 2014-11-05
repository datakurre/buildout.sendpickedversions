SYSTEM ?= x86_64-linux
PYTHON ?= python3
BUILDOUT ?= buildout292

TEST = $(wildcard tests/*.py)
SRC = $(wildcard src/buildout/sendpickedversions/*.py)

all: test

buildEnv: result/bin/$(PYTHON)

coverage: .coverage
	nix-shell --run "coverage report --fail-under=80"

coveralls: .coverage
	nix-shell --run coveralls

dist:
	nix-build release.nix -A tarball

shell:
	nix-shell --arg "pkgs" "import <nixpkgs> {}" \
	          --arg "pythonPackages" "(import <nixpkgs> {}).$(PYTHON)Packages" \
	          --arg "buildout" '"$(BUILDOUT)"'

test:
	nix-build release.nix -A build.$(SYSTEM).$(PYTHON) \
	          --arg "buildout" '"$(BUILDOUT)"'
	nix-shell --run "bin/code-analysis"

.PHONY: all buildEnv coverage coveralls dist shell test

###

.coverage: $(TEST) $(SRC)
	nix-shell --run "coverage run setup.py test"

result/bin/$(PYTHON):
	nix-build release.nix -A buildEnv.$(SYSTEM).$(PYTHON)

result/sphinxcontrib-httpexample.pdf:
	nix-build release.nix -A docs
