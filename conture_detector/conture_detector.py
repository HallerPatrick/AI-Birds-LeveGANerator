import numpy as np
import cv2
import json


def view_image(image):
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def centroid(*points):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    _len = len(points)
    centroid_x = sum(x_coords)/_len
    centroid_y = sum(y_coords)/_len
    return [centroid_x, centroid_y]


def conture_detector(image_path):
    """
    Conture detector returns a list of centroids of a generated image (of nn).


    """
    
    image = cv2.imread(image_path)
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    green_low = np.array([45, 100, 50])
    green_high = np.array([75, 255, 255])
    curr_mask = cv2.inRange(hsv_img, green_low, green_high)
    hsv_img[curr_mask > 0] = ([75, 255, 200])

    # converting the HSV image to Gray inorder to be able to apply
    # contouring
    RGB_again = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)
    gray = cv2.cvtColor(RGB_again, cv2.COLOR_RGB2GRAY)

    ret, threshold = cv2.threshold(gray, 90, 255, 0)

    a, contours, _ = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    centroid_points = []

    for contour in contours:
        contour = contour.tolist()

        contour_ = []
        for c in contour:
            contour_.append((*c[0],))

        centroid_point = centroid(*contour_)
        centroid_points.append(centroid_point)

    return centroid_points


def conture_detector_from_image_object(image):
    """
    Conture detector returns a list of centroids of a generated image (of nn).


    """

    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    green_low = np.array([45, 100, 50])
    green_high = np.array([75, 255, 255])
    curr_mask = cv2.inRange(hsv_img, green_low, green_high)
    hsv_img[curr_mask > 0] = ([75, 255, 200])

    # converting the HSV image to Gray inorder to be able to apply
    # contouring
    RGB_again = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)
    gray = cv2.cvtColor(RGB_again, cv2.COLOR_RGB2GRAY)

    ret, threshold = cv2.threshold(gray, 90, 255, 0)

    a, contours, _ = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    centroid_points = []

    for contour in contours:
        contour = contour.tolist()

        contour_ = []
        for c in contour:
            contour_.append((*c[0],))

        centroid_point = centroid(*contour_)
        centroid_points.append(centroid_point)

    return centroid_points


def write_to_json(fielpath, centroids):
    with open(fielpath, "w") as f:
        json.dump(centroids, f, indent=4)


def main():
    centroids = conture_detector("sample.png")

    write_to_json("centroids.json", centroids)

if __name__ == "__main__":
    main()


# cv2.drawContours(image, contours, -1, (255, 255, 255), 3)
# view_image(image)  # 5
