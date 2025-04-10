{ nixpkgs, pynix, python_pkgs }:
let
  make_bundle = commit: sha256:
    let
      src = builtins.fetchTarball {
        inherit sha256;
        url =
          "https://gitlab.com/dmurciaatfluid/arch_lint/-/archive/${commit}/arch_lint-${commit}.tar";
      };
      bundle = import "${src}/build" { inherit nixpkgs pynix src; };
      extented_python_pkgs = python_pkgs // { inherit (bundle.deps) grimp; };
    in bundle.builders.pkgBuilder
    (bundle.builders.requirements extented_python_pkgs);
in {
  "v4.0.3" = make_bundle "ff6578a129d8b7401844fca2a5ebbe1c1331d757"
    "1qy3czqqjirl801p6ki11krydwr9yq984177xzn2bbk20xcdxvca";
}
