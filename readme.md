### Export your blender

In Blender, go to 'scripting'(top bar) then in 'Text' (top bar of the text editor) select 'Open' and open the script 'export_from_blender.py'

If not already done, import the Yaml python package in blender by copyin the three yaml folders ('yaml' , 'PyYAML-6.0.dist-info' , '_yaml') in :  blender/versionX.X/python/lib/pythonY.Y

You may have to change the 'mesh_root_path' (line 6 of the script) to match the location you want and the name of the scene set to Adream by default (line 7) to match your scene name ( you can see scene name in the top right corner)

> You can hide categories before the export if you dont want to export them by excluding them from the viewlayer (case next to the categories name)
 or hiding them in viewport (eyes next to the categories name). You can't hide mesh from the export only categories and if you use camera in blender put them in categories and hide the categories before launching the script.

After that, use the 'run script' button (play button in the top bar) and all your meshes will be exported in the desired formats (available formats are fbx, stl and obj).

If there is an error saying that the yaml librairy is not found. Try to open the blender where you put the library in and then open the project you want to export instead of opening directly your project.
