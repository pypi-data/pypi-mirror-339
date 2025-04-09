from glob import glob as globber
import os

# function to find files in directory with a specified variable


def create_ensemble(path="", recursive=True):
    """
    create_ensemble: Generate an ensemble of files from a directory.

    Parameters
    -------------
    path: str
        The directory to search for netCDF files
    recursive : boolean
        True/False depending on whether you want to search the path recursively.
        Defaults to True.

    Returns
    -------------

    files : list of files

    Examples
    ------------

    If you wanted to recursively find all netCDF files available in a directory "data", you would do this:

    >>> import nctoolkit as nc
    >>> nc.create_ensemble("data")

    If you wanted to find the files in that directory and ignore subdirectories, you would instead do this:

    >>> nc.create_ensemble("data", recursive = False)


    """

    # make sure the path exists

    if os.path.exists(path) is False:
        raise ValueError("The path provided does not exist!")

    # make sure the path ends with "/" if it is not empty
    if path != "":
        if path.endswith("/") is False:
            path = path + "/"

    if recursive:
        files = [f for f in globber(path + "/**/*.nc*", recursive=True)]
    else:
        files = [f for f in globber(path + "*.nc*")]

    if len(files) == 0:
        raise ValueError("There is no data in the target directory")

    return files

def glob(path="", recursive=True):
    """
    create_ensemble: Generate an ensemble of files from a directory.

    Parameters
    -------------
    path: str
        The directory to search for netCDF files
    recursive : boolean
        True/False depending on whether you want to search the path recursively.
        Defaults to True.

    Returns
    -------------

    files : list of files

    Examples
    ------------

    If you wanted to recursively find all netCDF files available in a directory "data", you would do this:

    >>> import nctoolkit as nc
    >>> nc.create_ensemble("data")

    If you wanted to find the files in that directory and ignore subdirectories, you would instead do this:

    >>> nc.create_ensemble("data", recursive = False)


    """

    # make sure the path exists

    try:
        files = globber(path, recursive = recursive)
        if [x for x in files if x.endswith(".nc")]:
            return files
        else:
            raise ValueError("There are no netCDF files in the target directory")
    except:

        if os.path.exists(path) is False:
            raise ValueError("The path provided does not exist!")

        # make sure the path ends with "/" if it is not empty
        if path != "":
            if path.endswith("/") is False:
                path = path + "/"

        if recursive:
            files = [f for f in globber(path + "/**/*.nc*", recursive=True)]
        else:
            files = [f for f in globber(path + "*.nc*")]

        if len(files) == 0:
            raise ValueError("There is no data in the target directory")

        return files
