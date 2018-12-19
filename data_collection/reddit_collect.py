import os
import signal
import sys

import praw

import reddit_comment_parse as rcp

BOT_ID = "comment_parse_bot"
BOT_USER_AGENT = BOT_ID + " user agent"

TRAINING_DATA_PATH = "../training_data/"
TRAINING_DATA_POS_PATH = os.path.join(TRAINING_DATA_PATH, "pos/")
TRAINING_DATA_NEG_PATH = os.path.join(TRAINING_DATA_PATH, "neg/")

def run_script(collect_pos, examples_limit=None):
	data_path = TRAINING_DATA_POS_PATH if collect_pos else TRAINING_DATA_NEG_PATH
	should_quit = False

	def shutdown_handler(sig, frame):
		# Set the flag to stop the comment retrieval.
		should_quit = True
			
	# Register a SIGINT handler to shutdown safely.
	signal.signal(signal.SIGINT, shutdown_handler)

	# Ensure the training data folders have been created.
	os.makedirs(data_path, exist_ok=True)

	# Populate a set of existing lowercased data to check for duplicates.
	existing_data = set()
	# And keep track of the file number to start with.
	starting_filenum = 0

	for f in os.listdir(data_path):
		filename = os.path.join(data_path, f)
		# Add contents to the set.
		with open(filename, "r") as text_file:
			existing_data.add(text_file.read().lower())
		# Update the starting file number with the highest number encountered so far.
		starting_filenum = max(starting_filenum, int(f[:-4]) + 1)

	print(f"Number of existing training examples: {len(existing_data)}")

	reddit = praw.Reddit(BOT_ID, user_agent=BOT_USER_AGENT)

	comment = reddit.comment("e8npbse")
	print(comment.score)
	print(comment.permalink)
	print(rcp.match_twss(comment.body))

	with open(f"{data_path}{starting_filenum}.txt", "w") as text_file:
		print("test", file=text_file)

	print("Shut down gracefully.")