#!/urs/local/bin/python
# Developed by Chalermpong Intarat, Nov 4, 2020
# NBT, NSTDA chalermpong.int@biotec.or.th

# Reference:
#
# Hong, L., Wan, Y., and Jain, A. K. Fingerprint image enhancement:
# Algorithm and performance evalutaion. IEEE Transactions on Pattern
# Anlysis and machine Intelligence 20, 8 (1998), 777 789.
#
# Peter Kovesi
# School of Computer Science & Software Engineering
# The University of Western Australia
# pk at csse uwa edu au
# http://www.csse.uwa.edu.au/~pk

from .ridge_segment import ridge_segment
from .ridge_orient import ridge_orient
from .ridge_freq import ridge_freq
from .ridge_filter import ridge_filter

def image_enhance(img):
	blksze = 16;
	thresh = 0.1;
	normim,mask = ridge_segment(img,blksze,thresh);		# Normalise the image and find a ROI.

	gradientsigma = 1;
	blocksigma = 7;
	orientsmoothsigma = 7;
	orientim = ridge_orient(normim, gradientsigma, blocksigma, orientsmoothsigma);		# Find orientation of every pixel.

	blksze = 38;
	windsze = 5;
	minWaveLength = 5;
	maxWaveLength = 15;
	freq,medfreq = ridge_freq(normim, mask, orientim, blksze, windsze, minWaveLength, maxWaveLength);		# Find the overall frequency of ridges.

	freq = medfreq*mask;
	kx = 0.65;ky = 0.65;
	newim = ridge_filter(normim, orientim, freq, kx, ky);		# Create gabor filter and do the actual filtering.

	# th, bin_im = cv2.threshold(np.uint8(newim),0,255,cv2.THRES_BINARY);
	return(newim < -3)
