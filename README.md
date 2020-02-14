# py-multiband-tif-splitter
Script, with bundled executable, to split 5-band multi-spectral .TIF files from the Sentera 6X into individual single band .TIFs.

## Usage:
The splitting functionality in this repository can be used one of two ways:
* By running the "split_5_band.py" script locally
* By running the "Sentera Multiband Splitting Tool.exe" standalone executable

## Requriements:
* **Script**: Windows, OSX, or Linux system with Python 3 or higher
* **Executable**: Windows system (no Python necessary)

### Script Usage:
The "split_5_band.py" script can be called from the command line by navigating to its file location and running

    python split_5_band.py --input_folder [--options]
  
These options are as follows:

   Command Flag                    |               Usage                     
:-------------------------------:  | :---------------------------------------: 
 **--input_folder**  FOLDER_PATH   | Path to folder of 5-band .tif files to be split into individual bands. 
                                                      **Required** argument. 
**--output_folder**  FOLDER_PATH   | Path to folder where the individual band images will be stored.<br> 
                                     Each band will be stored in its own subfolder within the<br> 
                                     specified folder. Default location is the specified input folder.      
**--delete_originals**             | Deletes original 5-band images after splitting them.<br> 
                                       Useful to avoid bloating one's hard drive."

#### Examples:

Split files located in current folder:

    python split_5_band.py --input_folder .
  
Split files in separate folder, deleting original multiband files:

    python split_5_band.py --input_folder "path/to/folder" --delete_originals
  
Split files in separate folder, and save output files in different folder:

    python split_5_band.py --input_folder "path/to/multiband/folder" --output_folder "path/to/output/folder"
  
  
### Executable Usage:
Simply double click the executable to run the application. This will open a window that exposes the same options as those allowed within the script.
