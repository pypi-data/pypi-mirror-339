import os
import zipfile
from pathlib import Path
from fnmatch import fnmatch
import argparse
import sys
import mimetypes
from collections import defaultdict
from argparse import RawTextHelpFormatter
import platform
import shutil

def detect_shell():
    shell = os.environ.get('SHELL') or os.environ.get('COMSPEC')
    if shell:
        return shell.lower()
    return "unknown"

def check_exclude_patterns_for_shell_issues(excludes):
    shell = detect_shell()
    needs_quotes = any(("*" in pat or "?" in pat) and not (pat.startswith('"') or pat.startswith("'")) for pat in excludes)
    
    if needs_quotes and ('powershell' in shell or 'bash' in shell or 'zsh' in shell):
        print(
            "[!] You may be using an unquoted wildcard in --exclude (e.g., *.log).\n"
            "    Use quotes like \"*.log\" or '*.log' to avoid unexpected file expansion.\n"
        )

def parse_gitignore(gitignore_path):
    patterns = []
    with open(gitignore_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                patterns.append(line.rstrip('/'))
    return patterns

def is_ignored(rel_path, ignore_patterns, exclude_patterns):
    rel_path_str = rel_path.as_posix()
    for pattern in ignore_patterns + exclude_patterns:
        if fnmatch(rel_path_str, pattern) or fnmatch(rel_path_str, pattern + "/*"):
            return True
    return False

def format_size(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} TB"

def zip_project_folder(project_path: Path, zip_name: str = None, verbose: bool = False,
                       dry_run: bool = False, exclude: list = None, summary: bool = False,
                       show_info: bool = False):
    parent_dir = project_path.parent
    zip_path = parent_dir / (zip_name if zip_name else f"{project_path.name}.zip")

    gitignore_file = project_path / ".gitignore"
    ignore_patterns = parse_gitignore(gitignore_file) if gitignore_file.exists() else []
    exclude_patterns = exclude or []

    if show_info:
        print("ZipIt Configuration")
        print("--------------------")
        print(f"Current Directory : {project_path}")
        print(f"Output File       : {zip_path.name}")
        print(f"Dry Run           : {dry_run}")
        print(f"Verbose           : {verbose}")
        print(f"Summary           : {summary}")
        print(f"Excludes from CLI : {exclude_patterns}")
        print(f"Excludes from .gitignore ({len(ignore_patterns)} patterns)")
        print("--------------------\n")
        return

    files_to_zip = []
    total_skipped = 0
    total_size = 0
    file_types = defaultdict(int)

    for root, dirs, files in os.walk(project_path):
        root_path = Path(root)
        rel_root = root_path.relative_to(project_path)

        dirs[:] = [d for d in dirs if not is_ignored(rel_root / d, ignore_patterns, exclude_patterns)]

        for file in files:
            abs_path = root_path / file
            rel_path = abs_path.relative_to(project_path)
            zip_path_inside = Path(project_path.name) / rel_path

            if not is_ignored(rel_path, ignore_patterns, exclude_patterns):
                files_to_zip.append((abs_path, zip_path_inside))
                total_size += abs_path.stat().st_size
                mime_type, _ = mimetypes.guess_type(str(abs_path))
                ext = mime_type if mime_type else abs_path.suffix or 'unknown'
                file_types[ext] += 1
                if verbose or dry_run:
                    print(f"✔ {'Would zip' if dry_run else 'Zipped'}: {zip_path_inside}")
            else:
                total_skipped += 1
                if verbose or dry_run:
                    print(f"✘ Skipped: {rel_path}")

    if summary:
        print("\nSummary:")
        print(f"   Files to zip: {len(files_to_zip)}")
        print(f"   Skipped: {total_skipped}")
        print(f"   Total size: {format_size(total_size)}")
        print("   File types included:")
        for ftype, count in file_types.items():
            print(f"     - {ftype}: {count}")

    if dry_run:
        print("\nDry run: ZIP file was not created.")
        return

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for abs_path, zip_path_inside in files_to_zip:
            zipf.write(abs_path, zip_path_inside)

    print(f"\nZipped to: {zip_path}")

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Create a zip archive of the current directory.\n"
            "Files and folders listed in .gitignore or excluded by pattern will be skipped.\n"
            "\n"
            "Examples:\n"
            "  zipit                            # Zip current directory (uses folder name)\n"
            "  zipit --name my_backup.zip      # Custom zip name\n"
            "  zipit --verbose                 # Show included/skipped files\n"
            "  zipit --dry-run --summary       # Simulate and show summary only\n"
            "  zipit --exclude *.log temp/     # Manually exclude patterns\n"
            "\n"
            "Notes:\n"
            "  - .gitignore is respected automatically.\n"
            "  - Patterns use Unix-style wildcards (e.g., *.log, temp/, node_modules/)\n"
            "  - --dry-run does not create any zip, just shows actions.\n"
        ),
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument('--name', type=str,
                        help="Custom zip filename (e.g., output.zip). Default: <folder_name>.zip")
    parser.add_argument('--verbose', action='store_true',
                        help="Show each file that is included or skipped")
    parser.add_argument('--dry-run', action='store_true',
                        help="Only show what would be zipped, do not create the zip")
    parser.add_argument('--exclude', nargs='*', default=[],
                        help="Extra patterns to exclude (e.g., *.log temp/ node_modules/)")
    parser.add_argument('--summary', action='store_true',
                        help="Show total files zipped/skipped, total size, and file type breakdown")
    parser.add_argument('--info', action='store_true',
                        help="Show current zip configuration and exit")

    args = parser.parse_args()

    if args.exclude:
        check_exclude_patterns_for_shell_issues(args.exclude)

    current_dir = Path.cwd()
    zip_project_folder(
        current_dir,
        zip_name=args.name,
        verbose=args.verbose,
        dry_run=args.dry_run,
        exclude=args.exclude,
        summary=args.summary,
        show_info=args.info
    )

def run():
    main()

