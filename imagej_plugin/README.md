# bin file FiJi/imageJ plugin

This implements a Jython plugin to parse images from bin files.

## Installation

The code is tested on FiJi version 1.54.

1. Install [FiJi](https://fiji.sc/)
2. The plugin should be standalone and [accessible as any other script](https://imagej.net/scripting/).

**-Tip** You can install the plugin to be accessible from the plugin menu or just load it into the script editor (File/New/Script).

## Usage

The generic goal is to read in a .bin file and separate out color channels. These steps are in FiJi.

1. Select a .bin file using the File/Import/Raw menu command.
2. Set the parameters as follows
    1. Image type: 16-bit unsigned
	2. Width: 1504 pixels (assuming X2, 3008 for X1)
	3. Height: 1504 pixels (assuming X2, 3008 for X1)
	4. Offset to first image: 108
	5. Number of images: 1000 (it will stop automaticallly when the file runs out)
	6. Gap between images: 44
	7. Only check *Little-endian byte order*
3. Click OK
4. Open the plugin in the script editor (File/New/Script then File/Open)
5. Click on *Run* in the top right.

Four stacks will be created with red, two greens, and blue. Note that the size is 1/4 of what it was since the color channels are only available on the 1/4 of the pixels. No data are extrapolated.
