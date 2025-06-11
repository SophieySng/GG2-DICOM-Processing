"""This is performed on the outputs of the script named remove.py """

import numpy as np
import nrrd

# === Load input files ===
top_file = "a.nrrd"       # Unflipped top scan
bottom_file = "b.nrrd" # Unflipped bottom scan

top, top_header = nrrd.read(top_file)
bottom, bottom_header = nrrd.read(bottom_file)

# === Flip the bottom volume ===
# Flip Z (slice order)
bottom_flipped = np.flip(bottom, axis=2)

# Optionally flip Y and/or X (to correct mirroring)
# bottom_flipped = np.flip(bottom_flipped, axis=1)  # Flip Y (antero-posterior)
bottom_flipped = np.flip(bottom_flipped, axis=0)  # Flip X (left-right)

# === Merge along Z (slices) ===
merged = np.concatenate((top, bottom_flipped), axis=2)

# === Update header ===
merged_header = top_header.copy()
merged_header['sizes'] = list(merged.shape[::-1])  # NRRD uses (X, Y, Z) in reverse

# === Save output ===
output_file = "full.nrrd"
nrrd.write(output_file, merged, header=merged_header)

print(f"Merged and flipped volume saved to: {output_file}")
