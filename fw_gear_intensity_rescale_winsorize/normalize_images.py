import numpy as np
import nibabel as nib

def scale_winorize(img_path):

    img = nib.load(img_path)
    img_data = img.get_fdata()
    img_data = np.float32(img_data)

    max_val = np.percentile(img_data, 99) # Find the 99.99th percentile
    min_val = np.percentile(img_data, 1)

    img_data[img_data <= min_val] = min_val # mask for less than 1st percentile, gets changed to value of 1st percentile
    img_data[img_data >= max_val] = max_val # mask for greater than 99th percentile, gets changed to value of 99th percentile

    img_data = ((img_data - min_val) * 1.0) / (max_val - min_val) # normalize entire image to be within range of 0-1

    normalized_image = nib.Nifti1Image(img_data, img.affine, img.header)

    return normalized_image
