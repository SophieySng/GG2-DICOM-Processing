"""This file converts DICOM format to NRRD. It processes 1 DICOM folder at a time."""

import os
import numpy as np
import pydicom
import nrrd
from glob import glob
from tqdm import tqdm

# === CONFIGURATION ===
dicom_folder = "/Users/yangmengyujia/recon_normalise_b"
output_nrrd_path = "masked_b.nrrd"
radius_mm = 52

# === LOAD DICOM ===
dicom_files = sorted(glob(os.path.join(dicom_folder, "*.dcm")))
volume = []
pixel_spacing = None

for file in tqdm(dicom_files, desc="Loading DICOM"):
    ds = pydicom.dcmread(file)
    if pixel_spacing is None:
        pixel_spacing = [float(sp) for sp in ds.PixelSpacing]
        slice_thickness = float(ds.SliceThickness)

    rescale_slope = float(ds.RescaleSlope)
    rescale_intercept = float(ds.RescaleIntercept)
    corrected_slice = ds.pixel_array * rescale_slope + rescale_intercept
    volume.append(corrected_slice)

volume = np.array(volume)  # shape (Z, Y, X)
Z, Y, X = volume.shape
cx, cy = X // 2, Y // 2

# === CREATE CIRCULAR MASK (2D) ===
pixel_radius = radius_mm / pixel_spacing[0]
yy, xx = np.ogrid[:Y, :X]
dist = np.sqrt((yy - cy)**2 + (xx - cx)**2)
mask_2d = dist <= pixel_radius

# === APPLY MASK (vectorized) ===
mask_3d = np.broadcast_to(mask_2d, (Z, Y, X))
volume[~mask_3d] = -1024

# === PREPARE HEADER ===
header = {
    'type': 'short',
    'dimension': 3,
    'space': 'left-posterior-superior',
    'sizes': list(volume.shape[::-1]),
    'space directions': [[pixel_spacing[1], 0.0, 0.0],
                         [0.0, pixel_spacing[0], 0.0],
                         [0.0, 0.0, slice_thickness]],
    'kinds': ['domain', 'domain', 'domain'],
    'endian': 'little',
    'encoding': 'gzip'
}

# === SAVE WITH PROGRESS BAR (slice-wise simulation) ===
# Note: This is only a simulated bar — full NRRD write still happens in one line
transposed = volume.transpose(2, 1, 0)  # NRRD expects (X, Y, Z)
print("Saving NRRD (simulated progress)...")

with tqdm(total=transposed.shape[2], desc="Saving NRRD") as pbar:
    # Fake slice-by-slice progress
    for _ in range(transposed.shape[2]):
        pbar.update(1)
    # Actual save
    nrrd.write(output_nrrd_path, transposed, header)

print("NRRD file saved:", output_nrrd_path)
