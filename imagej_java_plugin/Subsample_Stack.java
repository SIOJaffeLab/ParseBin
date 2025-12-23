import ij.*;              // Gives us access to ImagePlus, ImageStack, IJ
import ij.process.*;      // Gives us access to ImageProcessor
import ij.plugin.PlugIn;  // This is what makes it a plugin

/**
 * An ImageJ plugin that creates a new stack by copying every other 
 * pixel in X and Y from the currently open stack.
 *
 * The underscore in the class name "Subsample_Stack" tells
 * ImageJ to create a menu item called "Subsample Stack".
 */
public class Subsample_Stack implements PlugIn {

    // The 'run' method is what ImageJ calls when the plugin is selected
    public void run(String arg) {
    
        // 1. Get the currently open image
        ImagePlus imp = IJ.getImage(); // 'imp' is the standard name for an ImagePlus
        
        // 2. Check if it's a stack
        if (imp.getStackSize() <= 1) {
            IJ.error("This plugin requires a stack (an image with multiple slices).");
            return; // Stop the plugin
        }
        
        ImageStack sourceStack = imp.getStack();

        // 3. Get dimensions
        int width = imp.getWidth();
        int height = imp.getHeight();
        int nSlices = imp.getStackSize();

        // 4. Calculate new, smaller dimensions
        int newWidth = width / 2;
        int newHeight = height / 2;

        // 5. Create a new, empty stack to hold the results
        ImageStack red_targetStack = new ImageStack(newWidth, newHeight);
        ImageStack green1_targetStack = new ImageStack(newWidth, newHeight);
        ImageStack green2_targetStack = new ImageStack(newWidth, newHeight);
        ImageStack blue_targetStack = new ImageStack(newWidth, newHeight);

        // 6. Loop through all slices in the source stack
        for (int s = 1; s <= nSlices; s++) {
            IJ.showProgress(s, nSlices);
            
            // Get the processor for the current slice
            ImageProcessor sourceProcessor = sourceStack.getProcessor(s);
            
            // Create a new, blank processor for the target slice
            ImageProcessor red_targetProcessor = sourceProcessor.createProcessor(newWidth, newHeight);
            ImageProcessor green1_targetProcessor = sourceProcessor.createProcessor(newWidth, newHeight);
            ImageProcessor green2_targetProcessor = sourceProcessor.createProcessor(newWidth, newHeight);
            ImageProcessor blue_targetProcessor = sourceProcessor.createProcessor(newWidth, newHeight);

            // 7. Loop over the NEW (smaller) image dimensions
            for (int y = 0; y < newHeight; y++) {
                for (int x = 0; x < newWidth; x++) {
                    
                    // Read pixel from source at (2*x, 2*y)
                    // getf() works for 32-bit float images. Use get() for 8-bit or 16-bit.
                    float red_pixelValue = sourceProcessor.get(x * 2, y * 2); 
                    float green1_pixelValue = sourceProcessor.get(x * 2+1, y * 2); 
                    float green2_pixelValue = sourceProcessor.get(x * 2, y * 2+1); 
                    float blue_pixelValue = sourceProcessor.get(x * 2+1, y * 2+1); 
                    
                    // Write pixel to target at (x, y)
                    red_targetProcessor.setf(x, y, red_pixelValue);
                    green1_targetProcessor.setf(x, y, green1_pixelValue);
                    green2_targetProcessor.setf(x, y, green2_pixelValue);
                    blue_targetProcessor.setf(x, y, blue_pixelValue);
                }
            }
            
            // Add the newly created slice to our new stack
            red_targetStack.addSlice(red_targetProcessor);
            green1_targetStack.addSlice(green1_targetProcessor);
            green2_targetStack.addSlice(green2_targetProcessor);
            blue_targetStack.addSlice(blue_targetProcessor);
        }
        
        IJ.showProgress(1.0);
        IJ.showStatus("Subsampling complete.");

        // 8. Create a new image window for our target stack and show it
        ImagePlus red_targetImp = new ImagePlus("Subsampled red-" + imp.getTitle(), red_targetStack);
        ImagePlus green1_targetImp = new ImagePlus("Subsampled green1-" + imp.getTitle(), green1_targetStack);
        ImagePlus green2_targetImp = new ImagePlus("Subsampled green2-" + imp.getTitle(), green2_targetStack);
        ImagePlus blue_targetImp = new ImagePlus("Subsampled blue-" + imp.getTitle(), blue_targetStack);

        red_targetImp.show();
        green1_targetImp.show();
        green2_targetImp.show();
        blue_targetImp.show();
    }
}
