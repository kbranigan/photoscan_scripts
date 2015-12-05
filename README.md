
Thought I'd host these scripts so people could collaborate on them and add new ones.

I picked this naming format to mirror the scripts found on:
http://wiki.agisoft.com/wiki/Python

`PS110_bounding_box_to_coordinate_system.py`
 The script can be used to bring the bounding box in accordance to the coordinate system used for the active chunk. Sides of the bounding box will be made parallel to the coordinate system axis.

`PS110_coordinate_system_to_bounding_box.py` 
The script can be used to bring the chunks' coordinate system in accordance to the sides of the bounding box.

`PS110_copy_bounding_box.py`
The script copies the bounding box from the active chunk for all other chunks in the project.

`PS110_batch_export_orthophoto_dialog.py`
The script can be used to export set of orthophotos based on the individual cameras.

`PS110_masking_by_color_dialog.py`
The script can be used to create masks for images based on user selected color and tolerance.

`PS110_split_in_chunks_dialog.py`
This script allows to split the original chunk into multiple chunks with smaller bounding boxes forming a grid. Optionally dense cloud / mesh can be generated in smaller boxed and merged back in to single chunk.