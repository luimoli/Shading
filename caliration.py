import cv2
import numpy as np
from pathlib import Path


def shading_save(shading_img_root, save_path):
    root = Path(shading_img_root)
    file_lst = [f for f in root.iterdir() if f.is_file()]
    img_arr = []
    for img_path in file_lst:
        img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
        shading_image_normalized = img / np.max(img)
        img_arr.append(shading_image_normalized[..., None])
    img_arr = np.concatenate(img_arr, -1)
    res = np.mean(img_arr, 2)
    np.savetxt(save_path, res)



# def shading_correction():

    


def lens_shading_correction(image, shading_image):
    # Convert the images to float32 for accurate calculations
    image = image.astype(np.float32)
    shading_image = shading_image.astype(np.float32)

    shading_image_normalized = shading_image / np.max(shading_image)
    corrected_image = image / shading_image_normalized
    corrected_image = np.clip(corrected_image, 0, 255)

    corrected_image = corrected_image.astype(np.uint8)

    return corrected_image


if __name__ =='__main__':

    # ------save parameter--------------------
    shading_save('./image', './test.txt')

    # # Load the original image and shading image
    # original_image = cv2.imread('image\Image__2023-09-15__17-19-39.bmp', cv2.IMREAD_GRAYSCALE)
    # shading_image = cv2.imread('image\Image__2023-09-15__17-19-54.bmp', cv2.IMREAD_GRAYSCALE)


    # Perform lens shading correction
    # corrected_image = lens_shading_correction(original_image, shading_image)

    # # Display the original and corrected images
    # cv2.imshow('Original Image', original_image)
    # cv2.imshow('Corrected Image', corrected_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # ------correction tmp ------------
    original_image = cv2.imread('test\CameraImg_0002(1).jpg', cv2.IMREAD_GRAYSCALE)
    calib = np.loadtxt('./test.txt')
    corrected_image = original_image / calib
    corrected_image = np.clip(corrected_image, 0, 255)
    corrected_image = corrected_image.astype(np.uint8)
    cv2.imwrite('./test_res.jpg', corrected_image)
    print(corrected_image.shape)