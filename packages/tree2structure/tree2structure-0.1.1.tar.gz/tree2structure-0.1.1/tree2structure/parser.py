import re


def parse_structure(raw: str):
    lines = raw.strip().splitlines()
    root = re.sub(r"[│├└─]+", "", lines[0]).strip().rstrip("/")
    stack = [{"folder": ".", "files": [], "subfolders": []}]
    last_indent = -1

    for line in lines[1:]:
        indent = len(re.match(r"^(\s*│? *).*", line).group(1).replace("│", "    "))
        clean = re.sub(r"[│├└─]+", "", line).rstrip()
        if not clean.strip():
            continue

        if "#" in clean:
            name, comment = map(str.strip, clean.split("#", 1))
            comment = f"# {comment}"
        else:
            name = clean.strip()
            comment = ""

        is_file = "." in name
        node = {"name": name, "comment": comment} if is_file else None

        while indent <= last_indent:
            stack.pop()
            last_indent -= 4

        parent = stack[-1]
        if is_file:
            parent.setdefault("files", []).append(node)
        else:
            folder = {"folder": name, "files": [], "subfolders": []}
            parent["subfolders"].append(folder)
            stack.append(folder)
            last_indent = indent

    def clean_output(folder):
        result = []
        for child in folder.get("subfolders", []):
            out = {
                "folder": child["folder"],
            }
            if child["files"]:
                out["files"] = child["files"]
            if child["subfolders"]:
                out["subfolders"] = clean_output(child)
            result.append(out)
        return result

    root_files = stack[0].get("files", [])
    final = clean_output(stack[0])
    if root_files:
        final.append({"folder": ".", "files": root_files})
    return final
