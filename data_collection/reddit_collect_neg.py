import sys

from reddit_collect import run_script

examples_limit = None
if len(sys.argv) == 2:
	examples_limit = int(sys.argv[1])

run_script(collect_pos=False, examples_limit=examples_limit)