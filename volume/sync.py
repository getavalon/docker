import os
import gazu
from avalon import io as avalon


def main():
    projects = {}
    objects = {}
    objects_count = 0

    for project in gazu.project.all_projects():
        assets = gazu.asset.all_assets_for_project(project)
        shots = gazu.shot.all_shots_for_project(project)

        entities = {}
        for assets, silo in ((assets, "assets"), (shots, "shots")):
            for asset in assets:
                entity_type = gazu.entity.get_entity_type(
                    asset["entity_type_id"]
                )
                # Remove spaces for compatibility, lowercase for consistentcy
                name = asset["name"].replace(" ", "_").lower()
                entities[name] = {
                    "schema": "avalon-core:asset-2.0",
                    "name": name,
                    "silo": silo,
                    "type": "asset",
                    "parent": project["name"],
                    "data": {
                        "label": asset["name"],
                        "group": entity_type["name"]
                    },
                }

                objects_count += 1

        objects[project["name"]] = entities

        projects[project["name"]] = {
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
        }

    print("Found:")
    print("- %d projects" % len(projects))
    print("- %d assets" % objects_count)

    os.environ["AVALON_PROJECTS"] = r""
    os.environ["AVALON_PROJECT"] = "temp"
    os.environ["AVALON_ASSET"] = "bruce"
    os.environ["AVALON_SILO"] = "assets"
    os.environ["AVALON_CONFIG"] = "polly"
    os.environ["AVALON_MONGO"] = "mongodb://192.168.99.100:27017"

    existing_projects = {}
    existing_objects = {}

    print("Fetching Avalon data..")
    avalon.install()
    for project in avalon.projects():
        existing_projects[project["name"]] = project

        # Update project
        os.environ["AVALON_PROJECT"] = project["name"]
        avalon.uninstall()
        avalon.install()

        # Collect assets
        assets = {}
        for asset in avalon.find({"type": "asset"}):
            assets[asset["name"]] = asset

        existing_objects[project["name"]] = assets

    print("Synchronising..")
    for name, project in projects.items():
        if project["name"] in existing_projects:
            continue

        print("Installing project: %s" % project["name"])
        os.environ["AVALON_PROJECT"] = project["name"]
        avalon.uninstall()
        avalon.install()

        avalon.insert_one(project)

    for project_name, assets in objects.items():
        os.environ["AVALON_PROJECT"] = project_name
        avalon.uninstall()
        avalon.install()

        for asset_name, asset in assets.items():
            if asset_name in existing_objects.get(project_name, {}):
                continue

            asset["parent"] = avalon.locate([asset["parent"]])
            print("Installing asset: %s" % asset_name)
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
        print("Sleeing for 10 seconds..")
        time.sleep(10)
