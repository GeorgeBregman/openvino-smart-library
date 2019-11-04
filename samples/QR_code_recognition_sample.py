import sys, os
import tempfile
import argparse
import numpy as np
import cv2
sys.path.append("../src/modules")
import book_recognizer as br
import QR_generator as qr


# Display QR code location
def display(image, bbox):
    n = len(bbox)
    for j in range(n):
        cv2.line(image, tuple(bbox[j][0]), tuple(bbox[(j + 1) % n][0]), (255, 0, 0), 3)

    # Display results
    cv2.imshow("Results", image)


def createArgparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', nargs='?', default=None)
    return parser.parse_args()


# Main
if __name__ == '__main__':
    qrDecoder = br.BookRecognizer.create(2)
    args = createArgparse()
    if args.name is not None:
        if args.name == 'GUI':
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not cap.isOpened():
                raise IOError("Cannot open WebCam")
            data = ""
            while True:
                ret, image = cap.read()
                cv2.imshow('WebCam', image)
                key = cv2.waitKey(10) & 0xff
                if key == 27:
                    break
                data = qrDecoder.recognize(image)
                if data != "":
                    break
            print("Decoded Data : {}".format(data))
            cap.release()
            cv2.destroyAllWindows()
        else:
            s = args.name
            image = cv2.imread(s)
            data = qrDecoder.recognize(image)
            if data == "":
                print("QR-code not detected!!!")
            else:
                display(image, qrDecoder.box)
                cv2.waitKey(0)
                print("Decoded Data : {}".format(data))
    else:
        print("To use recognizer, you have to input 'GUI' or name of your image as arguments of program")
