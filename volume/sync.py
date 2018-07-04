import os

import gazu
from avalon import io as avalon


def main():
    projects = []
    objects = []
    tasks = [{"name": task["name"]} for task in gazu.task.all_task_types()]

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
                "apps": [
                    {
                        "name": "maya2015",
                        "label": "Autodesk Maya 2015"
                    },
                    {
                        "name": "maya2016",
                        "label": "Autodesk Maya 2016"
                    },
                    {
                        "name": "maya2017",
                        "label": "Autodesk Maya 2017"
                    },
                    {
                        "name": "nuke10",
                        "label": "The Foundry Nuke 10.0"
                    }
                ],
                "tasks": tasks,
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
            # Update task types
            existing_project = existing_projects[project["name"]]
            existing_project_task_types = existing_project["config"]["tasks"]
            if existing_project_task_types != tasks:
                print(
                    "Updating tasks types on \"{0}\" to:\n{1}".format(
                        project["name"], tasks
                    )
                )
                existing_project["config"]["tasks"] = tasks
                os.environ["AVALON_PROJECT"] = project["name"]
                avalon.uninstall()
                avalon.install()
                avalon.replace_one({"type": "project"}, existing_project)

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

    while True:
        print("Syncing..")
        main()
        print("Sleeping for 10 seconds..")
        time.sleep(10)
