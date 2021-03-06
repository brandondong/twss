import re

LENNY_FACE = "( ͡° ͜ʖ ͡°)"
TWSS_LETTERS_TEST = "thatswhatshesaid"

QUOTE_FORMAT = re.compile(r">(.+)\n+(.+)")
NON_ALPHANUMERIC = re.compile(r"[^\w]|_")

# Two different ways of representing bold text.
BOLD_1 = re.compile(r"\*\*(.+)\*\*")
BOLD_2 = re.compile(r"__(.+)__")

NONESCAPED_UNDERSCORE = re.compile(r"(^|[^\\])_")
NONESCAPED_ASTERIX = re.compile(r"(^|[^\\])\*")

NONESCAPED_DOUBLE_UNDERSCORE = re.compile(r"(^|[^\\])__")
NONESCAPED_DOUBLE_ASTERIX = re.compile(r"(^|[^\\])\*\*")

SUPERSCRIPT = re.compile(r"([^\\])\^")

STRIKETHROUGH_STARTING_SPACE = re.compile(r" ~~.+~~")
STRIKETHROUGH_ELSE = re.compile(r"(^|[^\\])~~.+~~ ?")

ESCAPE_SEQUENCE = re.compile(r"(^|[^\\])\\")

def match_twss(s):
	"""Matches for the delivery of a 'That's what she said' punchline against the comment text.

    Returns None if punchline is not present.
    Otherwise, returns the text that the punchline is referring to.
	If that text is not in this comment, an empty string is returned instead.
    """
	
	# Check for a delivery in the form a simple reply.
	if _is_punchline(s):
		return ""
	# Look for comment text in the format of [single line quote]?[newlines][twss | lenny face].
	matched = QUOTE_FORMAT.match(s)
	if matched == None:
		return None
	# Extract and check the potential punchline.
	punchline = matched.group(2)
	if not _is_punchline(punchline):
		return None
	joke = matched.group(1)
	# Since quoting requires copying and pasting plaintext, any bolding can be assumed to be emphasizing the actual joke.
	return strip_formatting(_extract_possible_bold(joke))
	
def strip_formatting(s):
	"""Strips the comment text of any Reddit formatting. Assumed not to have quotes."""
	
	# Handle bolded text.
	s = NONESCAPED_DOUBLE_UNDERSCORE.sub(r"\1", s)
	s = NONESCAPED_DOUBLE_ASTERIX.sub(r"\1", s)
	
	# Handle italicized text.
	s = NONESCAPED_UNDERSCORE.sub(r"\1", s)
	s = NONESCAPED_ASTERIX.sub(r"\1", s)
	
	# Handle superscripts.
	s = SUPERSCRIPT.sub(r"\1 ", s)
	
	# Handle strikethroughs.
	s = STRIKETHROUGH_STARTING_SPACE.sub("", s)
	s = STRIKETHROUGH_ELSE.sub(r"\1", s)
	
	# Remove the escapes now that all formatting is removed.
	s = ESCAPE_SEQUENCE.sub(r"\1", s)
	return s.strip()

def _is_punchline(s):
	return _is_lenny(s) or _is_twss(s)
	
def _is_twss(s):
	# Normalize by stripping non-alphanumeric characters and lowercasing.
	normalized = NON_ALPHANUMERIC.sub("", s).lower()
	return normalized == TWSS_LETTERS_TEST
	
def _is_lenny(s):
	return s.strip() == LENNY_FACE
	
def _extract_possible_bold(s):
	matched = BOLD_1.search(s)
	if matched:
		return matched.group(1)
	matched = BOLD_2.search(s)
	if matched:
		return matched.group(1)
	return s