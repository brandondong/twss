import os
import sys

if len(sys.argv) != 2:
	print("usage: resort.py <directory>")
else:
	# Assume the directory contains text files in the expected order format.
	directory = sys.argv[1]
	# Get a sorted list of the directory's files based on their number.
	files = os.listdir(directory)
	files.sort(key=lambda s : int(s[:-4]))
	num_files = len(files)
	print(f"Number of files: {num_files}")
	
	for i in range(num_files):
		expected_filename = f"{i}.txt"
		current_filename = files[i]
		if current_filename != expected_filename:
			print(f"Renaming {current_filename} -> {expected_filename}.")
			full_src = os.path.join(directory, current_filename)
			full_dst = os.path.join(directory, expected_filename)
			
			# If the filenames differ, it is because the actual number is ahead of expected.
			# The rename cannot clash with an existing file inductively.
			os.rename(full_src, full_dst)