import shutil
from pathlib import Path
from datetime import datetime

import loguru
from rich.console import Console
from rich.panel import Panel

from .history import OperationHistory

console = Console()


def get_folder_path(file: Path, cleaning_plan: dict, unrecognized_file: Path) -> Path:
    """Determine the folder for a given file based on its extension.

    Supports nested categories in the cleaning plan.

    Args:
        file (Path): The file to determine the folder for.
        cleaning_plan (dict): The cleaning plan with possible nested categories.
        unrecognized_file (Path): The folder to return when the file extension is not found.

    Returns:
        Path: The folder for the given file.
    """

    def find_category(plan: dict, extension: str, current_path: Path = None) -> Path:
        for category, value in plan.items():
            if isinstance(value, dict):
                # If this is a nested category with "extensions" key, check it first
                if "extensions" in value and extension in value["extensions"]:
                    return current_path / category if current_path else Path(category)

                # Recursively search in subcategories
                sub_path = find_category(
                    value,
                    extension,
                    current_path / category if current_path else Path(category),
                )
                if sub_path:
                    return sub_path
            elif isinstance(value, list) and extension in value:
                return current_path / category if current_path else Path(category)
        return None

    # Start with the root path
    result = find_category(cleaning_plan, file.suffix)
    return result if result else unrecognized_file


def create_plans(
    source_dir: Path,
    cleaning_plan: dict,
    unrecognized_file: Path,
    **kwargs,
) -> tuple[list[tuple[Path, Path]], list[Path]]:
    """Generate plans for file transfers and directory deletions.

    Scans the source directory, creating a plan to move files based on the
    cleaning plan and a plan to delete directories found during the scan.
    Supports nested categories in the cleaning plan and excluding specific paths.

    Args:
        source_dir (Path): The directory to scan.
        cleaning_plan (dict): Configuration mapping file extensions to destination folders.
        unrecognized_file (Path): The base path for files with unrecognized extensions.
        **kwargs: Optional arguments. Supports 'excludes' (set): Paths to ignore.

    Returns:
        tuple[list[tuple[Path, Path]], list[Path]]: A tuple containing the
            transfer plan (list of source/destination pairs) and the delete
            plan (list of directories).
    """
    transfer_plan = []
    delete_plan = []
    excludes = kwargs.get("excludes", set()) or set()

    for filesystem_object in source_dir.rglob("*"):
        # Skip if the object is in excludes
        if any(filesystem_object.is_relative_to(excluded) for excluded in excludes):
            continue

        if filesystem_object.is_dir():
            delete_plan.append(filesystem_object)
        elif filesystem_object.is_file() and not filesystem_object.is_symlink():
            destination_folder = get_folder_path(
                filesystem_object, cleaning_plan, unrecognized_file
            )
            transfer_plan.append(
                (filesystem_object, destination_folder / filesystem_object.name)
            )

    return transfer_plan, delete_plan


def transfer_files(
    transfer_plan: list[tuple[Path, Path]],
    logger: loguru.logger,
    dry_run: bool,
    history: OperationHistory = None,
) -> tuple[int, int]:
    """
    Move files to designated folders based on sorting plan.

    If the destination file already exists, the function will create a new file
    with a copy number appended to the filename (e.g. "example.txt" would become
    "example_1.txt").

    Args:
        transfer_plan (list[tuple[Path, Path]]): A list of tuples, where the first
            element is the source file and the second element is the destination
            folder.
        logger (loguru.logger): The logger to use for logging.
        dry_run (bool): Whether to perform a dry run (i.e. do not actually move
            the files).
        history (OperationHistory, optional): History tracker for operations.

    Returns:
        tuple[int, int]: A tuple containing the number of files transferred and
            the total number of files in the transfer plan.
    """
    num_transferred_files = 0
    operations = []

    for source, destination in transfer_plan:
        copy_number = 1
        while destination.exists():
            destination = destination.with_name(
                f"{destination.stem}_{copy_number}{destination.suffix}"
            )
            copy_number += 1

        if dry_run:
            msg = f"MOVE_FILE [DRY-RUN] | FROM: {source} | TO: {destination}"
            operations.append(f"[yellow]{msg}[/yellow]")
            logger.info(msg)
        else:
            try:
                destination.parent.mkdir(parents=True, exist_ok=True)
                source.replace(destination)
                msg = f"MOVE_FILE [SUCCESS] | FROM: {source} | TO: {destination}"
                operations.append(f"[green]{msg}[/green]")
                logger.info(msg)
                num_transferred_files += 1
                if history:
                    history.add_operation("move", source, destination, datetime.now())
            except Exception as e:
                error_msg = (
                    f"MOVE_FILE [FAILED] | FROM: {source} | "
                    f"TO: {destination} | ERROR: {str(e)}"
                )
                operations.append(f"[red]{error_msg}[/red]")
                logger.error(error_msg)

    summary = (
        f"Total files processed: {len(transfer_plan)}\n"
        f"Successfully moved: [green]{num_transferred_files}[/green]\n"
        f"Failed: [red]{len(transfer_plan) - num_transferred_files}[/red]"
    )

    panel_content = "\n".join(
        [
            "[bold cyan]=== File Transfer Operations ===[/bold cyan]",
            *operations,
            "\n[bold cyan]=== File Transfer Summary ===[/bold cyan]",
            summary,
        ]
    )
    console.print(Panel(panel_content))

    logger.info(
        "=== File Transfer Summary ===\n"
        f"Total files processed: {len(transfer_plan)}\n"
        f"Successfully moved: {num_transferred_files}\n"
        f"Failed: {len(transfer_plan) - num_transferred_files}"
    )
    return num_transferred_files, len(transfer_plan)


def delete_dirs(
    delete_plan: list[Path],
    logger: loguru.logger,
    dry_run: bool,
    history: OperationHistory = None,
) -> tuple[int, int]:
    """
    Delete empty directories after moving files.

    Args:
        delete_plan (list[Path]): A list of directories to delete.
        logger (loguru.logger): The logger to use for logging.
        dry_run (bool): Whether to perform a dry run (i.e. do not actually delete
            the directories).
        history (OperationHistory, optional): History tracker for operations.

    Returns:
        tuple[int, int]: A tuple containing the number of directories deleted and
            the total number of directories in the delete plan.
    """
    deleted_paths = set()
    num_deleted_directories = 0
    operations = []

    for directory in delete_plan:
        if any(directory.is_relative_to(deleted) for deleted in deleted_paths):
            skip_msg = (
                "DELETE_DIR [SKIPPED] | "
                f"PATH: {directory} | "
                "REASON: Already deleted with parent directory"
            )
            operations.append(f"[yellow]{skip_msg}[/yellow]")
            logger.info(skip_msg)
            num_deleted_directories += 1
            continue

        if dry_run:
            msg = f"DELETE_DIR [DRY-RUN] | PATH: {directory}"
            operations.append(f"[yellow]{msg}[/yellow]")
            logger.info(msg)
        else:
            try:
                if directory.exists():
                    shutil.rmtree(directory)
                    deleted_paths.add(directory)
                    msg = f"DELETE_DIR [SUCCESS] | PATH: {directory}"
                    operations.append(f"[green]{msg}[/green]")
                    logger.info(msg)
                    num_deleted_directories += 1
                    if history:
                        history.add_operation(
                            "delete", directory, directory, datetime.now()
                        )
            except Exception as e:
                error_msg = f"DELETE_DIR [FAILED] | PATH: {directory} | ERROR: {str(e)}"
                operations.append(f"[red]{error_msg}[/red]")
                logger.error(error_msg)

    summary = (
        f"Total directories processed: {len(delete_plan)}\n"
        f"Successfully deleted: [green]{num_deleted_directories}[/green]\n"
        f"Failed: [red]{len(delete_plan) - num_deleted_directories}[/red]"
    )

    panel_content = "\n".join(
        [
            "[bold cyan]=== Directory Cleanup Operations ===[/bold cyan]",
            *operations,
            "\n[bold cyan]=== Directory Cleanup Summary ===[/bold cyan]",
            summary,
        ]
    )
    console.print(Panel(panel_content))

    logger.info(
        "=== Directory Cleanup Summary ===\n"
        f"Total directories processed: {len(delete_plan)}\n"
        f"Successfully deleted: {num_deleted_directories}\n"
        f"Failed: {len(delete_plan) - num_deleted_directories}"
    )
    return num_deleted_directories, len(delete_plan)
