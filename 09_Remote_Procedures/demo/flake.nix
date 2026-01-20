{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs = inputs@{ self, nixpkgs, flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];

      perSystem = { pkgs, ... }: {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            go
            jdk25
            gradle_9
            (python3.withPackages (ps: with ps; [
              grpcio
              grpcio-tools
              protobuf
            ]))
            protobuf_25
            protoc-gen-go
            protoc-gen-go-grpc
            protoc-gen-grpc-java
          ];
        };
      };
    };
}
