import os
import sys
import tomllib
from typing import Any


def read_pyproject(pyproject_path="pyproject.toml") -> dict[str, Any]:
  """Reads and returns the content of pyproject.toml as a dict.

  Args:
    pyproject_path: file path to pyproject.toml

  Returns: A dictionary parsed from the file
  """
  if not os.path.isfile(pyproject_path):
    sys.exit(f"{pyproject_path} not found.")
  with open(pyproject_path, "rb") as f:
    data = tomllib.load(f)
    return data


def extract_project_data(pyproject_data: dict[str, Any]) -> dict[str, Any]:
  """Extract desired fields from the pyproject.toml file.

  Args:
    pyproject_data: dictionary representation of pyproject.toml

  Returns:
    a dictionary with the relevant entries for meta.yaml
  """
  project = pyproject_data.get("project", {})
  # Basic info
  name = project.get("name", "unknown-package")
  version = project.get("version", "0.0.0")
  authors_data = project.get("authors", [])
  # Join authors names if available (authors entries are expected to be dicts with "name" key)
  authors = (
    ", ".join(author.get("name", "") for author in authors_data)
    if authors_data
    else "Unknown"
  )
  description = project.get("description", "")
  readme = project.get("readme", "")
  license_info = project.get("license", {})
  license_files = ", ".join(project.get("license-files", []))
  # license may be a dict with "text" or "file", or a string.
  if isinstance(license_info, dict):
    license_str = license_info.get("text") or license_info.get("file") or "Unknown"
  else:
    license_str = license_info
  pyversion = project.get("requires-python", "")
  dependencies = project.get("dependencies", [])
  # Dev dependencies can be stored in an optional dependency group.
  # The key name can vary. We'll try to find a group named 'dev' or 'development'
  dev_deps = pyproject_data.get("dependency-groups", {}).get("dev", [])
  sys_deps = pyproject_data.get("tool.condabuild", {}).get("system-dependencies", [])
  return {
    "name": name,
    "version": version,
    "description": description,
    "authors": authors,
    "readme": readme,
    "license": license_str,
    "license-files": license_files,
    "pyversion": pyversion,
    "dependencies": dependencies,
    "dev_dependencies": dev_deps,
    "sys_dependencies": sys_deps,
  }


def generate_meta_yaml(data: dict[str, Any], output_path="meta.yaml") -> None:
  """Generate a meta.yaml content from the extracted data and write to file."""
  # Create the meta.yaml as a multi-line string.
  meta_yaml = f"""
package:
  name: {data["name"]}
  version: "{data["version"]}"

source:
  path: ../..

build:
  noarch: python
  number: 0
  script: "{{{{ PYTHON }}}} -m pip install . --no-deps -vv"

requirements:
  host:
  - python {data["pyversion"]}
  - pip
  build:
  - python {data["pyversion"]}
"""

  # igne dev dependencies for now
  # if data["dev_dependencies"]:
  #   for dep in data["dev_dependencies"]:
  #     meta_yaml += f"  - {dep}\n"

  # Add dependencies from pyproject.toml, if any.
  meta_yaml += "  run:\n"
  if data["dependencies"]:
    for dep in data["dependencies"]:
      meta_yaml += f"  - {dep}\n"
  if data["sys_dependencies"]:
    for dep in data["sys_dependencies"]:
      meta_yaml += f"  - {dep}\n"
  else:
    print("No system dependencies!")

  meta_yaml += f"""
test:
  imports:
  - {data["name"]}" 

about:
  home: https://github.com/courtotlab/{data["name"]}
  license: {data["license"]}
  license_file: {data["license-files"]}
  summary: {data["description"]}
"""

  # Write the meta.yaml file
  with open(output_path, "w") as f:
    f.write(meta_yaml)
  print(f"meta.yaml has been generated at {output_path}")


def main(toml_path:str,yaml_path:str):
  pyproject = read_pyproject(toml_path)
  project_data = extract_project_data(pyproject)
  generate_meta_yaml(project_data, yaml_path)


if __name__ == "__main__":
  
  args = sys.argv[1:]
  toml_path = args[0]
  yaml_path = args[1]
  main(toml_path,yaml_path)
