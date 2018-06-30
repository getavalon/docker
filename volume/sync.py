import os
import json

import gazu
from avalon import io as avalon
from avalon.vendor import toml


def main(apps):
    """Syncing CGWire with Avalon.

    Args:
        apps: List of applications to add to projects. Example:
            [{"name": "maya2015", "label": "Autodesk Maya 2015"}]
    """

    projects = []
    objects = []

    for project in gazu.project.all_projects():
        assets = gazu.asset.all_assets_for_project(project)
        shots = gazu.shot.all_shots_for_project(project)

        for assets, silo in ((assets, "assets"), (shots, "shots")):
            for asset in assets:
                objects.append({
                    "schema": "avalon-core:asset-2.0",
                    "name": asset["name"].replace(" ", ""),  # remove spaces
                    "silo": silo,
                    "data": {},
                    "type": "asset",
                    "parent": project["name"],
                })

        projects.append({
            "schema": "avalon-core:project-2.0",
            "type": "project",
            "name": project["name"],
            "data": {},
            "parent": None,
            "config": {
                "schema": "avalon-core:config-1.0",
                "apps": apps,
                "tasks": [
                    {"name": task["name"]}
                    for task in gazu.task.all_task_types()
                ],
                "template": {
                    "work":
                        "{root}/{project}/{silo}/{asset}/work/"
                        "{task}/{app}",
                    "publish":
                        "{root}/{project}/{silo}/{asset}/publish/"
                        "{subset}/v{version:0>3}/{subset}.{representation}"
                }
            }
        })

    print("Found:")
    print("- %d projects" % len(projects))
    print("- %d assets" % len(objects))

    os.environ["AVALON_PROJECTS"] = r""
    os.environ["AVALON_PROJECT"] = "temp"
    os.environ["AVALON_ASSET"] = "bruce"
    os.environ["AVALON_SILO"] = "assets"
    os.environ["AVALON_CONFIG"] = "polly"
    os.environ["AVALON_MONGO"] = "mongodb://192.168.99.100:27017"

    existing_projects = {}
    existing_assets = {}

    print("Fetching Avalon data..")
    avalon.install()
    for project in avalon.projects():
        existing_projects[project["name"]] = project

    for asset in avalon.find({"type": "asset"}):
        existing_assets[asset["name"]] = asset

    print("Synchronising..")
    for project in projects:
        if project["name"] in existing_projects:
            continue

        print("Installing project: %s" % project["name"])
        os.environ["AVALON_PROJECT"] = project["name"]
        avalon.uninstall()
        avalon.install()

        avalon.insert_one(project)

    for asset in objects:
        if asset["name"] in existing_assets:
            continue

        asset["parent"] = avalon.locate([asset["parent"]])
        print("Installing asset: %s" % asset["name"])
        avalon.insert_one(asset)

    print("Success")


if __name__ == '__main__':
    import time

    print("Logging in..")
    gazu.client.set_host("http://192.168.99.100/api")
    gazu.log_in("admin@example.com", "default")
    print("Logged in..")

    # Get applications
    print("Scanning for applications..")
    path = os.path.abspath(os.path.join(__file__, "..", "bin"))
    apps = []
    for f in os.listdir(path):
        if f.endswith(".toml"):
            apps.append(
                {
                    "name": f.replace(".toml", ""),
                    "label": toml.load(os.path.join(path, f))["label"]
                }
            )
    print("Applications found:\n{0}".format(json.dumps(apps, indent=4)))

    while True:
        print("Syncing..")
        main(apps)
        print("Sleeping for 10 seconds..")
        time.sleep(10)
