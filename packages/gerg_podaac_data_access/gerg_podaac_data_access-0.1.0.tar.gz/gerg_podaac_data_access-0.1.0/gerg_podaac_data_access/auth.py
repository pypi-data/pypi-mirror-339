def get_earthdata_auth_when_needed():
    """
    Check if Earthdata authentication is needed and set it up if necessary.
    This function should be imported from setup_auth.py
    """
    from gerg_podaac_data_access.setup_auth import get_earthdata_auth_when_needed
    return get_earthdata_auth_when_needed()

def setup_earthdata_auth(force_setup=False):
    """
    Set up Earthdata authentication credentials.
    This function should be imported from setup_auth.py
    """
    from gerg_podaac_data_access.setup_auth import setup_earthdata_auth
    return setup_earthdata_auth(force_setup=force_setup)

def cleanup_earthdata_auth():
    """
    Clean up Earthdata authentication credentials.
    This function should be imported from setup_auth.py
    """
    from gerg_podaac_data_access.setup_auth import cleanup_earthdata_auth
    return cleanup_earthdata_auth()