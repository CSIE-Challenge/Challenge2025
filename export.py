import os
import zipfile

AGENT_DIR = "./agent"
EXPORT_DIR = "./export"
ZIP_NAME = "agent.zip"
ZIP_PATH = os.path.join(EXPORT_DIR, ZIP_NAME)

EXCLUDE_PATHS = [
    os.path.join(AGENT_DIR, "api", "__pycache__"),
    os.path.join(AGENT_DIR, "tests"),
    os.path.join(AGENT_DIR, "agent/boss")
]


def should_exclude(file_path):
    return any(file_path.startswith(exclude) for exclude in EXCLUDE_PATHS)


def zip_ai_folder():
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(AGENT_DIR):
            dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]

            for file in files:
                full_path = os.path.join(root, file)
                if should_exclude(full_path):
                    continue

                relative_path = os.path.relpath(full_path, os.path.dirname(AGENT_DIR))
                zipf.write(full_path, arcname=relative_path)

    print(f"Zipped {AGENT_DIR} to {ZIP_PATH}")


if __name__ == "__main__":
    zip_ai_folder()
