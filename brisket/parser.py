import subprocess
import os
import os.path as path
from pprint import pprint as pp
import sys

android_home = os.getenv("ANDROID_HOME")
if android_home is None:
    print("Could not find ANDROID_HOME")
    sys.exit(1)

sdkmanager = path.join(android_home, "tools/bin/sdkmanager")

def run_sdkmanager():
    output = subprocess.check_output([sdkmanager, "--list", "--verbose"], stderr=subprocess.DEVNULL)
    return output.decode()


installed_marker = "Installed packages:"
available_marker = "Available"
dashes_marker = "-------------"


s = run_sdkmanager()

installed, available = s.split(available_marker)


def parse_installed(raw):
    components = {}
    installed = raw.split(installed_marker)[1]
    installed = installed.split("-\n")[1]

    clean_installed = [i for i in installed.split("\n\n") if not i.startswith("\n")]
    for item in clean_installed:
        parts = item.splitlines()
        if not parts:
            continue
        component = parts[0].strip()
        components[component] = {}
        for line in parts[1:]:
            parsed_line = line.split(":")[-1].strip()
            if "Desc" in line:
                components[component]["description"] = parsed_line
            elif "Version" in line:
                components[component]["version"] = parsed_line
            elif "Installed" in line:
                components[component]["installed_location"] = parsed_line

    return components


def parse_available(raw):
    components = {}
    available = raw.split("--\n")[1]
    clean_available = [i for i in available.split("\n\n") if not i.startswith("\n")]

    for item in clean_available:
        parts = item.splitlines()
        if not parts:
            continue
        component = parts[0].strip()
        # print(component)
        components[component] = {}
        for line in parts[1:]:
            parsed_line = line.split(":")[-1].strip()
            if "Desc" in line:
                components[component]["description"] = parsed_line
            elif "Version" in line:
                components[component]["version"] = parsed_line
            else:
                print(line)


parse_available(available)