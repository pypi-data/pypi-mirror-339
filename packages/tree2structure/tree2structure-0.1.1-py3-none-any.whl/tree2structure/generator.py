import os


def create_from_structure(structure, base_path="."):
    for item in structure:
        folder_path = os.path.join(base_path, item["folder"]) if item[
                                                                     "folder"] != "." else base_path
        os.makedirs(folder_path, exist_ok=True)

        for file in item.get("files", []):
            file_path = os.path.join(folder_path, file["name"])
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(file.get("comment", "") + "\n")

        for sub in item.get("subfolders", []):
            create_from_structure([sub], folder_path)
