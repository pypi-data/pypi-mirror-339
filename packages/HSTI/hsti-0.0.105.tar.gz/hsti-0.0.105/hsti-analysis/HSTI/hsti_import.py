import cv2 as cv
import numpy as np
import os
from natsort import natsorted

import os
import numpy as np
import cv2 as cv
from natsort import natsorted

def import_data_cube(directory, file_format='.ppm', rotate=True, verbose=False):
    """
    import_data_cube

    Imports a hyperspectral data cube from a sequence of image files or a single .pam/.npy file.

    The function searches for images in the specified directory. If no matching files are found,
    it will also check for subdirectories named 'capture/' or 'images/capture/'.

    Images are sorted using natural sorting and stacked into a 3D NumPy array where the first two
    dimensions are spatial and the third is spectral. For .pam or .npy files, the data is loaded
    directly as a full data cube.

    Parameters:
        directory (str): The path to the data directory or single file.
        file_format (str): File extension to look for (default: '.ppm').
        rotate (bool): Whether to rotate images 90 degrees counter-clockwise (default: True).
        verbose (bool): If True, prints the shape of the loaded data cube.

    Returns:
        np.ndarray: A 3D NumPy array representing the hyperspectral data cube.
    """
    imgs = None

    try:
        # --- Handle .pam file ---
        if directory.endswith('.pam'):
            header_info = {}
            with open(directory, 'rb') as f:
                while True:
                    line = f.readline().decode('ascii').strip()
                    if line == "ENDHDR":
                        data_start_pos = f.tell()
                        break
                    if line.startswith("WIDTH"):
                        header_info['width'] = int(line.split()[1])
                    elif line.startswith("HEIGHT"):
                        header_info['height'] = int(line.split()[1])
                    elif line.startswith("DEPTH"):
                        header_info['depth'] = int(line.split()[1])
                    elif line.startswith("MAXVAL"):
                        header_info['maxval'] = int(line.split()[1])

                f.seek(data_start_pos)
                dtype = np.uint16 if header_info['maxval'] > 255 else np.uint8
                shape = (header_info['height'], header_info['width'], header_info['depth'])
                imgs = np.fromfile(f, dtype=dtype).reshape(shape)
                imgs = imgs.astype('float64')

        # --- Handle .npy file ---
        elif directory.endswith('.npy'):
            imgs = np.load(directory).astype('float64')

        # --- Handle folder of individual images ---
        else:
            search_paths = [
                directory,
                os.path.join(directory, 'capture'),
                os.path.join(directory, 'images', 'capture')
            ]

            for path in search_paths:
                if os.path.exists(path) and any(file_format in fname for fname in os.listdir(path)):
                    new_directory = path
                    break
            else:
                new_directory = None

            if new_directory:
                file_lst = [
                    fname for fname in os.listdir(new_directory)
                    if file_format in fname and 'RGB' not in fname
                ]
                file_lst = natsorted(file_lst)
                imgs_list = []
                for fname in file_lst:
                    img_path = os.path.join(new_directory, fname)
                    img = cv.imread(img_path, cv.IMREAD_ANYDEPTH)
                    if rotate:
                        img = np.rot90(img)
                    imgs_list.append(img)
                if imgs_list:
                    imgs = np.array(imgs_list, dtype='float32')
                    imgs = np.moveaxis(imgs, 0, 2)

        if imgs is not None:
            if verbose:
                print('Hyperspectral image shape:')
                print(imgs.shape)
            return imgs
        else:
            print('Chosen directory either does not exist or contains no images of provided file type')
            return None

    except Exception as e:
        print(f"Error loading data cube: {e}")
        return None


    """
    ########## import_image_acquisition_settings ##########
    his function imports the image acquisition settings during the capturing event.
    The directory that the function uses as input must be the one containing the
    'images' directory.
    """
def import_image_acquisition_settings(directory, verbose = False):

    with open(f"{directory}/output.txt", 'r') as file:
        lines = file.readlines()
        temperature_lst = []
        for line in lines:
            if (len(line.split()) == 13) or (len(line.split()) == 10):
                temperature_lst.append(int(line.split()[6])/1000)
        sens_T = np.mean(temperature_lst)
        if len(lines[-1].split()) == 13:
            GSK = int(lines[-1].split()[10])
            GFID = int(lines[-1].split()[11])
            Gain = float(lines[-1].split()[12])
        else:
            GSK = None
            GFID = None
            Gain = None

    if verbose:
        print(f'Sensor temperature: {sens_T}')
        print(f'GSK: {GSK}')
        print(f'GFID: {GFID}')
        print(f'Gain: {round(Gain,2)}')

    valdict = {
      'SENS_T': sens_T,
      'GSK': GSK,
      'GFID': GFID,
      'GAIN': Gain
    }

    return valdict
