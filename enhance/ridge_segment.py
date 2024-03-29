#!/urs/local/bin/python
# Developed by Chalermpong Intarat, Nov 4, 2020
# NBT, NSTDA chalermpong.int@biotec.or.th

# RIDGESEGMENT - Normalises muzzle print image and segment ridge region.

# Function identifies ridge regions of a muzzle print image and return a
# mask identifying this region. It also normalises the intesity values of
# the image so that the ridge regions have zero mean, unit standard
# deviation.

# This function breaks the image up into blocks of size blksze x blksze and
# evaluates the standard deviation in each region. If the standard
# deviation is above the threshold it is deemed part of the muzzle print image.
# Note that the image is normalised to have zero mean, unit standard
# deviation prior to performing this process so that the threshold you
# specify is relative to a unit standard deviation.

# Usage:	[normin, mask, maskind] = ridgesegment(im, blksze, thresh)

# Arguments:	im 		- Muzzle print image to be segmented.
#				blksze	- Block size over which the standard
#						  deviation is determined (try aq value of 16).
#				thresh 	- Threshold of determined deviation to decide if a
#						  block is a ridge region (Try a value 0.1 - 0.2)

# Returns:		normim	- Image where the ridge regions are renormalised to
#						  have zero mean, unit standard deviation.
#				mask 	- Mask indicating ridge-like regions of the image,
#						  0 for non ridge regions, 1 for ridge regions.
#				maskind	- Vector of indices of locations within the mask.

# Suggested values for a 500dp1 muzzle print image:
# 	[normin, mask, maskind] = ridgesegment(im, 16, 0.1)

# See also: RIDGEORIENT, RIDGEFREQ, RIDGEFILTER

import numpy as np 

def normalise(img,mean,std):
	normed = (img - np.mean(img))/(np.std(img));
	return(normed)

def ridge_segment(im,blksze,thresh):
	
	rows,cols = im.shape;

	im = normalise(im,0,1);		# Normalise to get zero mean and unit standard deviation.

	new_rows = np.int(blksze * np.ceil((np.float(rows))/(np.float(blksze))))
	new_cols = np.int(blksze * np.ceil((np.float(cols))/(np.float(blksze))))

	padded_img = np.zeros((new_rows,new_cols));
	stddevim = np.zeros((new_rows,new_cols));

	padded_img[0:rows][:,0:cols] = im;

	for i in range(0,new_rows, blksze):
		for j in range(0, new_cols, blksze):
			block = padded_img[i:i+blksze][:,j:j+blksze];

			stddevim[i:i+blksze][:,j:j+blksze] = np.std(block)*np.ones(block.shape)

	stddevim = stddevim[0:rows][:,0:cols]

	mask = stddevim > thresh;

	mean_val = np.mean(im[mask]);

	std_val = np.std(im[mask]);

	normim = (im - mean_val)/(std_val);

	return(normim,mask)
