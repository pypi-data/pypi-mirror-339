# ITCPR Tools Library

This Python library provides utilities for your internship at ITCPR, including features for plotting data, generating mumax3 commands based on file naming patterns, and renaming files for organizational purposes.

## Installation

To install the GRE Tool Library, run the following command:

```pip install itcpr```


## Features

- **Listing Available Parameters**: Find the parameters from data files for plotting.
- **Data Plotting**: Easily plot specific parameters from data files for analysis.
- **MuMaX3 Command Generation**: Automate the generation of mumax3 commands for simulations.
- **File Renaming**: Streamline your file organization by renaming `table.txt` files according to their parent directory names.

## Usage

#### Listing Available Parameters for Plotting `plot_list(file_path)`

Lists the parameters available for plotting from a given file, excluding the independent variable.

Args:

- file_path: Path to the data file.

This function helps you identify which parameters can be plotted from your data file, aiding in the visualization process of your GRE preparation data:

```python
import spintronics as spin

file_path = "path/to/your/data/filename.txt" # make sure to use / instead of \ in the path
spin.plot_list(file_path)
```

#### Plotting Data `plot(file_path, parameter_names)`

Plots specified parameters from a given file.

Args:
- `file_path`: Path to the data file.
- `parameter_names`: List of parameter names to plot.

Plot specified parameters from a data file to visualize your GRE preparation data:

```python
import spintronics as spin

file_path = "path/to/your/data/filename.txt" # make sure to use / instead of \ in the path
parameter_names = ["Parameter1", "Parameter2"] #use one or more parameters
spin.plot(file_path, parameter_names)
```

Look into your `table.txt` file to know what parameters you have there. For example:
- `mx ()`
- `my ()`
- `mz ()`
- and more...

#### Generating mumax3 Commands `m3_commands(base_folder, filename_pattern, ranges)`

Prints mumax3 commands for files based on a pattern with multiple 'cng' placeholders, each having different start, end values, and increments, and then prints 'mumax3' at the end.

Args:
- base_folder: The base folder address where the files are located or will be saved.
- filename_pattern: The pattern of the filename with 'cng' as placeholders.
- ranges: A list of tuples, each tuple contains (start_value, end_value, increment) for each 'cng'.

Generate mumax3 commands for a series of files, facilitating batch run of simulations:

```python
import spintronics as spin

base_folder = "path/to/base/folder" # make sure to use / instead of \ in the path
filename_pattern = "N_2_2_2_C_1_1_1_A_cng_f_cng.m3"
ranges = [(10, 15, 1), (18.5, 21.2, 0.1)]  # Example for two placeholders with their ranges
spin.m3_commands(base_folder, filename_pattern, ranges)
```

#### Renaming Table Files `rename_tables(base_dir)`

Renames all 'table.txt' files to match their parent folder names (without the '.out' extension) with '.txt' extension, within folders ending with '.out' found anywhere under the specified base directory.
    
Args:
- base_dir: The base directory to recursively search for '.out' folders.

Automatically rename table.txt files within .out folders to match their parent folder's name, improving file organization:

```python
import spintronics as spin

base_dir = "path/to/your/base/directory" # make sure to use / instead of \ in the path
spin.rename_tables(base_dir)
```

## Contribute
If you have discovered a bug or something else you want to change, feel free to contact the author at `abdussamiakanda@gmail.com`.

## License
&copy; 2024 Md. Abdus Sami Akanda

This repository is licensed under the MIT license. See LICENSE for details.