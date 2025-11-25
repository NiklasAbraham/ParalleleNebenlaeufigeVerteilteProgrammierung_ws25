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

## License

The material is licensed under the Creative Commons Attribution 4.0
International License (CC BY 4.0).

You are free to share and adapt the contents, even for commercial purposes, as
long as you give appropriate credit.

License text: https://creativecommons.org/licenses/by/4.0/

