#!/urs/local/bin/python
# Developed by Chalermpong Intarat
# On Wednesday, November 4, 2020

# RIDGEORIENT - Estimates the local orientation of ridges in a muzzle print image.

# Usage:	[orientim, reliability, coherence] = ridgeorientation(im, gradientsigmna,...
#												blockdigma, ...
#												orientsmoothsigma)

# Arguments:	im 					- A normalised input image.
#				gradientsigmna		- Sigma of the derivative of Gaussian
# 								  	  used to compute image gradients.
#				blockdigma			- Sigma of the Gaussian weighting used to
# 								  	  sum the gradient moments.
#				orientsmoothsigma	- Sigma of the Gaussian used to smooth
# 									  the final orientation vector field.
# 									  Optional: if ommitted it defaults to 0

# returns:		Orientim 			- The orientation image in radians.
# 									  Orientation values are +ve clockwise
# 									  and give the direction *along* The
# 									  ridges.
#				reliability			- Measure of the reliability of the
# 									  orientation measure. This is a value
# 									  between 0 and 1. I think a value above
# 									  about 0.5 can be considered 'reliable'.
# 									  reliability = 1 - Imin./(Imax+.001);
#				coherence			- A measure of the degree to which the local
#									 area is oriented.
#									 coherence = ((Imax-Imin)./(Imax+Imin)).^2;

# With a muzzle print image at a 'standard' resolution of 500dpi suggested
# parameter values might be:
#	[orientim, reliability] = ridgeorient(im, 1, 3, 3);

# See also: RIDGESEGMENT, RIDGEFREQ, RIDGEFILTER

import numpy as np 
import cv2
from scipy import ndimage
from scipy import signal

def ridge_orient(im, gradientsigmna, blockdigma, orientsmoothsigma):
	rows,cols = im.shape;
	# Calculate image gradients.
	sze = np.fix(6*gradientsigmna);
	if np.remainder(sze,2) == 0:
		sze = sze+1;

	gauss = cv2.getGaussianKernel(np.int(sze), gradientsigmna);
	f = gauss * gauss.T;

	fy,fx = np.gradient(f);		# Gradient of Gaussian.

	#Gx = ndimage.convolve(np.double(im),fx);
	#Gy = ndimage.convolve(np.double(im),fy);

	Gx = signal.convolve2d(im,fx,mode='same');
	Gy = signal.convolve2d(im,fy,mode='same');

	Gxx = np.power(Gx,2);
	Gyy = np.power(Gy,2);
	Gxy = Gx*Gy;

	# Now smooth the covariance data to perform a weighted summation of the data.

	sze = np.fix(6*blockdigma);

	gauss = cv2.getGaussianKernel(np.int(sze),blockdigma);
	f = gauss * gauss.T;

	Gxx = ndimage.convolve(Gxx,f);
	Gyy = ndimage.convolve(Gyy,f);
	Gxy = 2*ndimage.convolve(Gxy,f);

	# Analytic solution of principal direction.
	denom = np.sqrt(np.power(Gxy,2) + np.power((Gxx - Gyy),2)) + np.finfo(float).eps;

	sin2theta = Gxy/denom;			# Sine and cosin of doubled angles.
	cos2theta = (Gxx-Gyy)/denom;

	if orientsmoothsigma:
		sze = np.fix(6*orientsmoothsigma);
		if np.remainder(sze,2) == 0:
			sze = sze+1;
		gauss = cv2.getGaussianKernel(np.int(sze),orientsmoothsigma);
		f = gauss * gauss.T;
		cos2theta = ndimage.convolve(cos2theta,f); # Smoothed sine and cosine of
		sin2theta = ndimage.convolve(sin2theta,f); # doubled angles.

	orientim = np.pi/2 + np.arctan2(sin2theta,cos2theta)/2;
	return(orientim);