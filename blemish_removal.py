import cv2
import numpy as np

def calcNoise(img):
    """
    Get a measurement of noise by calculating the ratio of high frequencies compared
    to all frequencies
    :param img: input image with shape (30,30)
    :return: high frequency ratio
    """
    if(img.shape!=(30,30)):
        raise Exception('invalid input shape')
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift))
    sum_mag_spec = np.sum(magnitude_spectrum)
    mask = np.ones(img.shape)
    mask[7:23, 7:23] = np.logical_not(cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (16, 16)))
    filtered_mag_spec = magnitude_spectrum * mask
    sum_filtered_mag_spec = np.sum(filtered_mag_spec)
    highRatio = sum_filtered_mag_spec / sum_mag_spec
    return highRatio


def removeBlemish(action, x, y, flags, userdata):
    """
    mouse callback to remove blemishes on an image
    :param action:
    :param x:
    :param y:
    :param flags:
    :param userdata:
    :return:
    """
    global source
    if action == cv2.EVENT_LBUTTONDOWN:
        neighbor_patches = []
        blemish_patch_noise_score = 1
        for i in range(-1, 2):
            for j in range(-1, 2):
                patch = source[(y - 15 + 30 * j):(y + 15 + 30 * j), (x - 15 + 30 * i):(x + 15 + 30 * i), :]
                if i == 0 and j == 0:
                    blemish_patch_noise_score = calcNoise(cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY))
                else:
                    neighbor_patches.append(patch)

        min_noise = 1
        smoothest_neighbor = np.zeros((30, 30, 3))
        for patch in neighbor_patches:
            tmp_noise = calcNoise(cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY))
            if tmp_noise < min_noise:
                min_noise = tmp_noise
                smoothest_neighbor = patch
        if min_noise < blemish_patch_noise_score:
            source_cp = source.copy()
            mask2d = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (30, 30)) * 255
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
