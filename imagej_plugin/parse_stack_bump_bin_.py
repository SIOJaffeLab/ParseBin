#Joe Snider
#8/23
#
#Jython script for FiJi to create red/green/blue images
#  from a Bayer pattern.
#Operates on a stack and generates 4 subsequent stacks,
#  each at a quarter size.

from __future__ import with_statement, division
from ij import IJ, WindowManager, ImagePlus, ImageStack
from ij.gui import GenericDialog
from ij.process import ImageProcessor, ShortProcessor

def run_script():
	imp = IJ.getImage()
	
	if imp.getNSlices() == 1:
		IJ.showMessage("Requires a stack from raw bump output ... stopping.")
		raise RuntimeException("Not a stack")
	
	stack = imp.getStack()
	
	width = imp.width
	height = imp.height
	red_stack = ImageStack(int(width/2), int(height/2))
	green1_stack = ImageStack(int(width/2), int(height/2))
	green2_stack = ImageStack(int(width/2), int(height/2))	
	blue_stack = ImageStack(int(width/2), int(height/2))
	
	for s in range(1, imp.getNSlices()+1):
		slice = stack.getProcessor(s)
		
		image_red = ImagePlus("red", ShortProcessor(int(width/2), int(height/2)))
		image_green1 = ImagePlus("green1", ShortProcessor(int(width/2), int(height/2)))
		image_green2 = ImagePlus("green2", ShortProcessor(int(width/2), int(height/2)))
		image_blue = ImagePlus("blue", ShortProcessor(int(width/2), int(height/2)))
	
		image_red_ip = image_red.getProcessor()
		image_green1_ip = image_green1.getProcessor()
		image_green2_ip = image_green2.getProcessor()
		image_blue_ip = image_blue.getProcessor()
		
		print("starting calculation")
		for i in range(width):
			for j in range(height):
				if i%2 == 0 and j%2 == 0:
					image_red_ip.putPixel(int(i/2), int(j/2), slice.getPixel(i,j))
				elif i%2 == 0 and j%2 == 1:
					image_green1_ip.putPixel(int(i/2), int(j/2), slice.getPixel(i,j))
				elif i%2 == 1 and j%2 == 0:
					image_green2_ip.putPixel(int(i/2), int(j/2), slice.getPixel(i,j))
				elif i%2 == 1 and j%2 == 1:
					image_blue_ip.putPixel(int(i/2), int(j/2), slice.getPixel(i,j))
		print("done calculating ", s)
		
		red_stack.addSlice(stack.getSliceLabel(s), image_red_ip)
		green1_stack.addSlice(stack.getSliceLabel(s), image_green1_ip)
		green2_stack.addSlice(stack.getSliceLabel(s), image_green2_ip)
		blue_stack.addSlice(stack.getSliceLabel(s), image_blue_ip)
		
	red_imp = ImagePlus("red " + imp.title, red_stack)
	red_imp.show()
	green1_imp = ImagePlus("green1 " + imp.title, green1_stack)
	green1_imp.show()
	green2_imp = ImagePlus("green2 " + imp.title, green2_stack)
	green2_imp.show()
	blue_imp = ImagePlus("blue " + imp.title, blue_stack)
	blue_imp.show()

if __name__ in ['__builtin__','__main__']:
    run_script()
    