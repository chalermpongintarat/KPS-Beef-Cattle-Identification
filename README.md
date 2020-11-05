# KPS-Beef-Cattle-Identification
Kamphaeng Saen Beef Cattle Identification Approach using Muzzle Print Image

The proposed scheme uses Scale Invariant Feature Transform (SIFT) for detecting the interesting points for image matching. Gabor Filter method is proposed enhancement of muzzle print image quality before get the interesting points. For a robust identification scheme, a Random Sample Consensus (RANSAC) algorithm has been coupled with the SIFT output to remove the outlier points and achieve more robustness. Finally, the feature matching is accomplished by the Brute-Force Matchers.

Develope with SKimage and OpenCV

Requirements:
- NumPy
- SKimage
- OpenCV2


Works by extracting minutiae points using harris corner detection.

Uses SIFT (ORB) go get formal descriptors around the keypoints with brute-force hamming distance and then analyzes the returned matches using thresholds.

Usage:

1. Place 2 muzzle print image that you want to compare inside the database folder.
2. Pass the names of the muzzle print image as arguments in the console.

## Dockerfile

If you don't want to install the libraries, or want a easier way to test the application you can follow the commands:

```shell
docker build -t <name_of_your_choice> .

docker run -it <name_of_your_choice> <muzzle_print_image_1> <muzzle_print_image_2>
```

If you don't have Docker Engine imstalled, you can get the instructions to install it here: [Install Docker](https://docs.docker.com/v17.09/engine/installation/)

NOTE: the muzzle print image must be in the `/database` folder

## Credits

Special thanks to:
- https://github.com/Utkarsh-Deshmukh/Fingerprint-Enhancement-Python for providing a library used to enhance the muzzle print image.
- https://github.com/kjanko/python-fingerprint-recognition for providing a library used to recognition the muzzle print image with SKimage and OpenCV.

## Author

- maleerat.m@itd.kmutnb.ac.th
- chalermpong.int@biotec.or.th
