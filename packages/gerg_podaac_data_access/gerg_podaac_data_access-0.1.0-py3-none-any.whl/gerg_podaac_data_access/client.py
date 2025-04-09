import datetime
import pandas as pd
import subprocess
from pathlib import Path
import xarray as xr

from gerg_podaac_data_access.models import Dataset
from gerg_podaac_data_access.auth import get_earthdata_auth_when_needed, setup_earthdata_auth

class PodaacClient:
    dataset: Dataset
    # Bounds
    date_start: str|datetime.datetime
    date_end: str|datetime.datetime
    lat_min: int|float
    lat_max: int|float
    lon_min: int|float
    lon_max: int|float
    
    data_out_folder: Path

    def __init__(self, data_out_folder: Path,
                 date_start: str, date_end: str, 
                 lat_min: float, lat_max: float, 
                 lon_min: float, lon_max: float):
        self.data_out_folder = data_out_folder
        
        self.date_start = self.parse_datetime(date_start)
        self.date_end = self.parse_datetime(date_end)
        
        self.lat_min = lat_min
        self.lat_max = lat_max
        self.lon_min = lon_min
        self.lon_max = lon_max

    def parse_datetime(self, date: str|datetime.datetime) -> datetime.datetime:
        '''Converting formatting from user input like: 01-01-2013T00:00:00Z
        
        To the required format like: 2021-01-14T00:00:00Z'''
        date = pd.to_datetime(date)
        date = date.isoformat()
        if "+00:00" in date:
            date = date.replace("+00:00", "Z")
        else:
            raise ValueError(f"Dates must be in UTC, you passed {date}")
        return date
    
    def create_podaac_download_command(self, dataset: Dataset):
        # Create a subfolder with the dataset's podaac_download_name
        dataset_folder = self.data_out_folder / dataset.podaac_download_name
        # Ensure the folder exists
        dataset_folder.mkdir(exist_ok=True, parents=True)
        
        bounds_format = f"{self.lon_min},{self.lat_min},{self.lon_max},{self.lat_max}"
        command = f'''podaac-data-downloader -c {dataset.podaac_download_name} -d {dataset_folder.resolve()} --start-date {self.date_start} --end-date {self.date_end} -b="{bounds_format}"'''
        print(f"Running: {command}")
        return command

    def download_data(self, dataset: Dataset):
        '''
        Data from:
        Daily NeurOST L4 Sea Surface Height and Surface Geostrophic Currents
        Example command:
        podaac-data-downloader -c NEUROST_SSH-SST_L4_V2024.0 -d ./data --start-date 2010-01-01T00:00:00Z --end-date 2010-01-08T00:00:00Z -b="-180,-70,180,79.9"
        '''
        
        # First, ensure authentication is set up only when needed
        get_earthdata_auth_when_needed()
        
        command = self.create_podaac_download_command(dataset=dataset)
        
        try:
            # Run the command directly to see output in real-time
            process = subprocess.Popen(
                command, 
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Print output in real-time
            stdout_data = []
            stderr_data = []
            
            for line in process.stdout:
                print(line, end='')
                stdout_data.append(line)
                
            for line in process.stderr:
                print(f"ERROR: {line}", end='')
                stderr_data.append(line)
                
            # Wait for the process to complete
            return_code = process.wait()
            
            if return_code != 0:
                print(f"Command failed with return code: {return_code}")
                stderr_text = ''.join(stderr_data)
                
                # Check if it's an authentication error
                if "UnboundLocalError: cannot access local variable 'username'" in stderr_text or "There's no .netrc file" in stderr_text:
                    print("Authentication error detected. Let's set up your Earthdata Login credentials.")
                    if setup_earthdata_auth(force_setup=True):
                        print("Authentication set up successfully. Retrying download...")
                        subprocess.run(command, shell=True)
        
        except Exception as e:
            print(f"Error during download: {str(e)}")
            
    def open_dataset(self, dataset: Dataset):
        """
        Open the downloaded dataset files
        """
        # Implementation needed
        # dataset_files = dataset.podaac_download_name
        # ds = xr.open_mfdataset()
        pass