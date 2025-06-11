import numpy as np
import SimpleITK as sitk
import sitkUtils

# Get volume node
volumeNode = getNode('full')  # Replace with loaded volume name
imageData = sitkUtils.PullVolumeFromSlicer(volumeNode)

# Convert to numpy
array = sitk.GetArrayFromImage(imageData)

# Flatten and remove background (optional)
pixels = array.flatten()
pixels = pixels[pixels > np.min(pixels)]

# Ridler thresholding (iterative intermeans)
def ridler_threshold(pixels, max_iter=100):
    T = pixels.mean()
    for _ in range(max_iter):
        G1 = pixels[pixels <= T]
        G2 = pixels[pixels > T]
        T_new = 0.5 * (G1.mean() + G2.mean())
        if abs(T - T_new) < 1:
            break
        T = T_new
    return T

T_ridler = ridler_threshold(pixels)
print(f"CL-Ridler Threshold = {T_ridler:.2f}")

# Use the threshold in Segment Editor → Threshold tool manually
