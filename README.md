# BLAST-lab-data-collection-codes

## Install
  `sudo ./install.sh`

## Setup node information
  Fill in the `node_info.py` file by defining the variables `SITENAME`, `HOSTNAME`, and `ROLE`.
  `SITENAME` is the site where the given node is installed, `HOSTNAME` is the unique name of
  the given node, and ROLE is either `master` or `edge`. `master` nodes log weather conditions,
  while `edge` nodes log light intensity and take images of a given crop site.

## Run
  `sudo ./startup.sh`

## Run on boot
