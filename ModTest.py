#!/usr/bin/env python3

"""
A script for creating pseudo-jails. Useful for testing software modules.  Kind
of similar to python's virtual env, but more generalized and centered around
the modulecmd utility.
"""

import os
import sys
import subprocess

from string import Template

TEMPLATE = """
#!/bin/bash
source /etc/profile
source $$HOME/.profile

PRISON="$prefix/prisons/$$HOSTNAME"
if [ ! -d "$$PRISON" ]; then
    mkdir "$$PRISON"
    ln -s "$$HOME/.Xauthority" "$$PRISON"
fi

export HOME="$$PRISON"
export _JAVA_OPTIONS="$$_JAVA_OPTIONS -Duser.home=$$HOME"
shopt -s expand_aliases
cd $$HOME

export PS1="{captive} $$PS1"
trap 'echo END SESSION' EXIT
echo 'BEGIN SESSION'

#begin
"""
TEMPLATE = Template(TEMPLATE.strip())

# Find where ModTest.py is stored...
BASEDIR = os.path.dirname(os.path.abspath(__file__))

# Create a "boilerplate" script with the current node's hostname.
SCRIPT = os.path.join(BASEDIR, "boilerplates", os.environ["HOSTNAME"])

DELIM = ":"

def resolve_module(module):
    """
    If the module begins with a ., then it will return the absolute path to the
    module file. This lets you make a local module (not in $MODULEPATH) and
    load it using this script.
    """
    if not module.startswith("."):
        return module

    return os.path.abspath(module)


def main(script, modules, cmds):
    with open(script, "wt") as init:
        init.write(TEMPLATE.substitute(prefix=BASEDIR))
        init.write("\n")

        for module in modules:
            init.write("module load {}\n".format(module))

        if cmds is None:
            if modules:
                lastmodule = modules[-1].partition("/")
                cmds = [lastmodule[0], "exit"]
            else:
                cmds = []

        for cmd in cmds:
            init.write("{}\n".format(cmd))
    
    ec = subprocess.call(["/bin/bash", "--init-file", script])
    exit(ec)

def get_help():
    print("Usage: Please see README.txt")

if __name__ == '__main__':
    args = sys.argv[1:]

    if DELIM in args:
        idx = args.index(DELIM)
        modules = [resolve_module(mod) for mod in args[:idx]]
        commands = args[idx+1:]
    else:
        modules = [resolve_module(mod) for mod in args]
        commands = None

    main(SCRIPT, modules, commands)
