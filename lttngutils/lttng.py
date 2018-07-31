# The MIT License (MIT)
#
# Copyright (C) 2018 - Geneviève Bastien <gbastien@versatic.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import subprocess
import os
import logging
import getpass
import grp

__all__ = ["check_sessiond", "check_kernel_tracer", "check_ust_tracer"]

# the lttng command
LTTNG="lttng"

def check_sessiond():
    retcode = subprocess.call([LTTNG, "list"], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
    logging.debug("exit: " + str(retcode))

    if (retcode != 0):
        # See if the user is in the tracing group
        user = getpass.getuser()
        tracing_grp = grp.getgrnam('tracing')
        if (not user in tracing_grp[3]):
            # Display a messages to add the user to tracing group
            print("\x1b[1m\x1b[31mThe user is not in the 'tracing' group\x1b[0m")
            print("")
            print("You can add yourself to the tracing group with the following command, then logout and log back in:")
            print("")
            print("$ sudo usermod -a -G tracing <my_user>")
            print("")
            print("You may also run this script as 'sudo', but in this case, the trace will belong to the 'root' user and will not be readable by the user.")
        else:
            # Display a message to run the session daemon
            print("\x1b[1m\x1b[31mThe LTTNG session daemon is not running\x1b[0m")
            print("")
            print("It's preferable to run the session daemon as \x1b[1mroot\x1b[0m, as it is required to do \x1b[1mkernel tracing \x1b[0m, and for \x1b[1msome functionnalities of userspace tracing\x1b[0m. You can execute the following command:")
            print("")
            print("$ sudo systemctl start lttng-sessiond")
            print("")
            print("or")
            print("")
            print("$ sudo lttng-sessiond -d")
            print("")
            print("To trace \x1b[1monly userspace applications\x1b[0m, you can simply run")
            print("")
            print("$ lttng-sessiond -d")
        return False
    return True

def check_kernel_tracer():
    retcode = subprocess.call([LTTNG, "list", "-k"], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
    logging.debug("exit: " + str(retcode))

    if (retcode != 0):
        # Display a message to run the session daemon
        print("\x1b[1m\x1b[31mThe kernel tracer is not available but kernel events are requested\x1b[0m")
        print("")
        print("Make sure the \x1b[1mlttng-modules\x1b[0m package has been installed. You may check if it's available by running")
        print("")
        print("$ lttng list -k")
        print("")
        print("If compiling from source, make sure you compiled again after a kernel upgrade. Refer to the lttng web site for more info.")
        return False
    return True

def check_ust_tracer():
    retcode = subprocess.call([LTTNG, "list", "-u"], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
    logging.debug("exit: " + str(retcode))

    if (retcode != 0):
        # Display a message to run the session daemon
        print("\x1b[1m\x1b[31mThe userspace tracer is not available but userspace events are requested\x1b[0m")
        print("")
        print("Make sure the \x1b[1mlttng-ust\x1b[0m package has been installed. You may check if it's available by running")
        print("")
        print("$ lttng list -u")
        print("")
        print("If compiling from source, the lttng-tools package should be built after the userspace so it has ust support. Refer to the lttng web site for more info.")
        return False
    return True
