#!/urs/local/bin/python
# Adapted by Chalermpong Intarat, Nov 4, 2020
# NBT, NSTDA chalermpong.int@biotec.or.th

# RIDGEFREQ - Calculate a ridge frequency image.

# Function to estimate the muzzle print image ridge frequency across a
# muzzle print image. This is done by considering blocks of the image and
# determining a ridgecount within each block by a call to FREQEST.

# Usage:	[freqim, medianfreq] = ridgefreq(im, mask, orientim, blksze, windsze, ...
#									minWaveLength, maxWaveLength)

# Argukents:	im 								- Image to be processed.
#				mask							- Mask defining ridge regions (obtained from RIDGESEGMENT)
#				orientim						- Ridge orientation image (obtained from RIDGEORIENT)
#				blksze							- Size of image block to use (say 32)
#				windsze							- Window length used to identify peaks. This should be
#												  an odd integer, say 3 or 5.
#				minWaveLength, maxWaveLength	- Minimum and maximum ridge wavelengths, in pixels, considered acceptable.

# Returns:		freqim		- An image the same size as im with values set to
#							  the estimate ridge spatial frequency within each
#							  image block. If a ridge frequency cannot be
#							  found within a block, or cannot be found within the
#							  limits set by min amd max Wavelength freqim is set
#							  to zeros within that block.
#				medianfreq	- Median frequency value evaluated over all the
#							  valid reqions of the image.

# Suggested parameters for a 500dpi muzzle print image
#	[freqim, medianfreq] = ridgefreq(im,orientim, 32, 5, 5, 15);

# See also: RIDGEORIENT, FREQEST, RIDGESEGMENT

import numpy as np 
# import math
# import scipy.ndimage
from . frequest import frequest

def ridge_freq(im, mask, orient, blksze, windsze, minWaveLength, maxWaveLength):
	rows,cols = im.shape;
	freq = np.zeros((rows,cols));

	for r in range(0,rows-blksze,blksze):
		for c in range(0,cols-blksze,blksze):
			blkim = im[r:r+blksze][:,c:c+blksze];
			blkor = orient[r:r+blksze][:,c:c+blksze];

			freq[r:r+blksze][:,c:c+blksze] = frequest(blkim,blkor,windsze,minWaveLength,maxWaveLength);

	freq = freq*mask;
	freq_1d = np.reshape(freq,(1,rows*cols));
	ind = np.where(freq_1d>0);

	ind = np.array(ind);
	ind = ind[1,:];

	non_zero_elems_in_freq = freq_1d[0][ind];

	meanfreq = np.mean(non_zero_elems_in_freq);
	medianfreq = np.median(non_zero_elems_in_freq);		# Does not work properly.
	return(freq,meanfreq)
