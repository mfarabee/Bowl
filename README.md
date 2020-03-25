# Bowl
 This program will generate Gcode to cut a bowl into a flat surface.
 You can specify the depth of the bowl as well as the diameter at the surface.
 It is assumed that a round nose cutter is being used.
 
 X/Y zero location is at the center of the bowl.
 
 The gcode generated will use G2 and G3 commands on the XZ plane, cutting multiple passes 
 based on the rough and finish depths specified.

To install and run the program:  
* Option 1:  
  Copy bowl.zip to a directory on your computer and extract it.  
  Execute the "bowl.bat" program  
  
* Option 2:  
  Copy the "bowl.bat" file and "dist" directory to your windows PC.  
  Then execute "bowl.bat"  
