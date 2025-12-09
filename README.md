# Parallel, Concurrent, and Distributed Programming

This repository hosts material for the lecture on parallel, concurrent, and
distributed programming in 2025.

This in the repo of Niklas, and therfore holds my solutions for the tasks.


## SetUp

To keep your fork of this repository up to date with the original (upstream), you need to configure a new remote and regularly fetch and merge changes. Here’s a step-by-step guide:

```bash
# 1. Add the upstream repository if you haven't already
git remote add upstream https://github.com/se-tuebingen-exercises/pcd-ws25.git

# 2. Verify that the new remote URL has been added
git remote -v
# You should see something like:
# origin    git@github.com:YOUR_USERNAME/ParalleleNebenlaeufigeVerteilteProgrammierung_ws25.git (fetch)
# origin    git@github.com:YOUR_USERNAME/ParalleleNebenlaeufigeVerteilteProgrammierung_ws25.git (push)
# upstream  https://github.com/se-tuebingen-exercises/pcd-ws25.git (fetch)
# upstream  https://github.com/se-tuebingen-exercises/pcd-ws25.git (push)

# 3. Fetch changes from the upstream repository
git fetch upstream

# 4. Merge the changes from upstream/main into your currently checked out branch (usually 'main')
git merge upstream/main
```

**Explanation:**
- `git remote add upstream ...`  
  Adds the instructor's repository as a remote source named `upstream`.
- `git remote -v`  
  Lists all remotes so you can verify `upstream` was added successfully.
- `git fetch upstream`  
  Downloads changes from the upstream repository without merging them.
- `git merge upstream/main`  
  Integrates upstream changes into your local branch.

Repeat `fetch`/`merge` regularly to stay up to date with new course material.

## Nix Cleanup Guide (Ubuntu, Non-NixOS)

This procedure removes old development shells, unused store paths, stale flake inputs, and root-owned GC roots. It safely frees disk space without uninstalling Nix.

### 1. Remove stale GC roots from `nix develop`

```bash
sudo rm -f /nix/var/nix/gcroots/auto/*
```

### 2. Ensure root can access Nix binaries

If needed, adjust sudo secure_path via:

```bash
sudo visudo
```

Add:

```
Defaults secure_path="/nix/var/nix/profiles/default/bin:/nix/var/nix/profiles/default/sbin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
```

### 3. Full garbage collection

```bash
sudo nix-collect-garbage --delete-old
sudo nix-store --gc
```

### 4. Deduplicate and optimize store

```bash
sudo nix-store --optimize
```

### Optional: Create a clean profile for your user

```bash
sudo mkdir -p /nix/var/nix/profiles/per-user/$USER
sudo chown -R $USER:$USER /nix/var/nix/profiles/per-user/$USER
nix profile install nixpkgs#hello
```

### Verify cleanup impact

```bash
sudo du -sh /nix/store
```

A significant reduction (several GB reclaimed) confirms success.

## License

The material is licensed under the Creative Commons Attribution 4.0
International License (CC BY 4.0).

You are free to share and adapt the contents, even for commercial purposes, as
long as you give appropriate credit.

License text: https://creativecommons.org/licenses/by/4.0/

