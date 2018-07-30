# lttng-utils

This repository contains helper scripts to record traces with LTTng for many common use cases.

### Requirements

This scripts requires the following packages to run:

  * [LTTng](http://lttng.org)
  * [Python](https://www.python.org) >= 3.4
  * [PyYaml](http://pyyaml.org) often available in distros as ``python3-yaml`` or ``python-yaml``
  * [Setuptools](https://pypi.python.org/pypi/setuptools) (for installation, not needed if running from directory)

### Install

#### Install from source

To install the helper script and profiles from the source

1. Install the required dependencies.
2. run the setup script from the project's root directory

```
$ git clone https://github.com/tahini/lttng-utils.git
$ cd lttng-utils
$ sudo python3 setup.py install
```

#### Install from the Git repository

To install LTTng utils directly from the git repository

1. Install the required dependencies.
2. Make sure ``pip`` for Python 3 is installed on your system. The package is named ``python3-pip`` on most distributions
   (``python-pip`` on Arch Linux).
3. Use ``pip3`` to install LTTng analyses:

```
$ sudo pip3 install --upgrade git+git://github.com/tahini/lttng-utils.git@master
```

### Usage

To simply record a trace with common kernel events that can then be analyzed with most of the analyses in [lttng-analyses](https://github.com/lttng/lttng-analyses) or opened in [Trace Compass](http://tracecompass.org). Tracing can be stopped by pressing ctrl-c.

```
$ lttng-record-trace
```

To trace a specific application, just add the application to trace to the arguments of the commands, for example, to trace only the ``ls -alt`` command

```
$ lttng-record-trace ls -alt
```

More options are available for tracing. See the helper

```
$ lttng-record-trace --help
```

### Profiles

LTTng-utils comes with a set of pre-defined profiles for common tracing use cases. Users can define their own profiles as well. The ``lttng-utils --list-profiles`` command will show the paths that are searched for profile, typically, the builtin script's path, ``$HOME/.lttng-utils/profiles/`` and a ``profiles/`` directory in the current directory. You can just create a new file named ``myprofile.profile`` in one of those directory and edit it. Profiles are yaml files with the following structure:

```
desc:
    A description of the profile that will appear when listing profiles
includes:
    list of profiles to include in this one
kernel:
    list of kernel events to enable, 'syscall' being a special event to enable all syscalls
ust:
    list of userspace events to enable
preload:
    list of libraries to preload when running the application to trace
```

Then you can run the trace recording script with the profile like this:

```
$ lttng-record-trace -p myprofile
```
