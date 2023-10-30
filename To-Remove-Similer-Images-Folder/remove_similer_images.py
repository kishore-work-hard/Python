import cv2
import os
import imagehash
from PIL import Image
from multiprocessing import Pool, Manager
from functools import partial

def orb_sim(img1, img2):
    orb = cv2.ORB_create()
    kp_a, desc_a = orb.detectAndCompute(img1, None)
    kp_b, desc_b = orb.detectAndCompute(img2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(desc_a, desc_b)
    similar_regions = [i for i in matches if i.distance < 50]
    if len(matches) == 0:
        return 0
    return len(similar_regions) / len(matches)

def calculate_image_hash(img):
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return str(imagehash.dhash(pil_img))

def process_image(img_path, shared_dict):
    img = cv2.imread(img_path)
    is_similar = False
    img_hash = calculate_image_hash(img)

    for unique_hash, unique_img in shared_dict.items():
        similarity = orb_sim(img, unique_img)
        if similarity >= 0.85:

            print("DEL-",img_path, "SIM-", similarity)
            is_similar = True
            os.remove(img_path)
            txt_file_path = os.path.splitext(img_path)[0] + '.txt'
            if os.path.exists(txt_file_path):
                os.remove(txt_file_path)
            break

    if not is_similar:
        shared_dict[img_hash] = img
    return img_path

def remove_image_and_txt(img_path):
    try:
        os.remove(img_path)
        txt_file = os.path.splitext(img_path)[0] + ".txt"
        if os.path.exists(txt_file):
            os.remove(txt_file)
            print(f"Removed similar image: {os.path.basename(img_path)} and its associated .txt file")
        else:
            print(f"Removed similar image: {os.path.basename(img_path)}")
    except Exception as e:
        print(f"Error while removing image: {os.path.basename(img_path)} - {str(e)}")

if __name__ == '__main__':
    folder_path = '3-DONE'  # Replace with the actual folder path
    manager = Manager()
    unique_images = manager.dict()

    image_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith(('.jpg', '.jpeg', '.png'))]

    # Create a partial function with shared_dict as a fixed argument
    partial_process_image = partial(process_image, shared_dict=unique_images)

    # Parallel processing
    with Pool(processes=None) as pool:
        processed_image_paths = pool.map(partial_process_image, image_paths)






