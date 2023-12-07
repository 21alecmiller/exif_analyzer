#!/usr/bin/python3

import subprocess
import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def make_menu():
	while True:
		execute("clear", False)
		print("Main Menu:")
		print("\t1 - Add Filtering Tags")
		print("\t2 - View Timeline")
		print("\t3 - Generate Report")
		print("\t4 - Quit Program\n")

		process = input("Enter your selection: ")
		
		if process == "4":
			break		
		elif process == "1":
			filter_tags()
			time.sleep(2)
		elif process == "2":
			generate_timeline()
			time.sleep(2)
		elif process == "3":
			generate_report()
			time.sleep(2)
		else:
			print("Invalid selection, input 1-4")
			time.sleep(2)

def execute(cmd, output):
	if output:
		res = subprocess.check_output(cmd, shell=True).decode().strip()
		return res
	else:
		subprocess.run(cmd, shell=True)

def filter_tags():
	print("Currently selected tags are: ", tag_list)
	tags = input("Input space-separated tags or ENTER to cancel: ").split()
	for t in tags:
		tag_list.append(t)

def generate_timeline():
	start = ''
	end = ''
	while True:
		time_tag = input("Access, Modify, or Change time? (pick one): ")
		if time_tag == "Access":
			time_tag = "FileAccessDate"
			break
		elif time_tag == "Modify":
			time_tag = "FileModifyDate"
			break
		elif time_tag == "Change":
			time_tag = "FileInodeChangeDate"
			break
		else:
			print("Invalid selection, try again")
			time.sleep(1)			
	filename = input("Would you like to save the timeline? \n\tEnter filename or press ENTER: ")

	date_list = get_dates(time_tag)
	label_list = make_labels(date_list)
	draw(start, end, date_list, label_list)

	if filename:
		plt.savefig(filename)
		print("Timeline saved")
	plt.show()


def get_dates(type):
	date_format = '%Y:%m:%d %H:%M:%S'
	date_cmd = "exiftool -s * | grep " + type + " | awk -F ' : ' '{print $2}'"
	dates = execute(date_cmd, True)
	dates = dates.split('\n')
	for i in range(len(dates)):
		dates[i] = dates[i].split('-')[0]
		dates[i] = datetime.strptime(dates[i], date_format)
	return dates

def make_labels(dates):
	file_cmd = "exiftool -s * | grep ^FileName | awk -F ' : ' '{print $2}'"
	labels = execute(file_cmd, True)
	labels = labels.split('\n')
	labels = ['{0:%Y:%m:%d %H:%M:%S}:\n{1}'.format(d, l) for l, d in zip(labels, dates)]
	return labels

def draw(min, max, dates, labels):
	fig, ax = plt.subplots(figsize=(6, 8), constrained_layout=True)
	_ = ax.set_xlim(-20, 20)
	_ = ax.axvline(0, ymin=0.05, ymax=0.95, zorder=1)

	_ = ax.scatter(np.zeros(len(dates)), dates, s=120, c='green', zorder=2)
	_ = ax.scatter(np.zeros(len(dates)), dates, s=40, c='limegreen', zorder=3)

	label_offsets = np.repeat(2.0, len(dates))
	label_offsets[1::2] = -2.0
	for i, (l, d) in enumerate(zip(labels, dates)):
		align = 'right'
		if i % 2 == 0:
			align = 'left'
		_ = ax.text(label_offsets[i], d, l, ha=align, fontsize=10)

	stems = np.repeat(2.0, len(dates))
	stems[1::2] *= -1.0
	x = ax.hlines(dates, 0, stems, color='green')

	for spine in ["left", "top", "right", "bottom"]:
		_ = ax.spines[spine].set_visible(False)
	_ = ax.set_xticks([])
	_ = ax.set_yticks([])
	
	_ = ax.set_title('Case Timeline', fontweight="bold", fontsize=16, color='green')

def generate_report():
	filename = input("Give a filename for the report: ")
	header = 'echo "ExifTool Report for $(pwd)" > ' + filename
	execute(header, False)

	cmd = "exiftool"
	for t in tag_list:
		cmd += " -" + t
	cmd += " * >> " + filename
	execute(cmd, False)

	print("Report generated")
	time.sleep(2)

if __name__ == "__main__":
	tag_list = []
	make_menu()
	print("\nQuitting Program...\n")
