class Dataset:
    '''
    podaac_download_name (str): Name of the dataset on podaac, found by clicking "Data Access" on the selected dataset then clicking download,
    then look for "Download by Spatial and Temporal Search" under "PO.DAAC Data Subscriber" under "Tools.
    You should see something like this: podaac-data-downloader -c ECCO_L4_SSH_05DEG_DAILY_V4R4 -d ./data --start-date 1992-01-01T00:00:00Z --end-date 1992-01-08T00:00:00Z -b="-180,-90,180,90"
    Where "ECCO_L4_SSH_05DEG_DAILY_V4R4" is the podaac_download_name.
    
    link_to_metadata (str): Link to the dataset on podaac, for future reference.
    '''
    podaac_download_name: str
    link_to_metadata: str|None
    
    def __init__(self, podaac_download_name: str, link_to_metadata: str|None=None):
        self.podaac_download_name = podaac_download_name
        self.link_to_metadata = link_to_metadata
        
    def __str__(self):
        return f"podacc_download_name: {self.podaac_download_name}"
    
    def __repr__(self):
        return f"podacc_download_name: {self.podaac_download_name}"

# Define common datasets
def get_common_datasets():
    return {
        "NeurOST": Dataset(
            podaac_download_name="ECCO_L4_SSH_05DEG_DAILY_V4R4",
            link_to_metadata="https://podaac.jpl.nasa.gov/dataset/ECCO_L4_SSH_05DEG_DAILY_V4R4#"
        ),
        "NASA_SSH": Dataset(
            podaac_download_name="NASA_SSH_REF_SIMPLE_GRID_V1",
            link_to_metadata="https://podaac.jpl.nasa.gov/dataset/NASA_SSH_REF_SIMPLE_GRID_V1#"
        ),
        "MEaSUREs": Dataset(
            podaac_download_name="SEA_SURFACE_HEIGHT_ALT_GRIDS_L4_2SATS_5DAY_6THDEG_V_JPL2205",
            link_to_metadata="https://podaac.jpl.nasa.gov/dataset/SEA_SURFACE_HEIGHT_ALT_GRIDS_L4_2SATS_5DAY_6THDEG_V_JPL2205#"
        ),
        "ECCO_SSH": Dataset(
            podaac_download_name="ECCO_L4_SSH_05DEG_DAILY_V4R4",
            link_to_metadata="https://podaac.jpl.nasa.gov/dataset/ECCO_L4_SSH_05DEG_DAILY_V4R4#"
        )
    }