{
   description = "A devbox shell";

   inputs = {
     nixpkgs.url = "github:NixOS/nixpkgs/eb0e0f21f15c559d2ac7633dc81d079d1caf5f5f?narHash=sha256-ArWLUgRm1tKHiqlhnymyVqi5kLNCK5ghvm06mfCl4QY%3D";
     glibc-patch.url = "path:glibc-patch";
   };

   outputs = {
     self,
     nixpkgs,
     glibc-patch,
   }:
      let
        pkgs = nixpkgs.legacyPackages.x86_64-linux;
      in
      {
        devShells.x86_64-linux.default = pkgs.mkShell {
          buildInputs = [
            (builtins.trace "downloading uv@latest" (builtins.fetchClosure {
              
              fromStore = "https://cache.nixos.org";
              fromPath = "/nix/store/jcg8fnn76jdvf3aygbkh350cs9hgr9jb-uv-0.6.10";
              inputAddressed = true;
            }))
            
            (builtins.trace "downloading python313Packages.hatchling@latest" (builtins.fetchClosure {
              
              fromStore = "https://cache.nixos.org";
              fromPath = "/nix/store/q3pss741d48966i7fdb4a2qjl5y7da9x-python3.13-hatchling-1.27.0";
              inputAddressed = true;
            }))
            (builtins.trace "evaluating glibc-patch.packages.x86_64-linux.python313" glibc-patch.packages.x86_64-linux.python313)
          ];
        };
      };
 }
