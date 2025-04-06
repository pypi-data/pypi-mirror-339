import typer
import re
import os
import zipfile
import tarfile
import gzip
import shutil
import tempfile
from pathlib import Path
from typing_extensions import Annotated

app = typer.Typer()

def extract_member(archive, member_info, target_path: Path, pattern: re.Pattern):
    """Extracts a single member if it matches the pattern or is an archive itself."""
    member_name = ""
    member_data = None

    if isinstance(archive, zipfile.ZipFile):
        member_name = member_info.filename
        # Skip directories in zip files
        if member_info.is_dir():
            return
        # Check if the file name matches the pattern
        if pattern.search(member_name):
            print(f"Extracting matching file: {member_name}")
            archive.extract(member_info, path=target_path)
        # Check if the member itself is an archive to process recursively
        elif member_name.endswith(('.zip', '.tar.gz', '.gz', '.tgz')):
            print(f"Found nested archive: {member_name}")
            with tempfile.TemporaryDirectory() as tmpdir:
                nested_archive_path = Path(tmpdir) / Path(member_name).name
                # Extract the nested archive to a temporary location
                with archive.open(member_info) as source, open(nested_archive_path, 'wb') as dest:
                    shutil.copyfileobj(source, dest)
                # Process the nested archive
                process_archive(nested_archive_path, target_path, pattern)

    elif isinstance(archive, tarfile.TarFile):
        member_name = member_info.name
        # Skip directories in tar files
        if member_info.isdir():
            return
        # Check if the file name matches the pattern
        if pattern.search(member_name):
            print(f"Extracting matching file: {member_name}")
            # Use extractfile to handle potential path issues safely
            member_fileobj = archive.extractfile(member_info)
            if member_fileobj:
                output_file_path = target_path / Path(member_name).name # Extract to root of target_path
                output_file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_file_path, 'wb') as f_out:
                    shutil.copyfileobj(member_fileobj, f_out)
        # Check if the member itself is an archive to process recursively
        elif member_name.endswith(('.zip', '.tar.gz', '.gz', '.tgz')):
             print(f"Found nested archive: {member_name}")
             member_fileobj = archive.extractfile(member_info)
             if member_fileobj:
                 with tempfile.TemporaryDirectory() as tmpdir:
                     nested_archive_path = Path(tmpdir) / Path(member_name).name
                     with open(nested_archive_path, 'wb') as dest:
                         shutil.copyfileobj(member_fileobj, dest)
                     process_archive(nested_archive_path, target_path, pattern)

    elif isinstance(archive, gzip.GzipFile):
         # Gzip files contain only one file, the name is derived from the archive name
         # We assume the pattern should match the *archive* name for .gz files
         # Or we could try to infer the internal filename if needed, but let's keep it simple
         # If the .gz archive itself matches, extract its content
         # Note: The 'member_info' is the archive path itself for gzip
         archive_path = Path(str(member_info)) # member_info is the path here
         member_name = archive_path.stem # Use the name without .gz
         if pattern.search(archive_path.name): # Match against the .gz filename
             print(f"Extracting matching gzip content: {archive_path.name}")
             output_file_path = target_path / member_name
             output_file_path.parent.mkdir(parents=True, exist_ok=True)
             with open(output_file_path, 'wb') as f_out:
                 shutil.copyfileobj(archive, f_out)
         # Gzip cannot contain other archives directly, but the extracted content might be one
         # This case is handled when the extracted file is processed if needed elsewhere,
         # but direct recursion isn't applicable like zip/tar.


def process_archive(archive_path: Path, target_path: Path, pattern: re.Pattern):
    """Processes a single archive file (zip, tar.gz, gz)."""
    print(f"Processing archive: {archive_path}")
    try:
        if zipfile.is_zipfile(archive_path):
            with zipfile.ZipFile(archive_path, 'r') as archive:
                for member_info in archive.infolist():
                    extract_member(archive, member_info, target_path, pattern)
        elif tarfile.is_tarfile(archive_path):
            # Handle .tar.gz, .tgz, .tar
            mode = 'r:gz' if str(archive_path).endswith(('.gz', '.tgz')) else 'r'
            try:
                 with tarfile.open(archive_path, mode) as archive:
                    for member_info in archive.getmembers():
                        extract_member(archive, member_info, target_path, pattern)
            except tarfile.ReadError as e:
                 # Sometimes .gz might not be a tar file, could be just gzipped data
                 if mode == 'r:gz' and 'not a gzip file' not in str(e).lower():
                     # Try opening as plain gzip if tar.gz fails and error isn't about gzip format
                     try:
                         with gzip.open(archive_path, 'rb') as archive:
                             extract_member(archive, str(archive_path), target_path, pattern)
                     except Exception as gz_err:
                          print(f"Failed to open {archive_path} as tar.gz or gzip: {gz_err}")
                 else:
                     print(f"Failed to open {archive_path} as tar file: {e}")

        elif str(archive_path).endswith('.gz'):
             try:
                 with gzip.open(archive_path, 'rb') as archive:
                     # Pass archive_path as member_info for context in extract_member
                     extract_member(archive, str(archive_path), target_path, pattern)
             except Exception as e:
                 print(f"Failed to open {archive_path} as gzip file: {e}")
        else:
            print(f"Skipping unsupported file type: {archive_path}")
    except FileNotFoundError:
        print(f"Error: Archive file not found: {archive_path}")
    except Exception as e:
        print(f"Error processing archive {archive_path}: {e}")


@app.command()
def main(
    input_file: Annotated[Path, typer.Argument(exists=True, file_okay=True, dir_okay=False, readable=True, help="Path to the input archive file (.zip, .tar.gz, .gz).")],
    target_pattern: Annotated[str, typer.Argument(help="Regular expression pattern to match filenames.")],
    output_path: Annotated[Path, typer.Argument(file_okay=False, dir_okay=True, writable=True, resolve_path=True, help="Directory to extract matching files into.")]
):
    """
    Extracts files matching a regex pattern from an input archive (zip, tar.gz, gz),
    handling nested archives recursively.
    """
    try:
        pattern = re.compile(target_pattern)
    except re.error as e:
        print(f"Error: Invalid regex pattern '{target_pattern}': {e}")
        raise typer.Exit(code=1)

    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Input file: {input_file}")
    print(f"Target pattern: {target_pattern}")
    print(f"Output path: {output_path}")

    process_archive(input_file, output_path, pattern)

    print("Extraction process completed.")


if __name__ == "__main__":
    app()
