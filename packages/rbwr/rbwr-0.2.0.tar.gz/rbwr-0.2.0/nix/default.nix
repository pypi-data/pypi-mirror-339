{ sprinkles ? null }:

let
  source =
    (import (
      let
        lock = builtins.fromJSON (builtins.readFile ./flake.lock);
        inherit (lock.nodes.flake-compat.locked) narHash rev url;
      in
      builtins.fetchTarball {
        url = "${url}/archive/${rev}.tar.gz";
        sha256 = narHash;
      }
    ) { src = ./.; }).inputs;

  # Keep sorted.
  input = source: {
    nixpkgs = import source.nixpkgs {
      config.allowAliases = false;
    };
    sprinkles = if sprinkles == null
      then import source.sprinkles
      else sprinkles;
  };
in

(input source).sprinkles.new {
  inherit input source;

  output = self:
    let
      inherit (self.input) nixpkgs;
      inherit (self.input.nixpkgs.lib.customisation) makeScope;
    in
    {
      shell = makeScope nixpkgs.newScope (scope: {
        default = scope.callPackage ./shell/default {};
      });
    };
}
