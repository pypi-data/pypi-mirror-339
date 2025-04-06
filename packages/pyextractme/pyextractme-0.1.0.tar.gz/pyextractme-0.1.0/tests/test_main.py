import pytest
import zipfile
import tarfile
import gzip
import shutil
import tempfile
import os
import re
from pathlib import Path
from typer.testing import CliRunner

# Assuming your main script is runnable and the typer app object is named 'app'
# Adjust the import path if your structure is different
from pyextractme.main import app

runner = CliRunner()

# Helper function to create a dummy file
def create_dummy_file(filepath: Path, content: str = "dummy content"):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)

# Fixture for temporary directories
@pytest.fixture(scope="function")
def temp_dirs():
    """Provides temporary input and output directories for a test."""
    with tempfile.TemporaryDirectory() as input_dir, tempfile.TemporaryDirectory() as output_dir:
        yield Path(input_dir), Path(output_dir)

# Fixture to create a sample zip archive
@pytest.fixture(scope="function")
def zip_archive(temp_dirs):
    input_dir, _ = temp_dirs
    archive_path = input_dir / "test_archive.zip"
    file1_path = input_dir / "file1.txt"
    file2_path = input_dir / "subdir" / "file2.log"
    create_dummy_file(file1_path, "content1")
    create_dummy_file(file2_path, "content2")

    with zipfile.ZipFile(archive_path, 'w') as zf:
        zf.write(file1_path, arcname="file1.txt")
        zf.write(file2_path, arcname="subdir/file2.log") # Include subdir structure
        zf.write(file1_path, arcname="another_file.txt") # Add another file
    return archive_path

# Fixture to create a sample tar.gz archive
@pytest.fixture(scope="function")
def targz_archive(temp_dirs):
    input_dir, _ = temp_dirs
    archive_path = input_dir / "test_archive.tar.gz"
    file1_path = input_dir / "itemA.csv"
    file2_path = input_dir / "nested" / "itemB.data"
    create_dummy_file(file1_path, "csv,data")
    create_dummy_file(file2_path, "binary data")

    with tarfile.open(archive_path, 'w:gz') as tf:
        tf.add(file1_path, arcname="itemA.csv")
        tf.add(file2_path, arcname="nested/itemB.data") # Include subdir structure
        tf.add(file1_path, arcname="another_item.csv") # Add another file
    return archive_path

# Fixture to create a sample gz archive
@pytest.fixture(scope="function")
def gz_archive(temp_dirs):
    input_dir, _ = temp_dirs
    file_to_compress = input_dir / "config.json"
    archive_path = input_dir / "config.json.gz"
    create_dummy_file(file_to_compress, '{"key": "value"}')

    with open(file_to_compress, 'rb') as f_in, gzip.open(archive_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    return archive_path

# Fixture for a nested zip archive (zip inside zip)
@pytest.fixture(scope="function")
def nested_zip_archive(temp_dirs):
    input_dir, _ = temp_dirs
    outer_archive_path = input_dir / "outer.zip"
    inner_archive_path = input_dir / "inner.zip"
    file_in_inner_path = input_dir / "nested_file.log"
    file_in_outer_path = input_dir / "outer_file.txt"

    # Create the file destined for the inner archive
    create_dummy_file(file_in_inner_path, "inner content")
    # Create the inner archive
    with zipfile.ZipFile(inner_archive_path, 'w') as inner_zf:
        inner_zf.write(file_in_inner_path, arcname="nested_file.log")

    # Create a file for the outer archive
    create_dummy_file(file_in_outer_path, "outer content")

    # Create the outer archive containing the inner archive and another file
    with zipfile.ZipFile(outer_archive_path, 'w') as outer_zf:
        outer_zf.write(inner_archive_path, arcname="inner_archive.zip")
        outer_zf.write(file_in_outer_path, arcname="outer_file.txt")

    return outer_archive_path

# Fixture for a nested tar.gz archive (zip inside tar.gz)
@pytest.fixture(scope="function")
def nested_targz_archive(temp_dirs):
    input_dir, _ = temp_dirs
    outer_archive_path = input_dir / "outer_mixed.tar.gz"
    inner_zip_path = input_dir / "inner.zip"
    file_in_inner_path = input_dir / "deep_file.data"
    file_in_outer_path = input_dir / "outer_config.cfg"

    # Create file for inner zip
    create_dummy_file(file_in_inner_path, "deep data")
    # Create inner zip
    with zipfile.ZipFile(inner_zip_path, 'w') as inner_zf:
        inner_zf.write(file_in_inner_path, arcname="deep_file.data")

    # Create file for outer tar.gz
    create_dummy_file(file_in_outer_path, "config settings")

    # Create outer tar.gz containing the inner zip and another file
    with tarfile.open(outer_archive_path, 'w:gz') as outer_tf:
        outer_tf.add(inner_zip_path, arcname="archives/inner.zip")
        outer_tf.add(file_in_outer_path, arcname="configs/outer_config.cfg")

    return outer_archive_path

# Fixture for an unsupported file type
@pytest.fixture(scope="function")
def unsupported_file(temp_dirs):
    input_dir, _ = temp_dirs
    file_path = input_dir / "document.txt"
    create_dummy_file(file_path, "This is not an archive.")
    return file_path

# Fixture for a plain GZ file (not tar.gz) - reusing gz_archive is fine for this


# --- Test Functions ---

def test_extract_zip_match(temp_dirs, zip_archive):
    """Test extracting a specific file from a zip archive."""
    _, output_dir = temp_dirs
    pattern = r"file1\.txt" # Match file1.txt exactly
    result = runner.invoke(app, [str(zip_archive), pattern, str(output_dir)])

    print(f"CLI Output:\n{result.output}") # Print output for debugging
    assert result.exit_code == 0
    assert "Extracting matching file: file1.txt" in result.output
    extracted_file = output_dir / "file1.txt"
    assert extracted_file.exists()
    assert extracted_file.read_text() == "content1"
    # Ensure other files are not extracted
    assert not (output_dir / "subdir" / "file2.log").exists()
    assert not (output_dir / "file2.log").exists() # Check it wasn't extracted to root
    assert not (output_dir / "another_file.txt").exists()

def test_extract_targz_match(temp_dirs, targz_archive):
    """Test extracting a specific file from a tar.gz archive."""
    _, output_dir = temp_dirs
    pattern = r"itemA\.csv" # Match itemA.csv exactly
    result = runner.invoke(app, [str(targz_archive), pattern, str(output_dir)])

    print(f"CLI Output:\n{result.output}")
    assert result.exit_code == 0
    assert "Extracting matching file: itemA.csv" in result.output
    extracted_file = output_dir / "itemA.csv"
    assert extracted_file.exists()
    assert extracted_file.read_text() == "csv,data"
    # Ensure other files are not extracted
    assert not (output_dir / "nested" / "itemB.data").exists()
    assert not (output_dir / "itemB.data").exists() # Check it wasn't extracted to root
    assert not (output_dir / "another_item.csv").exists()


def test_extract_gz_match(temp_dirs, gz_archive):
    """Test extracting content from a .gz archive when the archive name matches."""
    _, output_dir = temp_dirs
    pattern = r"config\.json\.gz" # Pattern matches the archive name itself
    result = runner.invoke(app, [str(gz_archive), pattern, str(output_dir)])

    print(f"CLI Output:\n{result.output}")
    assert result.exit_code == 0
    assert f"Extracting matching gzip content: {gz_archive.name}" in result.output
    extracted_file = output_dir / "config.json" # Expecting the uncompressed name
    assert extracted_file.exists()
    assert extracted_file.read_text() == '{"key": "value"}'

def test_extract_gz_no_match(temp_dirs, gz_archive):
    """Test .gz extraction when the pattern does not match the archive name."""
    _, output_dir = temp_dirs
    pattern = r"non_matching_pattern"
    result = runner.invoke(app, [str(gz_archive), pattern, str(output_dir)])

    print(f"CLI Output:\n{result.output}")
    assert result.exit_code == 0
    assert "Extracting matching gzip content" not in result.output # Should not extract
    assert not list(output_dir.iterdir()) # Output directory should be empty

def test_invalid_regex_pattern(temp_dirs, zip_archive):
    """Test providing an invalid regex pattern."""
    _, output_dir = temp_dirs
    invalid_pattern = r"[" # Invalid regex
    result = runner.invoke(app, [str(zip_archive), invalid_pattern, str(output_dir)])

    assert result.exit_code == 1 # Expecting non-zero exit code for error
    assert "Error: Invalid regex pattern" in result.output

def test_non_existent_input_file(temp_dirs):
    """Test providing a non-existent input file path."""
    input_dir, output_dir = temp_dirs
    non_existent_file = input_dir / "does_not_exist.zip"
    pattern = r".*"
    result = runner.invoke(app, [str(non_existent_file), pattern, str(output_dir)])

    assert result.exit_code != 0 # Expecting non-zero exit code for error
    # Check for key parts of the Typer error message for non-existent file
    assert "Invalid value for 'INPUT_FILE'" in result.output
    assert "does not exist" in result.output

# --- Tests for Nested Archives ---

def test_nested_zip_extraction(temp_dirs, nested_zip_archive):
    """Test extracting a file from a zip archive nested within another zip."""
    _, output_dir = temp_dirs
    pattern = r"nested_file\.log" # Match the file inside the inner zip
    result = runner.invoke(app, [str(nested_zip_archive), pattern, str(output_dir)])

    print(f"CLI Output:\n{result.output}")
    assert result.exit_code == 0
    assert "Found nested archive: inner_archive.zip" in result.output
    assert "Extracting matching file: nested_file.log" in result.output

    extracted_file = output_dir / "nested_file.log" # Should be extracted to the root of output
    assert extracted_file.exists()
    assert extracted_file.read_text() == "inner content"

    # Ensure the outer file (if not matching) is not extracted
    assert not (output_dir / "outer_file.txt").exists()
    # Ensure the inner archive itself is not extracted as a file
    assert not (output_dir / "inner_archive.zip").exists()


def test_nested_targz_extraction(temp_dirs, nested_targz_archive):
    """Test extracting a file from a zip archive nested within a tar.gz."""
    _, output_dir = temp_dirs
    pattern = r"deep_file\.data" # Match the file inside the inner zip
    result = runner.invoke(app, [str(nested_targz_archive), pattern, str(output_dir)])

    print(f"CLI Output:\n{result.output}")
    assert result.exit_code == 0
    assert "Found nested archive: archives/inner.zip" in result.output
    assert "Extracting matching file: deep_file.data" in result.output

    extracted_file = output_dir / "deep_file.data" # Should be extracted to the root of output
    assert extracted_file.exists()
    assert extracted_file.read_text() == "deep data"

    # Ensure the outer file (if not matching) is not extracted
    assert not (output_dir / "outer_config.cfg").exists()
    assert not (output_dir / "configs" / "outer_config.cfg").exists()
    # Ensure the inner archive itself is not extracted as a file
    assert not (output_dir / "inner.zip").exists()
    assert not (output_dir / "archives" / "inner.zip").exists()


def test_extract_all_with_nesting(temp_dirs, nested_targz_archive):
    """Test extracting all files matching a broad pattern from a nested structure."""
    _, output_dir = temp_dirs
    pattern = r"\.(data|cfg)$" # Match .data or .cfg files
    result = runner.invoke(app, [str(nested_targz_archive), pattern, str(output_dir)])

    print(f"CLI Output:\n{result.output}")
    assert result.exit_code == 0
    assert "Found nested archive: archives/inner.zip" in result.output
    assert "Extracting matching file: deep_file.data" in result.output
    assert "Extracting matching file: configs/outer_config.cfg" in result.output

    extracted_inner = output_dir / "deep_file.data"
    extracted_outer = output_dir / "outer_config.cfg" # Note: Extracted flat

    assert extracted_inner.exists()
    assert extracted_inner.read_text() == "deep data"
    assert extracted_outer.exists()
    assert extracted_outer.read_text() == "config settings"

# --- Tests for Edge Cases ---

def test_ignore_directories_in_zip(temp_dirs, zip_archive):
    """Test that directories inside zip files are ignored."""
    _, output_dir = temp_dirs
    # but the current zip_archive fixture already includes 'subdir/'.
    pattern = r"^subdir$" # Match only the exact name "subdir"
    result = runner.invoke(app, [str(zip_archive), pattern, str(output_dir)])

    print(f"CLI Output:\n{result.output}")
    assert result.exit_code == 0
    # Check that the directory itself was not created in the output
    # Since the pattern only matches the directory entry (which is skipped), no files should be extracted.
    assert not list(output_dir.iterdir()) # Output dir should be empty


def test_ignore_directories_in_targz(temp_dirs, targz_archive):
    """Test that directories inside tar.gz files are ignored."""
    _, output_dir = temp_dirs
    # The targz_archive fixture includes 'nested/'.
    pattern = r"^nested$" # Match only the exact name "nested"
    result = runner.invoke(app, [str(targz_archive), pattern, str(output_dir)])

    print(f"CLI Output:\n{result.output}")
    assert result.exit_code == 0
    # Check that the directory itself was not created in the output
    # Since the pattern only matches the directory entry (which is skipped), no files should be extracted.
    assert not list(output_dir.iterdir()) # Output dir should be empty


def test_unsupported_file_type(temp_dirs, unsupported_file):
    """Test providing an unsupported file type as input."""
    _, output_dir = temp_dirs
    pattern = r".*"
    result = runner.invoke(app, [str(unsupported_file), pattern, str(output_dir)])

    print(f"CLI Output:\n{result.output}")
    assert result.exit_code == 0 # Script should complete, just skip the file
    assert f"Skipping unsupported file type: {unsupported_file}" in result.output
    assert not list(output_dir.iterdir()) # No files should be extracted


def test_plain_gz_file_not_tar(temp_dirs, gz_archive):
    """Test handling of a .gz file that isn't a tar archive (already covered by test_extract_gz_match)."""
    # This scenario is effectively tested by test_extract_gz_match and test_extract_gz_no_match
    # The code correctly uses gzip.open for .gz files directly,
    # and the tarfile logic has a fallback for ReadError if opened as 'r:gz'.
    # Re-running test_extract_gz_match ensures the plain gz case works.
    test_extract_gz_match(temp_dirs, gz_archive)

# --- Final check ---
# Consider adding tests for corrupted archives if robustness is critical.
