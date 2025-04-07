# scene-rir
##  Room Impulse Response package for the SCENE project.
Copyright (C) 2025 Christos Sevastiadis

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

## Installation

Use `pip` to install **scene-rir**

```
pip install scene-rir
```
(Requires Python>=3.8)


## Installation verification
To check if the package was installed successfully, try:
```
python -c "import scene_rir.rir; help(scene_rir.rir)
```
If the **scene-rir** is installed, this command will print all of its help documentation string.

## Examples of usage

Examples of usage can be found in the `examples` and `tests` directories of the repository tree. There are Python scripts in `.py` files, and Jupyter notebooks in `.ipynb` files. To execute the test `.ipynb` notebooks, the directory `input` with its content should be downloaded, either. To execute the examples and the tests, some extra packages should be installed, for example, the `matplotlib` package.

### Usage from the Comman Line 

#### Open a Terminal or Command Prompt
- **Windows**: Press `Win + R`, type `cmd`, and hit `Enter`.
- **Mac/Linux**: Open the terminal from your applications menu o use `Ctrl + Alt + T`.

#### Use the following command to get help for the Command Line usage
```
python -m scene_rir.rir --help
```
