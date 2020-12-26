# Bowl
 This program will generate Gcode to cut a bowl into a flat surface.
 You can specify the depth of the bowl as well as the diameter at the surface.
 It is assumed that a round nose cutter is being used.
 
 X/Y zero location is at the center of the bowl.
 
 The gcode generated will use G2 and G3 commands on the XZ plane, cutting multiple passes 
 based on the rough and finish depths specified.

- Z Safety
	Distance the cutter will move in "Z" to clear work surface before making rapid moves

- Spindle Speed
	Speed of spindle (performs M03 command, Spindle on CW @ speed specified)
- Rough Feed Rate
	Feed rate for roughing cuts
- Finish Feed Rate
	Feed rate for finishing cuts
- Bowl 
	- Diameter
		Diameter to bowl
	- Depth
		Depth of bowl (assumes to of bowl is at Z=0.0)
- Tool 
	- Diameter
		Diameter of round nose cutter
	- Rough Cut 
		Depth for roughing passes 
	- Finish Cut 
		Depth for final finish pass. If set to "0", no finish pass
		will take place.
	- Rough Step 
		Distance the cutter will move within a pass as a
		% of tool diameter. 50% would move the tool half the
		tool diameter for each step during each roughing pass.
		1-100% are valid inputs.
	- Finish Step 
		Distance the cutter will move within a pass as a
		% of tool diameter. 50% would move the tool half the
		tool diameter for each step during the finishing pass.
		1-100% are valid inputs.

To install and run the program:  
* Option 1:  
  Copy bowl.zip to a directory on your computer and extract it.  
  Execute the "bowl.bat" program  
  
* Option 2:  
  Copy the "bowl.bat" file and "dist" directory to your windows PC.  
  Then execute "bowl.bat"  
