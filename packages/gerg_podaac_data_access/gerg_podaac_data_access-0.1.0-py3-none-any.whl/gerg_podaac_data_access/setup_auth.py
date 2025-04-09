import os
import getpass
import platform
import re
from pathlib import Path

def get_netrc_path():
    """Return the path to the .netrc file."""
    return Path.home() / ".netrc"

def check_earthdata_auth():
    """
    Check if Earthdata Login authentication is already set up.
    
    Returns:
        bool: True if authentication is already set up, False otherwise
    """
    netrc_path = get_netrc_path()
    
    if netrc_path.exists():
        try:
            with open(netrc_path, 'r') as f:
                content = f.read()
                # Check for both machine name and that it has login and password
                return (
                    "machine urs.earthdata.nasa.gov" in content and
                    re.search(r"machine urs\.earthdata\.nasa\.gov.*?login\s+\S+\s+password\s+\S+", content) is not None
                )
        except Exception:
            pass
    return False

def setup_earthdata_auth(force_setup=False):
    """
    Interactive setup for Earthdata Login authentication.
    Creates a .netrc file with the user's credentials.
    
    Args:
        force_setup (bool): If True, prompt for credentials even if auth seems valid
        
    Returns:
        bool: True if authentication is set up successfully, False otherwise
    """
    is_windows = platform.system().lower() == 'windows'
    netrc_path = get_netrc_path()
    
    # Check if authentication is already set up
    if not force_setup and check_earthdata_auth():
        print(f"Earthdata Login credentials found in {netrc_path}")
        return True
    
    print("Setting up Earthdata Login authentication...")
    print("You need an Earthdata Login account to download data from PO.DAAC.")
    print("If you don't have one, please register at: https://urs.earthdata.nasa.gov/")
    
    # Get user credentials
    username = input("Enter your Earthdata Login username: ")
    password = getpass.getpass("Enter your Earthdata Login password: ")
    
    # Create or update the netrc file
    try:
        existing_content = ""
        if netrc_path.exists():
            with open(netrc_path, 'r') as f:
                existing_content = f.read()
        
        # Prepare the new entry
        earthdata_entry = f"machine urs.earthdata.nasa.gov login {username} password {password}"
        
        # Replace existing entry or add new one
        if "machine urs.earthdata.nasa.gov" in existing_content:
            # Replace existing entry using regex
            pattern = r"machine urs\.earthdata\.nasa\.gov.*?(?=machine|\Z)"
            new_content = re.sub(pattern, earthdata_entry + "\n", existing_content, flags=re.DOTALL)
        else:
            # Add new entry
            new_content = existing_content
            if new_content and not new_content.endswith('\n'):
                new_content += '\n'
            new_content += earthdata_entry + '\n'
        
        # Write to file
        with open(netrc_path, 'w') as f:
            f.write(new_content)
        
        # Set appropriate permissions on Unix systems
        if not is_windows:
            os.chmod(netrc_path, 0o600)
        
        print(f"Authentication credentials saved to {netrc_path}")
        print("You can now download data from PO.DAAC.")
        
        return True
        
    except Exception as e:
        print(f"Error setting up authentication: {str(e)}")
        return False

def get_earthdata_auth_when_needed():
    """
    Ensures Earthdata Login authentication is set up only when needed.
    Call this function before operations that require authentication.
    
    Returns:
        bool: True if authentication is set up successfully, False otherwise
    """
    if not check_earthdata_auth():
        print("Earthdata Login credentials required for this operation.")
        return setup_earthdata_auth()
    return True

def cleanup_earthdata_auth():
    """
    Removes Earthdata Login credentials from the .netrc file.
    This preserves other credentials in the file.
    
    Returns:
        bool: True if cleanup was successful, False otherwise
    """
    netrc_path = get_netrc_path()
    
    if not netrc_path.exists():
        print(f"No .netrc file found. Nothing to clean up.")
        return False
    
    try:
        # Read the current content
        with open(netrc_path, 'r') as f:
            content = f.read()
        
        if "machine urs.earthdata.nasa.gov" not in content:
            print("No Earthdata Login credentials found in .netrc file.")
            return False
        
        # Remove the entire Earthdata entry using regex
        pattern = r"machine urs\.earthdata\.nasa\.gov.*?(?=machine|\Z)"
        new_content = re.sub(pattern, "", content, flags=re.DOTALL)
        
        # Clean up any double newlines that might have been created
        new_content = re.sub(r"\n\s*\n", "\n", new_content)
        
        # If the file is now empty or just whitespace, delete it
        if not new_content.strip():
            os.remove(netrc_path)
            print(f".netrc file was empty after removing Earthdata credentials, so it was deleted.")
        else:
            # Write the modified content back
            with open(netrc_path, 'w') as f:
                f.write(new_content)
            
            # Set appropriate permissions on Unix systems
            is_windows = platform.system().lower() == 'windows'
            if not is_windows:
                os.chmod(netrc_path, 0o600)
            
            print(f"Earthdata credentials removed from {netrc_path}, other credentials preserved.")
        
        print("Note: You will need to set up authentication again when you next need to download data.")
        return True
        
    except Exception as e:
        print(f"Error cleaning up authentication file: {str(e)}")
        return False


if __name__ == "__main__":
    # This will only run setup if credentials don't exist
    get_earthdata_auth_when_needed()
