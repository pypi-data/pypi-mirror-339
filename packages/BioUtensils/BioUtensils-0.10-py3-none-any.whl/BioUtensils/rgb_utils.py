import tifffile
from pathlib import Path
import re
import numpy as np
from .normalize import normalize_image
from typing import Tuple, List

def find_unique_identifier(base_path: Path, identifier=r"\b\d{6}\b", file_ending="*.[tT][iI][fF]") -> Tuple[list, list]:
    """
    Finds unique identifiers in file names within a given directory.

    Args:
        base_path (Path): The directory path where the function will look for files.
        identifier (str, optional): A regular expression pattern used to identify and extract unique identifiers from filenames. Defaults to r"\b\d{6}\b".
        file_ending (str, optional): A pattern to match filenames with specific file extensions, case-insensitively (e.g., .tif, .TIF). Defaults to "*.[tT][iI][fF]".

    Returns:
        Tuple[list, list]: A tuple containing:
            - all_files (list): List of all files matching the file_ending pattern.
            - unique_identifier (list): List of unique identifiers extracted from the filenames.
    """
    all_files = list(base_path.glob(file_ending))
    unique_identifier = list(set([re.findall(identifier, str(x))[0] for x in all_files]))

    return all_files, unique_identifier


def load_rgb(files: List[Path], identifier: List[str] = ["-r.", "-g.", "-b."]) -> np.ndarray:
    """
    Loads RGB images from a list of files, normalizes, and stacks them.

    Args:
        files (List[Path]): List of file paths to search through.
        identifier (List[str], optional): List of substrings to identify red, green, and blue channels in filenames. Defaults to ["-r.", "-g.", "-b."].

    Returns:
        np.ndarray: The normalized RGB image as a numpy array.
    """
    stack = []
    for c in identifier:
        if c is None:
            stack.append(None)
            continue
        file = [x for x in files if c in str(x).lower()][0]
        stack.append(tifffile.imread(file))

    sizes = [im.shape for im in stack if im is not None]
    assert len(sizes) != 0
    size_to_fill = sizes[0]

    rgb_stack = []
    for im in stack:
        rgb_stack.append(im if im is not None else np.zeros(size_to_fill))

    rgb_image = normalize_image(np.stack(rgb_stack).transpose(1, 2, 0))

    return rgb_image


def get_matching_files(all_files: List[Path], unique_identifier: str) -> List[Path]:
    """
    Finds all files that match a given unique identifier.

    Args:
        all_files (List[Path]): List of all files to search through.
        unique_identifier (str): The unique identifier to match in filenames.

    Returns:
        List[Path]: List of files that match the unique identifier.
    """
    matches = [x for x in all_files if unique_identifier in str(x)]

    return matches