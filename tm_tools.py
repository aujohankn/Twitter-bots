#A modified version of the file taken from github repository https://github.com/maxcw/time-maps

import numpy as np
import matplotlib.pylab as plt

import scipy.ndimage as ndi
import datetime as dt

# Converts a twitter time string to a datetime object
def get_dt(t): 
	
	my_datetime = dt.datetime.strptime(t,"%Y-%m-%d %H:%M:%S")
	
	return my_datetime

# Plot heated time map. Nothing is returned
def make_heated_time_map(sep_array, Nside, width): 

	print('generating heated time map ...')
	
	# choose points within specified range
	indices=range(sep_array.shape[0]) # all time separations

	x_pts = np.log(sep_array[indices,0])
	y_pts = np.log(sep_array[indices,1])

	min_val = np.min([np.min(x_pts), np.min(y_pts)])
	
	x_pts = x_pts - min_val
	y_pts = y_pts - min_val
	
	max_val = np.max([np.max(x_pts), np.max(y_pts)])
	
	x_pts *= (Nside-1)/max_val
	y_pts *= (Nside-1)/max_val
	
	img=np.zeros((Nside,Nside))

	for i in range(len(x_pts)):
		img[int(x_pts[i]),int(y_pts[i])] +=1

	img = ndi.gaussian_filter(img,width) # apply Gaussian filter
	img = np.sqrt(img) # taking the square root makes the lower values more visible
	img=np.transpose(img) # needed so the orientation is the same as scatterplot

	## change font, which can also now accept latex: http://matplotlib.org/users/usetex.html
	plt.rc('text',usetex=False)
	plt.rc('font',family='serif')

	plt.imshow(img, origin='lower')
	
	## create custom tick marks. Calculate positions of tick marks on the transformed log scale of the image array
	plt.minorticks_off()
	

	my_max = np.max([np.max(sep_array[indices,0]), np.max(sep_array[indices,1])])
	my_min = np.max([np.min(sep_array[indices,0]), np.min(sep_array[indices,1])])

	pure_ticks = np.array([1e-3,1,10,60,60*10,2*3600,1*24*3600, 7*24*3600]) 
	# where the tick marks will be placed, in units of seconds. An additional value will be appended to the end for the max
	labels = ['1 msec','1 sec','10 sec','1 min','10 min','2 hr','1 day','1 week']  # tick labels
	
	index_lower=np.min(np.nonzero(pure_ticks >= my_min))
	
	# try:
	# 	index_lower=np.min(np.nonzero(pure_ticks >= my_min))
	# except ValueError as e:
	# 	print(e)
	# 	return None

	# index of minimum tick that is greater than or equal to the smallest time interval. This will be the first tick with a non-blank label

	index_upper=np.max(np.nonzero(pure_ticks <= my_max))
	# similar to index_lower, but for upperbound
	
	ticks = pure_ticks[index_lower: index_upper + 1]
	ticks = np.log(np.hstack((my_min, ticks, my_max ))) # append values to beginning and end in order to specify the limits
	ticks = ticks - min_val
	ticks *= (Nside-1)/(max_val)
	
	labels= np.hstack(('',labels[index_lower:index_upper + 1],'')) # append blank labels to beginning and end
	plt.xticks(ticks, labels,fontsize=14, ha='right', rotation=45, rotation_mode='anchor')
	plt.yticks(ticks, labels,fontsize=14)
	plt.xlabel('Time Before Tweet',fontsize=14)
	plt.ylabel('Time After Tweet' ,fontsize=14)
	plt.title("Heated Time Map")
	plt.tight_layout()
	plt.show()

	return None

def analyze_tweet_times(name_to_get, all_tweets): 
	# plots a heated or normal time map, and return lists of time quantities
	# input:
	# name_to_get: twitter handle, not including @
	# all tweets: list of tweets. Each tweet is a neted dictionary
	# HEAT: Boolean; 1 for a heated time map, 0 for a normal scatterplot
	#
	# output:
	# times: list of datetimes corresponding to each tweet
	# times_tot_mins: list giving the time elapsed since midnight for each tweet
	# sep_array: array containing xy coordinates of the time map points
	
	all_tweets = all_tweets[::-1] # reverse order so that most recent tweets are at the end
    
	times=[get_dt(tweet) for tweet in all_tweets]
	timezone_shift=dt.timedelta(hours=4) # times are in GMT. Convert to eastern time.
	times = [time-timezone_shift for time in times]
	
	times_tot_mins = 24*60 - (60*np.array([t.hour for t in times]) + np.array([t.minute for t in times])) # 24*60 - number of minutes since midnight

	seps=np.array([(times[i]-times[i-1]).total_seconds() for i in range(1,len(times))])
	seps[seps==0]=1 # convert zero second separations to 1-second separations

	sep_array=np.zeros((len(seps)-1,2)) # 1st column: x-coords, 2nd column: y-coords
	sep_array[:,0]=seps[:-1]
	sep_array[:,1]=seps[1:]

	Nside=4*256 # number of pixels along the x and y directions
	width=4 # the number of pixels that specifies the width of the Gaussians for the Gaussian filter
	make_heated_time_map(sep_array, Nside, width)

	return times,times_tot_mins,sep_array