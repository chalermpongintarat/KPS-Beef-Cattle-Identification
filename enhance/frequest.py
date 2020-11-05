#!/urs/local/bin/python
# Developed by Chalermpong Intarat, Nov 4, 2020
# NBT, NSTDA chalermpong.int@biotec.or.th

# FREQUEST - Estimate muzzle print image ridge frequency within image block.

# Function to estimate the muzzle print image ridge frequency within a small block
# of a muzzle print image. This function is used by RIDGEFREQ.

# Usage:	freqim = frequest(im, orientim, windsze, minWaveLength, maxWaveLength)

# Arguments: 	im 								- Image to be processed.
#				orientim 						- Ridge orientation image of image block.
#				windsze							- Window length used to identity peaks. This should be
#							  an odd interger, say 3 or 5.
#				minWaveLength, maxWaveLength 	- Minimum and maximum ridge Wavelength, in pixels,
#												  considered acceptable.

# Returns:		freqim	- An image block the same size as im with all values
#			    set to the esimated ridge spatial frequency. If a
#			    ridge frequency cannot be found, or cannot be found
#			    within the limits set by min and max Wavelength
#			    freqim is set to zeros.

# Suggested parameters for a 500dpi muzzle print image
#	freqim = frequest(im, orientim, 5, 5, 15);

# See alsoL: RIDGEFREQ, RIDGEORIENT, RIDGESEGMENT

import numpy as np 
import math
import scipy.ndimage
# impory cv2
def frequest(im, orientim, windsze, minWaveLength, maxWaveLength):
	rows,cols = np.shape(im);

	# Find mean orientation within the block. This done by averaging the
	# sines and cosines of the doubled andles before reconstructing the
	# angle again. This avoids wraparound problems at the origin.

	cosorient = np.mean(np.cos(2*orientim));
	sinorient = np.mean(np.sin(2*orientim));
	orient = math.atan2(sinorient,cosorient)/2;

	# Rotate the image block so that the ridges are vertical.

	# ROT_mat = cv2.getRotationMatrix2D((cols/2, rows/2),orient/np.pi*180 + 90,1)
	# rotim = cv2.warpAffine(im,ROT_mat,(cols,rows))
	rotim = scipy.ndimage.rotate(im,orient/np.pi*180 + 90,axes=(1,0), reshape=False, order=3, mode='nearest');

	# Now crop the image so that the rotated image does not contain any
	# invalid reqions. This prevents the projecttion down the columns
	# from being mucked up.

	cropsze = int(np.fix(rows/np.sqrt(2)));
	offset = int(np.fix((rows-cropsze)/2));
	rotim = rotim[offset:offset+cropsze][:,offset:offset+cropsze];

	# Sum down the columns to get a projection of the grey values down
	# the ridges.

	proj = np.sum(rotim,axis = 0);
	dilation = scipy.ndimage.grey_dilation(proj, windsze,structure=np.ones(windsze));

	temp = np.abs(dilation - proj);

	peak_thres = 2;

	maxpts = (temp<peak_thres) & (proj > np.mean(proj));
	maxind = np.where(maxpts);

	rows_maxind,cols_maxind = np.shape(maxind);

	# Determine the spatail frequency of the ridges by divinding the
	# distance between the 1st and last peaks by the (No of peaks-1). If no
	# peaks are detected, or the wavelength is outside the allowed bounds,
	# the frequency image is set to 0.

	if(cols_maxind<2):
		freqim = np.zeros(im.shape);
	else:
		NoOfPeaks = cols_maxind;
		waveLength = (maxind[0][cols_maxind-1] - maxind[0][0])/(NoOfPeaks - 1);
		if waveLength>=minWaveLength and waveLength<=maxWaveLength:
			freqim = 1/np.double(waveLength) * np.ones(im.shape);
		else:
			freqim = np.zeros(im.shape);

	return(freqim);
