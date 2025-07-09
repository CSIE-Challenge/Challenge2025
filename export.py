import os
import zipfile

AI_DIR = "./ai"
EXPORT_DIR = "./export"
ZIP_NAME = "ai.zip"
ZIP_PATH = os.path.join(EXPORT_DIR, ZIP_NAME)

EXCLUDE_PATHS = [
    os.path.join(AI_DIR, "api", "__pycache__")
]


def should_exclude(file_path):
    return any(file_path.startswith(exclude) for exclude in EXCLUDE_PATHS)


def zip_ai_folder():
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(AI_DIR):
            dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]

            for file in files:
                full_path = os.path.join(root, file)
                if should_exclude(full_path):
                    continue

                relative_path = os.path.relpath(full_path, os.path.dirname(AI_DIR))
                zipf.write(full_path, arcname=relative_path)

    print(f"Zipped {AI_DIR} to {ZIP_PATH}")


if __name__ == "__main__":
    zip_ai_folder()
