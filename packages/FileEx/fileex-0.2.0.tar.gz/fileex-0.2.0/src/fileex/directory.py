from pathlib import Path
import shutil
import os

from fileex import exception

__all__ = ["delete_contents"]


def delete(
    path: str | Path,
    exclude: list[str] | None = None,
    raise_existence: bool = True
) -> tuple[list[Path], list[Path]] | tuple[None, None]:
    """Recursively delete files and directories within a given directory, excluding those specified by `exclude`.

    Parameters
    ----------
    path
        Path to the directory whose content should be deleted.
    exclude
        List of glob patterns to exclude from deletion.
        Patterns are relative to the directory specified by `path`.
        If a directory is excluded, all its contents will also be excluded.
    raise_existence : bool, default: True
        Raise an error when the directory does not exist.

    Returns
    -------
        Paths of the files and directories that were deleted and excluded, respectively,
        or None if the directory does not exist and `raise_existence` is set to False.

    Raises
    ------
    fileex.exception.FileExPathNotFoundError
        If the directory does not exist and `raise_existence` is set to True.
    """
    path = Path(path).resolve()
    if not path.is_dir():
        if raise_existence:
            raise exception.FileExPathNotFoundError(path, is_dir=True)
        return None, None

    excluded_paths = set()
    for pattern in exclude or []:
        for excluded_path in path.glob(pattern):
            excluded_paths.add(excluded_path)
            if excluded_path.is_dir():
                # Also exclude all contents of the directory
                excluded_paths.update(excluded_path.rglob("*"))

    deleted = []
    # Walk bottom-up so we can delete files before trying to delete directories
    for current_dir, dirs, files in os.walk(path, topdown=False):
        current_path = Path(current_dir)
        # Delete files
        for name in files:
            file_path = current_path / name
            if file_path.resolve() in excluded_paths:
                continue
            file_path.unlink()
            deleted.append(file_path)
        # Delete directories
        for name in dirs:
            dir_path = current_path / name
            if dir_path.resolve() in excluded_paths:
                continue
            shutil.rmtree(dir_path)
            deleted.append(dir_path)
    return deleted, list(excluded_paths)


def merge(
    source: str | Path,
    destination: str | Path,
    raise_existence: bool = True
) -> list[Path] | None:
    """Recursively merge a directory into another.

    All files and subdirectories in `source` will be moved to `destination`.
    Existing files in `destination` will be overwritten.

    Parameters
    ----------
    source
        Path to the source directory.
    destination
        Path to the destination directory.
    raise_existence
        Raise an error if the source directory does not exist.

    Returns
    -------
        Paths of the files and directories that were moved,
        or None if the source directory does not exist and `raise_existence` is set to False.

    Raises
    ------
    fileex.exception.FileExPathNotFoundError
        If the source directory does not exist and `raise_existence` is set to True.
    """
    source = Path(source).resolve()
    destination = Path(destination).resolve()
    moved_paths = []
    if not source.is_dir():
        if raise_existence:
            raise exception.FileExPathNotFoundError(source, is_dir=True)
        return None, None
    for item in source.iterdir():
        dest_item = destination / item.name
        if item.is_dir():
            if dest_item.exists():
                # Merge the subdirectory
                move_and_merge(item, dest_item)
            else:
                # Move the whole directory
                shutil.move(str(item), str(dest_item))
                moved_paths.append(dest_item)
        else:
            # Move or overwrite the file
            if dest_item.exists():
                # Remove the existing file
                dest_item.unlink()
            shutil.move(str(item), str(dest_item))
            moved_paths.append(dest_item)
    source.rmdir()
    return moved_paths
