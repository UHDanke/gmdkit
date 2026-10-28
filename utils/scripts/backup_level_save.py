# Imports
import argparse
import sys
from pathlib import Path
from typing import Optional

# Package Imports
from gmdkit import LevelSave
from gmdkit.constants.paths.save import LOCAL_LEVELS_PATH, AUTOBACKUPS_PATH


def backup_levels(save_path:Path, output_path:Path, name_filter:Optional[str]=None) -> int:

    output_path.mkdir(parents=True, exist_ok=True)

    level_save = LevelSave.from_file(save_path)  
    count = 0
    for level in level_save.levels:
        name = str(level.name)
        path = level.create_backup(output_path)
        print(f"Backed up '{name}' -> {path.name}")
        count += 1

    print(f"Backed up {count} level{'s' if count != 1 else ''} to {output_path}")
    return count


def ask(prompt:str, default, required:bool=False):
    while True:
        answer = input(f"{prompt} [{default if default is not None else 'none'}]: ").strip().strip('"')
        value = answer or default
        if value is not None or not required:
            return value
        print(f"{prompt} is required.")


if __name__ == "__main__":

    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Back up local levels as .gdlvl files in the game's auto-backup format.")
        parser.add_argument("output", nargs="?", type=Path, default=AUTOBACKUPS_PATH, help="output folder (default: the game's auto_backups folder)")
        parser.add_argument("--save", type=Path, default=LOCAL_LEVELS_PATH, help="CCLocalLevels.dat to read")
        parser.add_argument("--filter", default=None, help="only back up levels whose name contains this text")
        args = parser.parse_args()

        save_path = args.save
        output_path = args.output
        name_filter = args.filter

    else:
        print("Press Enter to keep the value in brackets.")
        save_path = Path(ask("Level save", LOCAL_LEVELS_PATH, required=True))
        output_path = Path(ask("Output folder", AUTOBACKUPS_PATH, required=True))
        name_filter = ask("Name filter", None)

    backup_levels(save_path, output_path, name_filter)
    