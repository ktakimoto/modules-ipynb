# Nbgitpuller
For the first part of this workshop, we'll practice copying a Github repository's contents to our Jupyter hub using [nbgitpuller](https://jupyterhub.github.io/nbgitpuller/).

nbgitpuller is a tool developed by Berkeley students. It generates the "interact" links that Data-8 students use to access their assignments. We're going to create an interact link to access the materials for this workshop.

First, go to the interact link generator at [https://jupyterhub.github.io/nbgitpuller/link.html](https://jupyterhub.github.io/nbgitpuller/link.html). The notebook we want to link to is called style.ipynb, located in the "notebooks" folder.

The link generator needs four things:
1. The Jupyter hub url
2. The Github repository url
3. The Git branch
4. The path to the notebook file

Note that 3 and 4 can be blank; the generator will default to the "master" branch and the root directory of the repo.

For 1, the url for the Jupyter hub used by Modules is [https://datahub.berkeley.edu](https://datahub.berkeley.edu)

For 2, note that the repo url is the url at the root directory. If you're looking at a notebook file on Github, this will be everything before "blob" in the url.

4 is the path to the notebook file from the root directory. If you're looking at a notebook file on Github, this is everything after the branch name in the url.

Try making an interact link to the style.ipynb file!
