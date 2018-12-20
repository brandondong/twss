import os
import signal
import sys

import praw
from praw.models import MoreComments

import reddit_comment_parse as rcp

BOT_ID = "comment_parse_bot"
BOT_USER_AGENT = BOT_ID + " user agent"

TRAINING_DATA_PATH = "../training_data/"
TRAINING_DATA_POS_PATH = os.path.join(TRAINING_DATA_PATH, "pos/")
TRAINING_DATA_NEG_PATH = os.path.join(TRAINING_DATA_PATH, "neg/")

TRAINING_SUBREDDIT = "all"

SCORING_THRESHOLD = 1
REDDIT_PREFIX = "https://www.reddit.com"

def run_script(collect_pos, examples_limit=None):
	"""Initiates a script to start crawling through Reddit for either positive or negative training examples."""
	
	data_path = TRAINING_DATA_POS_PATH if collect_pos else TRAINING_DATA_NEG_PATH
	# Flag to stop the comment retrieval.
	should_quit = False

	def shutdown_handler(sig, frame):
		nonlocal should_quit
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

	print(f"Number of existing training examples: {len(existing_data)}.\n")

	reddit = praw.Reddit(BOT_ID, user_agent=BOT_USER_AGENT)
	
	# TODO remove this.
	submission = reddit.submission("9sc0qj")
	_walk_comment_forest(submission.comments, None, submission)
	
	for submission in reddit.subreddit(TRAINING_SUBREDDIT).hot(limit=None):
		if should_quit:
			break
		
		# Recursively explore already fetched comments.
		_walk_comment_forest(submission.comments, None, submission)
		
	print("Shut down gracefully.")
	
def _walk_comment_forest(tree, parent, submission):
	for comment in tree:
		if not isinstance(comment, MoreComments):
			_process_comment(comment, parent, submission)
			
			if hasattr(comment, "replies"):
				_walk_comment_forest(comment.replies, comment, submission)
			
def _process_comment(comment, parent, submission):
	# Ignore downvoted comments.
	if comment.score < SCORING_THRESHOLD:
		return
	result = rcp.match_twss(comment.body)
	if result == None:
		return
	if result == "":
		if parent == None:
			# Since this is not a reply, the punchline would likely be referring to the submission title.
			joke = rcp.strip_formatting(submission.title)
		else:
			joke = rcp.strip_formatting(parent.body)
	else:
		joke = result
	print(f"Found joke: [{joke}]")
	print(f"{REDDIT_PREFIX}{comment.permalink}")