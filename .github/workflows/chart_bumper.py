from pathlib import Path
import subprocess
import yaml
import os


# Add charts here where it is known that higher versions are not
# yet stable or that you would like to disable automatic upgrades for
EXCLUDED_CHARTS = []

# Inject a BUMP_MAJOR env variable if you would like the script to automatically
# bump major chart versions too. Make sure you inspect the upgrade instructions before merging!
BUMP_MAJOR = os.environ.get("BUMP_MAJOR") == "true"


def update_chart(path_chart: str):
    """
    Given a path to a helm chart, bump the version of the dependencies of this chart
    if any newer versions exist.
    """

    with open(path_chart + "/Chart.yaml") as f:
        text = f.read()

    chart: dict = yaml.safe_load(text)

    if not "dependencies" in chart:
        return

    for i, dependency in enumerate(chart["dependencies"]):

        if dependency["name"] in EXCLUDED_CHARTS:
            print(f"Skipping {dependency['name']} because it is excluded..")
            continue

        # Bump major or minor depending on the set env variable
        version = f"{dependency['version'].split('.')[0]}.*.*" if not BUMP_MAJOR else "*.*.*"
        manifest = f"""
sources:
  latestMinorRelease:
    kind: helmChart
    spec:
      url: "{dependency["repository"]}"
      name: "{dependency["name"]}"
      version: "{version}"
conditions: {{}}
targets:
  chart:
    name: "Bump Chart dependencies"
    kind: helmChart
    spec:
      name: "{path_chart}"
      file: "Chart.yaml"
      key: "dependencies[{i}].version"
      versionIncrement: "patch"
"""

        with open("manifest.yaml", "w") as f:
            f.write(manifest)

        subprocess.run(["updatecli", "apply", "--config", "manifest.yaml"])


def main():
    # Modify the path_chart variable to point to the directory where your charts are located
    path_chart = "charts/jaegertracing"

    update_chart(path_chart)


if __name__ == "__main__":
    main()
