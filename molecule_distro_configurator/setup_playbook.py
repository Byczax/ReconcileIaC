import os
from ruamel.yaml import YAML


def edit_converge_yaml(relative_path):
    converge_yaml_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../molecule/default/converge.yml")
    )

    yaml = YAML()
    with open(converge_yaml_path, "r") as file:
        data = yaml.load(file)

    data[-1]["ansible.builtin.import_playbook"] = "../../" + relative_path

    with open(converge_yaml_path, "w") as file:
        yaml.dump(data, file)

    print(f"Successfully edited molecule.yaml with relative path: {relative_path}")


if __name__ == "__main__":
    import sys

    relative_path = sys.argv[1]
    edit_converge_yaml(relative_path)
