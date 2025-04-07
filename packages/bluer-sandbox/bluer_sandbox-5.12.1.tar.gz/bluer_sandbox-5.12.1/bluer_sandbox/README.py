import os

from bluer_objects import file, README

from bluer_sandbox import NAME, VERSION, ICON, REPO_NAME


items = README.Items([])


def build():
    return README.build(
        items=items,
        path=os.path.join(file.path(__file__), ".."),
        ICON=ICON,
        NAME=NAME,
        VERSION=VERSION,
        REPO_NAME=REPO_NAME,
    )
