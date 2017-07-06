from os.path import isfile, splitext
from subprocess import check_call, CalledProcessError


def convert(pdf):
    """Convert a PDF to JPG"""
    if not isfile(pdf):
        print("ERROR", "Can't find {0}".format(pdf))
        return

    png = splitext(pdf)[0] + ".png"
    pdf = pdf + "[0]"

    try:
        check_call(["convert", "-density", "100", "-colorspace", "RGB",  pdf, png])
        print("Converted", "{0} converted".format(pdf))
    except (OSError, CalledProcessError) as e:
        print("ERROR", "ERROR: {0}".format(e))


if __name__ == "__main__":
    convert("./test.pdf")