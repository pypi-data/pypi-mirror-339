import pandas as pd
import os
import shutil
import requests
import zipfile
import tarfile
from urllib.parse import urlparse
# from pyspark.sql import types as T
from utilsme import timing

def df_print_shape(df: pd.DataFrame) -> None:
    """
    Prints the shape of a pandas DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame whose shape is to be printed.

    Returns:
        None
    """
    try:
        if df is pd.DataFrame:
            print(f"columns: {df.shape[1]}, rows: {df.shape[0]}")
    except Exception as e:
        print(f"Error while printing the shape -> {e}")

@timing
def read_file(path_file: str, *args, **kwargs) -> pd.DataFrame:
    """
    Reads a CSV or Excel file into a pandas DataFrame.

    Args:
        path_file (str): Path to the file to be read.
        *args: Additional positional arguments for pandas read functions.
        **kwargs: Additional keyword arguments for pandas read functions.

    Returns:
        pd.DataFrame: The DataFrame containing the file's data.
    """
    if not (path_file.endswith('csv') | path_file.endswith('xlsx')):
        print(f"Error: {path_file.split('.')[1]} file type is not yet taken into account. Only csv and xlsx are considered")
    
    else:
        try:
            if path_file.endswith('csv'):
                df = pd.read_csv(path_file, **kwargs)
            else:
                df = pd.read_excel(path_file, **kwargs)
                
            df_print_shape(df)
            return df
        except Exception as e:
            print(f"Error found when trying to read: {path_file}. {e}")
        
@timing
def write_file(df: pd.DataFrame, path_file: str, **kwargs) -> None:
    """
    Writes a pandas DataFrame to a CSV or Excel file.

    Args:
        df (pd.DataFrame): The DataFrame to be written.
        path_file (str): Path to the output file.
        **kwargs: Additional keyword arguments for pandas write functions.

    Returns:
        None
    """
    if not (path_file.endswith('csv') | path_file.endswith('xlsx')):
        print(f"Error: {path_file.split('.')[0]} file type is not yet taken into account. Only csv and xlsx are considered")
    
    else:
        try:
            
            # Get the directory from the given file path
            path = os.path.dirname(path_file)
            
            # Get file name form path
            file_name = os.path.basename(path_file)
            
            # If the directory doesn't exist, create it
            if not os.path.exists(path):
                os.makedirs(path)
            
            df_print_shape(df)
            if path_file.endswith('csv'):
                df.to_csv(path_file, **kwargs)
            else:
                df.to_excel(path_file, **kwargs)
        except Exception as e:
            print(f"Error found when trying to write: {file_name}. {e}")     

# @timing
def list_files(path: str, filter: str = '', in_subdirs: bool =False) -> dict:
    """
    Lists files in a directory, optionally filtering by a substring and including subdirectories.

    Args:
        path (str): Path to the directory.
        filter (str): Substring to filter file names.
        in_subdirs (bool): Whether to include files in subdirectories.

    Returns:
        dict: A dictionary with directory paths as keys and lists of file names as values.
    """
    result = {}
    try:
        if os.path.isdir(path):
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                if os.path.isfile(full_path):
                    if filter in item:
                        if path not in result.keys():
                            result[path] = []
                        result[path].append(item)
                else:
                    if in_subdirs:
                        result.update(list_files(full_path, filter, in_subdirs))
            return result
        else:
            raise(f"{path} is not a directory.")
    except Exception as e:
        print(e)

@timing
def delete_dir_file(path: str, with_content=False) -> None:
    """
    Deletes a directory or file. Optionally deletes directory contents.

    Args:
        path (str): Path to the directory or file.
        with_content (bool): Whether to delete directory contents.

    Returns:
        None
    """
    try:
        if os.path.isdir(path):
            nb_content = len([x for x in os.listdir(path)])
            if nb_content == 0:
                os.rmdir(path)
            elif (nb_content>0) and (with_content):
                shutil.rmtree(path)
                print(f"Path {path} has been correctly deleted with it content!")
            else:
                print(f"{path} contents {nb_content} elements. It cannot be deleted.")
        elif os.path.isfile(path):
            os.remove(path)
            print(f"File {path} has been correctly deleted!")
        else:
            print(f"{path} is neither dir nor file. It cannot be delete")
    except Exception as e:
        print(f"Error wile deleting {path}: {e}")        

@timing
def move(src: str, dest: str) -> str:
    """
    Moves a file or directory to a new location.

    Args:
        src (str): Source path.
        dest (str): Destination path.

    Returns:
        str: The destination path.
    """
    try:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        return shutil.move(src, dest)
    except Exception as e:
        print(f"Error while moving {src} to {dest}: {e}")
    
@timing
def copy_file(src_file: str, dest_path: str) -> str:
    """
    Copies a file to a specified destination.

    Args:
        src_file (str): Path to the source file.
        dest_path (str): Path to the destination directory or file.

    Returns:
        str: The destination file path.
    """
    return shutil.copy(src_file, dest_path)

@timing
def download_file(link: str, dest_path: str = "", display_stats: bool = False) -> str:
    """
    Downloads a file from a URL to a specified destination.

    Args:
        link (str): URL of the file to download.
        dest_path (str): Destination directory or file path.
        display_stats (bool): Whether to display download progress.

    Returns:
        str: The name of the downloaded file.
    """
    try:
        # check if the url works
        response = requests.get(link, stream=True)
        response.raise_for_status()
        
        # extract the file name from the url
        parsed_url = urlparse(link)
        filename = os.path.basename(parsed_url.path)
        
        # default file name
        if not filename:
            filename = 'downloaded_file'
        
        # get the file size
        if display_stats:
            file_size = int(response.headers.get("Content-Length", 0))
            print(f"Downloading {filename} ({file_size / (1024 * 1024):.2f} MB)")
        
        if dest_path:
            if not os.path.isdir(dest_path):
                if os.path.basename(dest_path):
                    filename = os.path.basename(dest_path)
                    dest_path = os.path.dirname(dest_path)
                    if not os.path.isdir(dest_path):
                        os.mkdir(dest_path)
                else:
                    os.mkdir(dest_path)
                
            dest_file_path = os.path.join(dest_path, filename)
        else:
            dest_file_path = filename
        
        downloaded_size = 0
        with open(dest_file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                if display_stats:
                    downloaded_size += len(chunk)
                    print(f"Downloaded {downloaded_size / (1024 * 1024):.2f} MB of {file_size / (1024 * 1024):.2f} MB", end="\r")
                
        return filename
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def decompressed(compressed_file: str, dest: str = "") -> list:
    """
    Decompresses a ZIP or TAR file to a specified destination.

    Args:
        compressed_file (str): Path to the compressed file.
        dest (str): Destination directory.

    Returns:
        list: List of extracted file names.
    """
    try:
        
        os.makedirs(dest, exist_ok=True)
        files_list = []
        if compressed_file.upper().endswith(".ZIP"):
            with zipfile.ZipFile(compressed_file, "r") as zip_content:
                zip_content.extractall(dest)
                files_list.extend(zip_content.namelist())
        
        elif(compressed_file.upper().endswith(".TAR") or compressed_file.upper().endswith(".TAR.GZ") or compressed_file.upper().endswith(".TAR.BZ2")):
            with tarfile.open(compressed_file, "r:*") as tar_content:
                tar_content.extractall(dest)
                files_list.extend(tar_content.getnames())
    
        else:
            print(f"Unsupported file format: {compressed_file}")
            
        return files_list
    except zipfile.BadZipFile:
        print("Error: the file is not a valid ZIP file")
    except Exception as e:
        print(f"An error occurred: ", e)
    
def compressed(src_path: str, dest_file: str, filter: str="") -> list:
    """
    Compresses files or directories into a ZIP or TAR archive.

    Args:
        src_path (str): Path to the source file or directory.
        dest_file (str): Path to the output compressed file.
        filter (str): Substring to filter files to be compressed.

    Returns:
        list: List of compressed file names.
    """
    compressed_file = []
    if not os.path.exists(src_path):
        print(f"Error: Source path {src_path} does not exist.")
        return compressed_file
    
    
    if dest_file.upper().endswith(".ZIP"):
        with zipfile.ZipFile(dest_file, "w", zipfile.ZIP_DEFLATED) as zip_content:
            if os.path.isdir(src_path):
                for root, dirs, files in os.walk(src_path):
                    for file in files:
                        if not filter in file:
                            continue
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, start=src_path)
                        zip_content.write(file_path, arcname=arc_name)
                        compressed_file.append(file)
            else:
                if filter in src_path:
                    zip_content.write(src_path, os.path.basename(src_path))
                    compressed_file.append(os.path.basename(src_path))
        return compressed_file
    elif (dest_file.upper().endswith(".TAR") or dest_file.upper().endswith(".TAR.GZ") or dest_file.upper().endswith(".TAR.BZ2")):
        mode = "w"
        if dest_file.upper().endswith(".TAR.GZ"):
            mode = "w:gz"
        elif dest_file.upper().endswith(".TAR.BZ2"):
            mode = "w:bz2"
        
        with tarfile.open(dest_file, mode) as tar_content:
            if os.path.isdir(src_path):
                for root, dirs, files in os.walk(src_path):
                    for file in files:
                        
                        if not filter in file:
                            continue
                        
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, start=src_path)
                        tar_content.add(file_path, arcname=arc_name)
                        compressed_file.append(file)
            else:
                if filter in src_path:
                    tar_content.add(src_path, arcname=os.path.basename(src_path))
                    compressed_file.append(src_path)
        return compressed_file            

@timing
def convert_data_types(df: pd.DataFrame, column_types: dict) -> pd.DataFrame:
    """
    Converts the data types of specified columns in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to modify.
        column_types (dict): Dictionary mapping column names to target data types.

    Returns:
        pd.DataFrame: The modified DataFrame.
    """
    conv_report = dict()
    for col in column_types.keys():
        try:
            if type(df) == pd.DataFrame:
                df[col]= df[col].astype(column_types[col])
            elif type(df) == None: #T.Dataframe:
                # need to implement for spark
                df[col]= df[col].astype(column_types[col])
            
        except Exception as e:
            print(f"Error while converting {col} to {column_types[col]}")
            conv_report[col] = f"Error while converting to {column_types[col]}: {e}"
    print(conv_report)
    return df


@timing
def validate_data_types(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    """
    Validates the data types of a DataFrame against a schema.

    Args:
        df (pd.DataFrame): The DataFrame to validate.
        schema (dict): Dictionary mapping column names to expected data types.

    Returns:
        pd.DataFrame: The original DataFrame.
    """
    conv_report = dict()
    for col, dtype in zip(df.columns, df.dtypes):
        if type(df) == pd.DataFrame:
            if dtype != schema[col]:
                conv_report[col] = f"{col}: Type in dataframe -> {dtype} and type in schema -> {schema[col]}"
        elif type(df) == None: #T.Dataframe:
            if dtype != schema[col]:
                conv_report[col] = f"{col}: Type in dataframe -> {dtype} and type in schema -> {schema[col]}"
    print(conv_report)
    return df

@timing
def remove_duplicates(df: pd.DataFrame, how: str = 'keep_first') -> pd.DataFrame:
    """
    Removes duplicate rows from a DataFrame based on specified criteria.

    Args:
        df (pd.DataFrame): The DataFrame to process.
        how (str): Strategy for handling duplicates ('keep_first', 'keep_last', or 'drop_all').

    Returns:
        pd.DataFrame: The DataFrame with duplicates removed.
    """
    rm_dup_report = dict()
    for col in df.columns:
        if df[col].duplicated:
            if how == 'keep_first':
                pass
            elif how == 'keep_last':
                pass
            else:
                df = df[~df[col].duplicated]
                rm_dup_report[col] = f"{sum(df[col].duplicated)} duplicates remove base on column {col}"
    print(rm_dup_report)
    return df
def handle_missing_values(df, strategy='drop'):
    pass


def normalize_data(df, columns):
    pass


def standardize_data(df, columns):
    pass


def setup_logger(log_file):
    pass


def log_message(message, level='info'):
    pass


def track_progress(task_name, total_steps):
    pass



def load_config(config_file):
    pass


def get_env_variable(key):
    pass

def set_env_variable(key, value):
    pass

def connect_to_db(connection_string):
    pass

def execute_query(connection, query):
    pass


def read_sql_to_df(connection, query):
    pass



def write_df_to_table(df, connection, table_name):
    pass


def assert_data_shape(df, expected_shape): #Asserts that a DataFrame has the expected shape.
    pass

def assert_data_types(df, schema): #Asserts that a DataFrame matches a given schema.
    pass

def assert_no_missing_values(df): #Asserts that a DataFrame has no missing values.
    pass