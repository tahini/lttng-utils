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

import os
import re
import yaml
import logging

class Profile:

    def __init__(self):
        self.searchpath = [ os.path.join(os.path.dirname(os.path.realpath(__file__)), "profiles/"),
                os.path.join(os.path.expanduser('~'), ".lttng-utils/profiles/"),
                os.path.join(os.getcwd(), "profiles/")]

    def _find_event_file(self, name):
        for dir in self.searchpath:
            if dir is None:
                continue
            evfile = os.path.join(dir, name)
            if os.path.exists(evfile):
                return evfile
        return None

    def _merge_event_list(self, add_to, concat):
        for ev in concat:
            if not ev in add_to:
                add_to.append(ev)

    def _load_profile(self, name):
        evfile = name
        if (not os.path.exists(name)):
            evfile = self._find_event_file(name + ".profile")
        if (evfile is None):
            logging.warning("tracing profile " + name + " not found")
            return None
        profile = yaml.safe_load(open(evfile))
        if "ust" not in profile:
            profile["ust"] = []
        if "jul" not in profile:
            profile["jul"] = []
        if "kernel" not in profile:
            profile["kernel"] = []
        if "preload" not in profile:
            profile["preload"] = []
        if "includes" in profile:
            # load and merge the included profiles
            subLists = self.load_profiles(profile["includes"])
            self._merge_event_list(profile["kernel"], subLists["kernel"])
            self._merge_event_list(profile["ust"], subLists["ust"])
            self._merge_event_list(profile["jul"], subLists["jul"])
            self._merge_event_list(profile["preload"], subLists["preload"])
        return profile

    def load_profiles(self, names):
        evLists = { "kernel": [], "ust": [], "jul": [], "preload": [] }
        for name in names:
            profile = self._load_profile(name)
            if profile is None:
                print("Unknown profile '" + name + "'. You can see the available profiles with ./lttng-record-trace --list-profiles")
                continue;
            self._merge_event_list(evLists["kernel"], profile["kernel"])
            self._merge_event_list(evLists["ust"], profile["ust"])
            self._merge_event_list(evLists["jul"], profile["jul"])
            self._merge_event_list(evLists["preload"], profile["preload"])
        return evLists

    def get_profiles(self):
        profiles = {}
        for dir in self.searchpath:
            if dir is None:
                continue
            for dirname, dirnames, filenames in os.walk(dir):
                for filename in filenames:
                    if (filename.endswith(".profile")):
                        profile_name = re.sub('\.profile$', '', filename)
                        if profile_name not in profiles:
                            profile = yaml.safe_load(open(dirname + filename))
                            if (profile is not None):
                                profile["file"] = dirname + filename
                                profiles[profile_name] = profile
        return profiles

    def print_profiles(self):
        print("Profile search paths: " + ", ".join(self.searchpath))
        print("")
        profiles = self.get_profiles()
        print("Available profiles:")
        print("")
        for p in profiles.keys():
            try:
                profile = profiles[p]
                desc = ""
                if "desc" in profile:
                    desc = profile["desc"]
                print('{:<7}{:<15}{:<25}'.format("", p, desc))
                if "includes" in profile:
                    print('{:<7}{:<15}{:<25}'.format("", "", "Includes profiles: " + ", ".join(profile["includes"])))
            except Exception as e:
                print("Error handling profile '" + p + "'")


    def _print_list(self, list, text):
        if list is None:
            return
        print('{:<7}{:<15}{:<25}'.format("", text, ""))
        for l in list:
            print('{:<7}{:<15}{:<25}'.format("", "", l))

    def print_profiles_detail(self, profiles_to_print):
        profiles = self.get_profiles()
        for p in profiles_to_print:
            if p not in profiles:
                print("Unknown profile: " + p)
                print("")
                continue
            profile = profiles[p]
            print("'" + p + "' profile detail:")
            print('{:<7}{:<15}{:<25}'.format("", "File:", profile["file"]))
            if "kernel" in profile:
                self._print_list(profile["kernel"], "Kernel events:")
            if "ust" in profile:
                self._print_list(profile["ust"], "Userspace events:")
            if "jul" in profile:
                self._print_list(profile["jul"], "JUL events:")
            if "includes" in profile:
                self._print_list(profile["includes"], "Included profiles:")
                print("")
                print("===== Included profiles details:")
                print("")
                self.print_profiles_detail(profile["includes"])
                print("====")
            print("")
