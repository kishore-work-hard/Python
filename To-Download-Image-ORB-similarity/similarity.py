
import os, time
import cv2

img_count = 1


# Works well with images of different dimensions
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


while True:
    flag = 0

    p_frame_c = cv2.imread("./live/cam_c_" + str(img_count - 1) + ".jpg", 0)
    p_frame_d = cv2.imread("./live/cam_d_" + str(img_count - 1) + ".jpg", 0)
    p_frame_e = cv2.imread("./live/cam_e_" + str(img_count - 1) + ".jpg", 0)
    # p_frame_f = cv2.imread("./live/cam_f_" + str(img_count - 1) + ".jpg", 0)

    cam_c = cv2.VideoCapture(0)
    cam_d = cv2.VideoCapture(1)
    cam_e = cv2.VideoCapture(2)
    # cam_f = cv2.VideoCapture(3)

    _c, frame_c = cam_c.read()
    _d, frame_d = cam_d.read()
    _e, frame_e = cam_e.read()
    # _f, frame_f = cam_f.read()

    orb_similarity_c = orb_sim(p_frame_c, frame_c)
    orb_similarity_d = orb_sim(p_frame_d, frame_d)
    orb_similarity_e = orb_sim(p_frame_e, frame_e)
    # orb_similarity_f = orb_sim(p_frame_f, frame_f)

    print("Similarity c using ORB is: ", orb_similarity_c)
    print("Similarity d using ORB is: ", orb_similarity_d)
    print("Similarity e using ORB is: ", orb_similarity_e)
    # print("Similarity f using ORB is: ", orb_similarity_f)
    print("")
    if orb_similarity_c < 0.50:
        cv2.imwrite("./live/cam_c_" + str(img_count) + ".jpg", frame_c)
        flag = 1
    if orb_similarity_d < 0.50:
        cv2.imwrite("./live/cam_d_" + str(img_count) + ".jpg", frame_d)
        flag = 1
    if orb_similarity_e < 0.50:
        cv2.imwrite("./live/cam_e_" + str(img_count) + ".jpg", frame_e)
        flag = 1
    # if orb_similarity_f < 0.50:
    #     cv2.imwrite("./live/cam_f_" + str(img_count) + ".jpg", frame_f)
    #     flag = 1

    # t = time.time()
    # time.sleep(600)
    # t1 = time.time() - t
    # print('{}ms : '.format(int(t1 * 1000)))

    if flag == 1:
        print(img_count)
        img_count += 1
        time.sleep(600)
