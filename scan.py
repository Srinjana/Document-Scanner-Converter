# run the code using the following commands
# python scan.py --image images/page.jpg
# python scan.py --image images/receipt.jpg
# python scan.py --image images/speakeasy.jpg
# python scan.py --image images/handwriting.jpg

# importing necessary packages
from scanner_opencv.transform import four_point_transform
# from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
import img2pdf
from PIL import Image
import os

# constructing the argument parser and parsing args
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "path to the Image to be scanned")
args = vars(ap.parse_args())

# loading image and adjusting ratio of new to old height and cloning it
image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height=500)

# preprocessing
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurry= cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurry, 75, 200)

# show the original image and the edge detected image
cv2.imshow("Image", image)
cv2.imshow("Edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

# finding the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	# if our approximated contour has four points, then we
	# can assume that we have found our screen
	if len(approx) == 4:
	    screenCnt = approx
	    break

# show the contour (outline) of the piece of paper
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline Contours", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# obtaining top-down view of ROI
warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
warped = cv2.GaussianBlur(warped, (5, 5), 0)
T = cv2.adaptiveThreshold(
	warped, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
warped = (warped < T).astype("uint8") * 255

# show the original and scanned images
cv2.imshow("Original", imutils.resize(orig, height=650))
cv2.imshow("Scanned", imutils.resize(warped, height=650))
cv2.waitKey(0)

# write and convert to pdf
cv2.imwrite("output/processed.jpg", warped)
image_final = Image.open(r"output/processed.jpg")
pdf_bytes = img2pdf.convert(r"output/processed.jpg")
file = open(r'output/final.pdf', "wb")
file.write(pdf_bytes)
file.close()
print("pdf has been made successfully")
# imf.save(r'images/scanned_copy.pdf')

## it is recommended you change the name of the processed image file and the pdf file to avoid discrepancies

