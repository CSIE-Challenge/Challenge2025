import os
import zipfile

AGENT_DIR = "./agent"
EXPORT_DIR = "./export"
ZIP_NAME = "agent.zip"
ZIP_PATH = os.path.join(EXPORT_DIR, ZIP_NAME)

WHITELIST = [
    "api/__init__.py",
    "api/constants.py",
    "api/game_client_base.py",
    "api/game_client.py",
    "api/logger.py",
    "api/serialization.py",
    "api/structures.py",
    "api/utils.py",
    "requirements.txt",
    "connection_test.py",
    "sample.py",
]


def main():
    os.makedirs(EXPORT_DIR, exist_ok=True)

    with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for path in WHITELIST:
            full_path = os.path.join(AGENT_DIR, path)
            if os.path.isfile(full_path):
                arcname = os.path.join("agent", path)
                zipf.write(full_path, arcname)
            else:
                print(f"Warning: {full_path} does not exist and is skipped.")

    print(f"Zipped {AGENT_DIR} to {ZIP_PATH}")


if __name__ == "__main__":
    main()
