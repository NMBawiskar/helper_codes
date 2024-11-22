from jdeskew.estimator import get_angle
from jdeskew.utility import rotate
import cv2
import os
from utils import timings

from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures import ProcessPoolExecutor
from threading import Thread
import shutil

@timings
def get_tilt_angles(image_dir):
    images  = os.listdir(image_dir)
    dict_angles = {}
    dict_tilt = {}
    list_tilt_pages =[]
    rotatedImgList = []
    for imgName in images:
        ext = imgName.split(".")[-1]
        imgNameWoExt = imgName[:len(imgName)-(len(ext)+1)]
        pg_no = imgNameWoExt.split("-")[-1]

        path = os.path.join(image_dir, imgName)
        img = cv2.imread(path)
        angle = get_angle(img)

        rotated_img = rotate(img, angle)
        rotatedImgList.append(rotated_img)

        dict_angles[pg_no] = round(angle,3)
        tilt_status = False
        if abs(angle) <= 1:
            tilt = 'no_tilt'
            tilt_status=False
        elif abs(angle) <=2.5:
            tilt ='slight_tilt'
            tilt_status=True
            list_tilt_pages.append(str(pg_no))
        else:
            tilt = 'higher_tilt'
            tilt_status=True
            list_tilt_pages.append(str(pg_no))

        dict_tilt[pg_no] = tilt_status
        
         

    print(dict_angles)
    print(dict_tilt)
    return [dict_tilt, dict_angles, list_tilt_pages, rotatedImgList]


dict_angles = {}


def rotate_single_img_n_save(img_path, out_dir):
    try:
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        img_name = os.path.basename(img_path)
        img = cv2.imread(img_path)
        angle = get_angle(img)
        rotated_img = rotate(img, angle)
        cv2.imwrite(os.path.join(out_dir, img_name), rotated_img)
    except Exception as e:
        print(f"Error rotating image {img_path}: {e}")
        return False, None, img_path

    return True, angle, img_path 

def get_rotated_png(image_dir):
    images = sorted(os.listdir(image_dir), key=lambda x: int(''.join(c for c in x if c.isdigit())))
    # images  = sorted(os.listdir(image_dir))
    rotatedImgList = []
    angle_list = []

    for imgName in images:
        ext = imgName.split(".")[-1]
        imgNameWoExt = imgName[:len(imgName)-(len(ext)+1)]
        pg_no = imgNameWoExt.split("-")[-1]

        path = os.path.join(image_dir, imgName)
        img = cv2.imread(path)
        angle = get_angle(img)
        angle_list.append(angle)

        rotated_img = rotate(img, angle)
        rotatedImgList.append(rotated_img)
    
    print("angle_list", angle_list)
    return rotatedImgList

def get_corrected_tilt_images(image_dir):
    images  = os.listdir(image_dir)

    for imgName in images:
        ext = imgName.split(".")[-1]
        imgNameWoExt = imgName[:len(imgName)-(len(ext)+1)]
        pg_no = imgNameWoExt.split("-")[-1]

        path = os.path.join(image_dir, imgName)
        img = cv2.imread(path)
        angle = get_angle(img)

        rotated_img = rotate(img, angle)


def get_tilt_angle_img(imgIndex, img):
    global dict_angles
    angle = get_angle(img)

    dict_angles[imgIndex] = angle
    print(f'thread for img {imgIndex} finished.....')
    return angle


@timings
def get_tilt_angles_using_thread(image_dir):
    images  = os.listdir(image_dir)
    # dict_angles = {}
    dict_tilt = {}
    list_tilt_pages =[]
    list_threads = []
    for i, imgName in enumerate(images):
        ext = imgName.split(".")[-1]
        imgNameWoExt = imgName[:len(imgName)-(len(ext)+1)]
        pg_no = imgNameWoExt.split("-")[-1]

        path = os.path.join(image_dir, imgName)
        img = cv2.imread(path)
        # angle = get_angle(img)

        t1 = Thread(target=get_tilt_angle_img, args=(i, img))
        t1.start()
        print(f'thread for img {i} started')
        list_threads.append(t1)
    
    
    
    for t in list_threads:
        t1.join()


    print("all threads completed...")
    print('done') 
    print("dict_angles", dict_angles)
    
    return dict_tilt, dict_angles, list_tilt_pages

@timings
def get_tilt_using_map(image_dir):
    images  = os.listdir(image_dir)
    # dict_angles = {}
    dict_tilt = {}
    list_tilt_pages =[]
    list_threads = []

    pathList = [os.path.join(image_dir, imgName) for imgName in images] 

    imgList = [cv2.imread(path) for path in pathList]

    listIndices = [i for i in range(len(imgList))]

    anglelist = list(map(get_tilt_angle_img, listIndices, imgList))
    print(anglelist)


    print("all threads completed...")
    print('done') 
    print("dict_angles", dict_angles)
    
    return dict_tilt, dict_angles, list_tilt_pages

def process_image(imagePath):
    img = cv2.imread(imagePath)
    angle = get_angle(img)
    pg_no = os.path.basename(imagePath).split(".")[0].split("-")[-1]
    return imagePath, angle, pg_no
    


@timings
def get_tilt_angles_using_process_pool(image_dir):
    images_paths = [os.path.join(image_dir, img_name) for img_name in os.listdir(image_dir)]
    dict_angles = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(process_image, images_paths)
    for img_path, angle, _ in results:
        pg_no = os.path.basename(img_path).split(".")[0].split("-")[-1]
        dict_angles[pg_no] = angle
    print(dict_angles)

    return dict_angles
@timings
def get_corrected_tilt_using_thread_pool(image_dir, out_dir):
    images_paths = [os.path.join(image_dir, img_name) for img_name in os.listdir(image_dir)]
    dict_angles = {}

    

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(rotate_single_img_n_save, img_path, out_dir) for img_path in images_paths]
    
        
        dict_angles = {}
        failed_to_rotate_pages = []
        

        for future_ in as_completed(futures):
            success, angle, img_path = future_.result()
            pg_no = os.path.basename(img_path).split(".")[0].split("-")[-1]
            if success:
                dict_angles[pg_no] = angle

                print(f"Successfully rotated image {img_path}")
            else:
                failed_to_rotate_pages.append(pg_no)
                print(f"Failed to rotate image {img_path}")
                continue
                
        
        print(dict_angles)

    return dict_angles, failed_to_rotate_pages



def rotate_std_angle_pdfs_from_dir(input_dir, output_dir, angle_to_rotate:int):
    
    if angle_to_rotate ==90:
        angle = cv2.ROTATE_90_CLOCKWISE
    elif angle_to_rotate == 180:
        angle = cv2.ROTATE_180
    elif angle_to_rotate == -90:
        angle = cv2.ROTATE_90_COUNTERCLOCKWISE
    else:
        print("Invalid angle. Please enter 90, 180, or -90.")
        return

    img_files = os.listdir(input_dir)
   

    for img_name in img_files:
        img_path = os.path.join(input_dir, img_name)

        img = cv2.imread(img_path)
        rotated_img = cv2.rotate(img, angle)
        output_img_path = os.path.join(output_dir, img_name)
        cv2.imwrite(output_img_path, rotated_img)
    print(f"All images rotated and saved in {output_dir}")

def copy_images_from_one_dir_to_other(input_dir, output_dir):
    img_files = os.listdir(input_dir)
    for img_name in img_files:
        img_path = os.path.join(input_dir, img_name)
        output_img_path = os.path.join(output_dir, img_name)
        shutil.copy(img_path, output_img_path)
    print(f"All images copied from {input_dir} to {output_dir}")






if __name__ == "__main__":
    imgDir = r"pngs_extracted\13169856-581652_tilt_corrected"
    get_tilt_angles_using_process_pool(imgDir)
