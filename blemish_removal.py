import cv2
import numpy as np


def calcNoise(img):
    # print(img.shape)
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift))
    sum_mag_spec = np.sum(magnitude_spectrum)
    mask = np.ones(img.shape)
    mask[10:20, 10:20] = 0
    filtered_mag_spec = magnitude_spectrum * mask
    sum_filtered_mag_spec = np.sum(filtered_mag_spec)
    highRatio = sum_filtered_mag_spec / sum_mag_spec
    return highRatio


def removeBlemish(action, x, y, flags, userdata):
    global source
    if action == cv2.EVENT_LBUTTONDOWN:
        print(x)
        print(y)
        neighbor_patches = []
        blemish_patch = np.zeros((30, 30))
        blemish_patch_noise_score = 1
        for i in range(-1, 2):
            for j in range(-1, 2):
                print(source.shape)
                print(x - 15 + 30 * j)
                print(x + 15 + 30 * j)
                print(y - 15 + 30 * i)
                print(y + 15 + 30 * i)
                patch = source[(y - 15 + 30 * j):(y + 15 + 30 * j), (x - 15 + 30 * i):(x + 15 + 30 * i), :]
                print(patch.shape)
                if i == 0 and j == 0:
                    blemish_patch = patch
                    blemish_patch_noise_score = calcNoise(cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY))
                    # print(tmp_noise)
                else:
                    neighbor_patches.append(patch)

        min_noise = 1
        smoothest_neighbor = np.zeros((30, 30))
        print(len(neighbor_patches))
        for patch in neighbor_patches:
            tmp_noise = calcNoise(cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY))
            if tmp_noise < min_noise:
                min_noise = tmp_noise
                print(min_noise)
                smoothest_neighbor = patch
        if min_noise < blemish_patch_noise_score:
            print("correcting image...")
            source_cp = source.copy()
            mask2d = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (30, 30))*255
            source = cv2.seamlessClone(smoothest_neighbor, source_cp, mask2d, (x, y), cv2.NORMAL_CLONE)


source = cv2.imread("blemish.png", 1)
cv2.namedWindow("Blemish_removal")
# highgui function called when mouse events occur
cv2.setMouseCallback("Blemish_removal", removeBlemish)
k = 0
# loop until escape character is pressed
while k != 27:
    cv2.imshow("Blemish_removal", source)

    k = cv2.waitKey(20) & 0xFF

cv2.destroyAllWindows()
