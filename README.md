# Document-Scanner-Converter
The application reads the input image files and performs edge detection to generate a birds-eye view of the document, it generates a scanned copy of the same and saves it as an image file as well as a pdf in an output folder.
---
## Components

* `images` folder contains the input image files.
* `output` folder contains the image and pdf files of the processed images.
* the folder `scanner_opencv` has a code for custom four-point-transform under the name of `transform.py`
---
## Run the Code
```
  python scan.py --image images/page.jpg
  python scan.py --image images/receipt.jpg
  python scan.py --image images/speakeasy.jpg
  python scan.py --image images/handwriting.jpg
```
Use any of the commands above to run the code.
