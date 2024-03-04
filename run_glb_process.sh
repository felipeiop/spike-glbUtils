#!/bin/bash

echo "Batch processing glb files...."

#run a Blender instance
/Applications/Blender.app/Contents/MacOS/Blender -b -P glb_process.py

#done processing
echo "Done processing files."
