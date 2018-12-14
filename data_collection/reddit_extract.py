import praw

reddit = praw.Reddit('comment_parse_bot', user_agent='comment_parse_bot user agent')
print(reddit.read_only)