import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import matplotlib.dates as mdates 
import csv
import glob





files = [ 'likes-200907-090929.csv', 'dau-by-mau-200907-090755.csv', 'signups-200907-091105.csv', 'visits-200907-091249.csv', 'daily-engaged-users-200907-090907.csv', 'topics-200907-091124.csv', 'new-contributors-200907-091010.csv', 'posts-200907-091037.csv']

# not plotting for now...
# 'trust-level-growth-200907-091152.csv',
# 'trending-search-200907-091229.csv',


glued_data = pd.DataFrame()
for file_name in glob.glob('*.csv'):
	files.append(file_name)

file_v = []
perc_change_v = []

for i in range(len(files)):		# for each file

	filename = files[i]

	df = pd.read_csv(filename)
	cols = df.columns

	# count_v = []
	# for j in range(len(cols) - 1):			# for each column of data
	# 	count_v.append(df[cols[j+1]])

	count = df[cols[1]]
	day = df['Day']

	# smoothing with a running average in one line using a convolution
	n_ave = 10
	count_smoothed = np.convolve(np.asarray(count), np.ones(n_ave)/n_ave, mode='same')

	count_smoothed = np.ndarray.tolist(count_smoothed)

	# -------------------------- Set dates time-filtering ------------------------

	# start_date = '2018/11/10 18:56:36'
	start_date = '2020-06-01'
	end_date = '2020-09-01'


	start_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%d')
	end_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d')

	trial_day = []
	trial_day_rel = []
	trial_count = []
	trial_count_smoothed = []


	day_rel = 1

	for j in range(len(day)):

		if (datetime.datetime.strptime(day[j], '%Y-%m-%d') >= start_datetime \
			and datetime.datetime.strptime(day[j], '%Y-%m-%d') <= end_datetime):
				trial_day.append(datetime.datetime.strptime(day[j], '%Y-%m-%d'))
				trial_count.append(count[j])
				trial_count_smoothed.append(count_smoothed[j])
				trial_day_rel.append(day_rel)

		day_rel = day_rel + 1


	# Linear regression 
	m,b = np.polyfit(np.asarray(trial_day_rel), np.asarray(trial_count), 1)
	x = np.asarray(trial_day_rel)
	y = m*x + b
	# plt.plot(x,y)
	# plt.show()


	print(filename)
	perc_change = y[len(y)-1]/y[0]
	print(perc_change)
	# plt.plot(np.asarray(trial_day_rel), np.asarray(trial_count), 'yo', np.asarray(trial_day_rel), m*np.asarray(trial_day_rel)+b, '--k') 
	# plt.show() 
	file_v.append(filename)
	perc_change_v.append(perc_change)

	plt.plot(trial_day,trial_count, color="blue")
	plt.plot(trial_day,trial_count_smoothed, label='10 day MA', color="red")


	plt.plot(trial_day,y, label='linear regression', color="black",linestyle='dashed')
	# plt.show()

	plt.xlabel('date', size=12)
	plt.ylabel('Likes',size=12)
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
	# plt.gca().xaxis.set_major_locator(mdates.DayLocator())

	plt.gcf().autofmt_xdate()
	plt.legend()

	plt.savefig(filename+'.png')
	plt.close()
	# plt.show()
	# plt.pause(0.001)
	# input("Press [enter] to continue.")


