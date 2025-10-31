# bin file FiJi/imageJ plugin

This implements a JAVA plugin to parse images from bin files. It is **much** faster than the python version.

## Installation

The code is tested on FiJi version 1.54.

1. Install [FiJi](https://fiji.sc/) being sure to get the full version with the java SDK.
2. Copy the Subsample_Stack.java file to the fiji plugins directory, e.g. Fiji.app/plugins/LocalPlugins/Subsample_Stack.java.
3. Open it in the script editor (File/New/Script, then File/Open) and compile/run.

As in the python version, four stacks will be created with red, two greens, and blue. Note that the size is 1/4 of what it was since the color channels are only available on the 1/4 of the pixels. No data are extrapolated.
