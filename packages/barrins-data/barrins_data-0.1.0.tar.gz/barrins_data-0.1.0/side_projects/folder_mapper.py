from pathlib import Path

EXCLUDE = [".", "__", "venv", "folder_"]


def generate_directory_description(
    path: Path,
    file,
    indent=0,
    prefix="|-",
):
    for item in path.iterdir():
        if ".egg-info" in item.name or any(
            item.name.startswith(excl) for excl in EXCLUDE
        ):
            continue

        file.write("  " * indent + prefix + " " + item.name + "\n")
        if item.is_dir():
            generate_directory_description(item, file, indent + 1)


# Exemple d'utilisation
folder_path = Path(__file__).parent
output_file = Path(__file__).parent / "folder_structure.txt"

with open(output_file, "w") as file:
    generate_directory_description(folder_path, file)
