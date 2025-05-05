import os

EXCLUDE_DIRS = {'.git', 'venv', '__pycache__', '.idea', '.vscode'}
OUTPUT_FILE = "project_structure_md.txt"

def walk_directory(path, prefix=""):
    items = sorted(os.listdir(path))
    for index, name in enumerate(items):
        full_path = os.path.join(path, name)
        if any(excluded in full_path for excluded in EXCLUDE_DIRS):
            continue

        connector = "└── " if index == len(items) - 1 else "├── "
        print(prefix + connector + name)

        if os.path.isdir(full_path):
            extension = "    " if index == len(items) - 1 else "│   "
            walk_directory(full_path, prefix + extension)

if __name__ == "__main__":
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        original_stdout = os.sys.stdout
        os.sys.stdout = f
        print("# 📁 Структура проекта AI-Agent-Suite\n")
        print("```")
        walk_directory(".")
        print("```")
        os.sys.stdout = original_stdout
    print(f"Структура проекта сохранена в {OUTPUT_FILE}")
