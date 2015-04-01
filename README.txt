ModTest.py: The module testing framework of the future.

-------
Purpose
-------

One of the most straightforward ways to test that a software module installed
at MSI actually works (at least in a cursory way) is to simply `module load`
it and try to run the software.

When testing many, many many different modules, this process of `module load
softwareName/version; sofwareName; module unload sofwareName` can become
incredibly tedious and error prone.

Furthermore, many of the programs like to helpfully place config files in your
home directory, an argument for which could be made if you were a frequent
user, but if you're just trying to run the software one time, you don't want
hundreds of config files for things you're not likely to ever touch again
clogging up your home. Another, related problem is that of certain programs
expecting to be started with a working directory that will contain their
result files. As a person just testing to see if something works, you don't
necessarily want bogus result files that you'll later have to track down and
remove proliferating either.

This script is designed to automate the process somewhat. Give it the name of
a software module that you want to test, and it will do its best to create an
environment that software which decides to place files all over the place can
still operate as it normally would (giving you an idea as to whether it works
at all), without making a mess of your carefully curated home directory, all
with minimal work from you.

-----
Usage
-----

The arguments for ModTest are arranged as follows:

    ModTest.py [list_of_modules] [: [list_of_shell_commands]]

The list of modules is optional.
The list of shell commands is also optional. If you include the list of shell
commands, you tell the program that they are coming by adding a single colon.

If you run ModTest.py with only a list of modules, its default behavior is to
load the modules one after another, and then try to run the program with the
name of the last module you loaded. For example:

    ModTest.py gcc/4.9.2 matlab/R2015a

Would load gcc/4.9.2, then it would load matlab/R2015, and then it would run
the shell command "matlab". This default behavior is because the vast majority
of the modules are named after the executable that they represent. In the
majority of cases, this is the way that you'll probably use ModTest.

Sometimes, however, the name of the executable is /not/ the same as the name
of the module. That's what the list of shell commands is for.

If you put a colon in the arguments, then it will completely override its
default behavior after it's loaded the modules (which is to simply run the
program command and then exit immediately), and all the script that it
generates will do is set up the jail.

    ModTest.py dstudo/4.1 : DiscoveryStudo41 exit

Would set up the jail, load the dstudio module, then run DiscoveryStudio41,
then immediately exit.

    ModTest.py pig : 'echo $PATH' exit

Would load the "pig" module, then it would display the PATH that the module
sets up. Note well the use of single quotes, to prevent the shell from
expanding your CURRENT path. Always use single quotes in the shell
command arguments unless you have a specific reason not to.

Finally, another useful thing you can do is load no modules, and run no
commands.

    ModTest.py :

This just gives you a jail'd shell, which can be useful.

-------------
Miscellaneous
-------------

Beware that it creates the jails and boilerplate scripts in directories called
"prisons" and "boilerplates", which must be located in the same directory as
ModTest.py is. Also, it does not remove any of the scripts after you've run it
until you run the next, so that you can either re-run one or look at the shell
script that it generated in order to make debugging slightly easier.

It names them after the host you're running on (by reading the HOSTNAME
variable from your environment). This is so you can have multiple jails going
at the same time on different hosts without interfering with one another.

It will also create a symbolic link to your actual ~/.Xauthority so that GUI
programs will still load inside the jailed shell when run through SSH.

Also, Java program have a special way of figuring out your real home directory
and ignoring the $HOME variable. The boilerplate script sets some java options
to override this behavior, but in some cases this can itself override
important variables like the max heap allocation. So, /most/ of the time it
plays well with Java programs, but sometimes it has had trouble in the past
with things like Matlab.
