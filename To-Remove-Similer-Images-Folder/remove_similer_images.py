import cv2
import os


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


folder_path = './data'  # Replace with the actual folder path

unique_images = []

# Step 1: Find unique images
for filename in os.listdir(folder_path):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(folder_path, filename)
        img = cv2.imread(img_path, 0)

        is_similar = False
        img_hash = hash(img.tobytes())  # Convert image array to a hashable representation

        for unique_img in unique_images:
            unique_img_hash = hash(unique_img.tobytes())
            similarity = orb_sim(img, unique_img)
            print(similarity)
            if similarity >= 0.85 :
                print("True")
                is_similar = True
                break

        if not is_similar:
            unique_images.append(img)

# Step 2: Remove similar images
for filename in os.listdir(folder_path):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(folder_path, filename)
        img = cv2.imread(img_path, 0)

        img_hash = hash(img.tobytes())  # Convert image array to a hashable representation

        if img_hash not in [hash(unique_img.tobytes()) for unique_img in unique_images]:
            os.remove(img_path)
            print(f"Removed similar image: {filename}")
