import signal
import sys

import praw

import reddit_comment_parse as rcp

BOT_ID = "comment_parse_bot"
BOT_USER_AGENT = BOT_ID + " user agent"

should_quit = False

def shutdown_handler(sig, frame):
	# Set the flag to stop the comment retrieval.
	should_quit = True
		
# Register a SIGINT handler to shutdown safely.
signal.signal(signal.SIGINT, shutdown_handler)

reddit = praw.Reddit(BOT_ID, user_agent=BOT_USER_AGENT)

comment = reddit.comment("e8npbse")
print(comment.score)
print(comment.permalink)
print(rcp.match_twss(comment.body))

print("Shutting down gracefully...")