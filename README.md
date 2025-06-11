# GG2-DICOM-Processing

Python scripts used for CT reconstruction and visualisation as part of the GG2 project.

## Overview

This repository contains tools for preprocessing DICOM data from CT scans of a toy mascot. The goal is to prepare clean, merged volumetric data for surface extraction, visualisation, and 3D printing.

## Scripts

- `remove.py`  
  Applies a circular mask to eliminate the cylindrical scanning shell by setting voxels outside a defined radius to air. 

- `merge.py`  
  Flips and merges two separate scan volumes (e.g., top and bottom halves of the toy) into a single coherent 3D dataset.

- `CL-Ridler.py`  
  This is a separate file to compute the CL-Ridler threshold for a given volume in 3D Slicer using SimpleITK.
