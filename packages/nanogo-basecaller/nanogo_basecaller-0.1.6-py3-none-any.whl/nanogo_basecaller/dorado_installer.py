#!/usr/bin/env python3
"""
Dorado Installer for NanoGO Basecaller

This script handles downloading and installing the latest version of Oxford Nanopore's
Dorado basecaller tool. It can be run as a standalone script after package installation.
"""

import os
import sys
import hashlib
import tarfile
import urllib.request
import shutil
import tempfile
import re
import subprocess
import platform
import argparse


# Fallback version info if we can't fetch the latest
FALLBACK_DORADO_URL = (
    "https://cdn.oxfordnanoportal.com/software/analysis/dorado-0.9.5-linux-x64.tar.gz"
)
FALLBACK_DORADO_SHA256 = (
    "b257321bc55ea5a3b6edb11bd1a3c78c1baa58cd022b6702925af970ac19ccd9"
)


def get_install_dirs(user_install=False):
    """
    Determine the appropriate directories for installing Dorado.
    Returns a tuple of (bin_dir, lib_dir, can_write)
    """
    # Try to determine if this is a user install or not
    venv_path = os.environ.get("VIRTUAL_ENV")

    # If in a virtual environment, install there
    if venv_path:
        bin_dir = os.path.join(venv_path, "bin")
        lib_dir = os.path.join(venv_path, "lib")
        print(f"Installing Dorado to virtual environment: {venv_path}")
        return bin_dir, lib_dir, True

    # If user install, use user's local bin directory
    if user_install:
        import site

        user_base = site.USER_BASE
        bin_dir = os.path.join(user_base, "bin")
        lib_dir = os.path.join(user_base, "lib")
        # Create the directories if they don't exist
        os.makedirs(bin_dir, exist_ok=True)
        os.makedirs(lib_dir, exist_ok=True)
        print(f"Installing Dorado to user directories: {bin_dir} and {lib_dir}")
        return bin_dir, lib_dir, True

    # For system installs, check if we have write permission to sys.prefix
    bin_dir = os.path.join(sys.prefix, "bin")
    lib_dir = os.path.join(sys.prefix, "lib")

    # Check if we have write permission
    can_write = os.access(os.path.dirname(bin_dir), os.W_OK) and os.access(
        os.path.dirname(lib_dir), os.W_OK
    )

    if not can_write:
        print(f"Warning: No write permission to {bin_dir} and {lib_dir}.")
        print("Consider using --user flag or a virtual environment.")

    return bin_dir, lib_dir, can_write


def get_latest_dorado_version():
    """
    Check ONT's CDN for the latest version of Dorado.
    Returns a tuple of (version, url, sha256) or None if unable to determine.
    """
    try:
        print("Checking for the latest version of Dorado...")
        index_url = "https://cdn.oxfordnanoportal.com/software/analysis/"

        with urllib.request.urlopen(index_url, timeout=10) as response:
            html = response.read().decode("utf-8")

            # Look for dorado release tarballs in the HTML
            pattern = r'href="(dorado-(\d+\.\d+\.\d+)-linux-x64\.tar\.gz)"'
            matches = re.findall(pattern, html)

            if not matches:
                print("No Dorado releases found, falling back to default version.")
                return None

            # Sort by version number to find the latest
            latest = sorted(
                matches, key=lambda x: [int(n) for n in x[1].split(".")], reverse=True
            )[0]
            latest_filename = latest[0]
            latest_version = latest[1]

            # Construct the full URL
            latest_url = f"{index_url}{latest_filename}"
            print(f"Found latest Dorado version: {latest_version} at {latest_url}")

            # Now we need to get the SHA256 hash
            try:
                hash_url = f"{latest_url}.sha256"
                with urllib.request.urlopen(hash_url, timeout=10) as hash_response:
                    sha256 = hash_response.read().decode("utf-8").strip().split()[0]
                    return (latest_version, latest_url, sha256)
            except urllib.error.URLError:
                print(
                    f"SHA256 file not found for {latest_filename}. Will verify after download."
                )
                return (latest_version, latest_url, None)

    except Exception as e:
        print(f"Error checking for latest Dorado version: {e}")
        print("Falling back to default version.")
        return None


def is_dorado_installed(bin_dir):
    """
    Check if Dorado is already installed and working.

    Args:
        bin_dir: Directory where the dorado executable should be located

    Returns:
        Boolean indicating if Dorado is properly installed and working
    """
    dorado_bin = os.path.join(bin_dir, "dorado")

    # Check if the executable exists
    if not os.path.exists(dorado_bin):
        print(f"Dorado executable not found at {dorado_bin}")
        return False

    # Check if it's executable
    if not os.access(dorado_bin, os.X_OK):
        print(f"Dorado exists but is not executable at {dorado_bin}")
        return False

    # Try to run a basic command to verify it works
    try:
        result = subprocess.run(
            [dorado_bin, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            text=True,
        )
        if result.returncode == 0:
            version = result.stdout.strip() or result.stderr.strip()
            print(f"Dorado is already installed: {version}")
            return True
        else:
            print(f"Dorado found but failed to run: {result.stderr.strip()}")
            return False
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        print(f"Error verifying Dorado: {e}")
        return False


def calculate_sha256(file_path):
    """Calculate SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def install_dorado(user_install=False, force=False):
    """
    Install Dorado if not already installed, trying to use the latest version.

    Args:
        user_install: Whether to install to user directories
        force: Whether to force installation even if Dorado is already installed

    Returns:
        True if installation was successful or Dorado was already installed.
    """
    # Check if platform is supported
    if platform.system() != "Linux":
        print(
            f"Dorado auto-installation is only supported on Linux, not {platform.system()}."
        )
        print("Please manually install Dorado for your platform.")
        return False

    # Determine installation directories
    bin_dir, lib_dir, can_write = get_install_dirs(user_install)

    # Check if already installed
    if is_dorado_installed(bin_dir) and not force:
        print("Dorado is already installed and working. Skipping installation.")
        print("Use --force to reinstall.")
        return True

    # If we can't write to the target directories, we can't install
    if not can_write:
        print("Cannot install Dorado due to permission issues.")
        print("Please install Dorado manually or reinstall with --user flag.")
        return False

    # Try to get latest version info
    latest_info = get_latest_dorado_version()

    try:
        if latest_info:
            version, url, sha256 = latest_info
            print(f"Using Dorado version: {version}")
            expected_dir_name = f"dorado-{version}-linux-x64"
        else:
            # Fall back to the hardcoded version
            version = "0.9.5"  # Extracted from the URL
            url = FALLBACK_DORADO_URL
            sha256 = FALLBACK_DORADO_SHA256
            expected_dir_name = "dorado-0.9.5-linux-x64"
            print(f"Using fallback Dorado version: {version}")

        # Create a temporary directory for download and extraction
        tmp_dir = tempfile.mkdtemp()
        tarball_path = os.path.join(tmp_dir, "dorado.tar.gz")

        try:
            # Download Dorado
            print(f"Downloading Dorado {version} from {url}...")
            urllib.request.urlretrieve(url, tarball_path)

            # Verify download
            print("Verifying download...")
            if sha256:
                # Verify against provided hash
                calculated_hash = calculate_sha256(tarball_path)
                if calculated_hash != sha256:
                    print(f"SHA256 hash verification failed for Dorado download.")
                    print(f"Expected: {sha256}")
                    print(f"Got: {calculated_hash}")
                    return False
                print("✓ SHA256 verified.")
            else:
                # If we don't have a hash to verify against, just log the hash we calculated
                calculated_hash = calculate_sha256(tarball_path)
                print(f"Downloaded file SHA256: {calculated_hash}")

            # Extract the archive
            print("Extracting Dorado...")
            with tarfile.open(tarball_path, "r:gz") as tar:
                tar.extractall(path=tmp_dir)

            # Find the extracted directory
            extracted_dirs = [
                d
                for d in os.listdir(tmp_dir)
                if os.path.isdir(os.path.join(tmp_dir, d)) and d.startswith("dorado-")
            ]

            if not extracted_dirs:
                print(
                    f"Could not find Dorado directory in extracted contents: {os.listdir(tmp_dir)}"
                )
                return False

            # Use the first directory that matches the pattern
            extracted_dir = os.path.join(tmp_dir, extracted_dirs[0])

            extracted_bin = os.path.join(extracted_dir, "bin")
            extracted_lib = os.path.join(extracted_dir, "lib")

            # Make sure target directories exist
            os.makedirs(bin_dir, exist_ok=True)
            os.makedirs(lib_dir, exist_ok=True)

            # Move all files from the extracted bin folder
            print(f"Moving files from {extracted_bin} to {bin_dir}...")
            for filename in os.listdir(extracted_bin):
                src = os.path.join(extracted_bin, filename)
                dst = os.path.join(bin_dir, filename)
                if os.path.exists(dst):
                    if os.path.isdir(dst):
                        shutil.rmtree(dst)
                    else:
                        os.remove(dst)
                shutil.copy2(src, dst)  # Use copy2 to preserve permissions
                os.chmod(dst, 0o755)  # Make executable

            # Move all files from the extracted lib folder
            print(f"Moving files from {extracted_lib} to {lib_dir}...")
            for filename in os.listdir(extracted_lib):
                src = os.path.join(extracted_lib, filename)
                dst = os.path.join(lib_dir, filename)
                if os.path.exists(dst):
                    if os.path.isdir(dst):
                        shutil.rmtree(dst)
                    else:
                        os.remove(dst)
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)  # Use copy2 to preserve permissions

            # Verify the installation
            if is_dorado_installed(bin_dir):
                print(f"✓ Dorado {version} installed successfully.")
                return True
            else:
                print("Dorado was installed but verification failed.")
                return False

        finally:
            # Cleanup the temporary directory
            shutil.rmtree(tmp_dir)

    except Exception as e:
        print(f"Error installing Dorado: {e}")
        return False


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Install Dorado for NanoGO Basecaller")
    parser.add_argument(
        "--user",
        action="store_true",
        help="Install to user directories instead of system directories",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force installation even if Dorado is already installed",
    )
    args = parser.parse_args()

    print("\n=== Dorado Installer for NanoGO Basecaller ===\n")
    success = install_dorado(user_install=args.user, force=args.force)

    if success:
        print("\nDorado installation completed successfully.")
        print("You can now use nanogo-basecaller with Dorado support.")
    else:
        print("\nDorado installation failed.")
        print("You may need to install Dorado manually.")
        print("See https://github.com/nanoporetech/dorado for instructions.")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
