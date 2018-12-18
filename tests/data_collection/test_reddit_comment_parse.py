import unittest

import reddit_comment_parse as rcp

class TestRedditCommentParse(unittest.TestCase):
	def test_simple_matches(self):
		self.assertEqual(rcp.match_twss("That's what she said"), "")
		self.assertEqual(rcp.match_twss("( ͡° ͜ʖ ͡°)"), "")

	def test_simple_nonmatches(self):
		self.assertEqual(rcp.match_twss("Hello world!"), None)
		self.assertEqual(rcp.match_twss("python 3"), None)
		
	def test_simple_match_variations(self):
		self.assertEqual(rcp.match_twss("That's what she said!"), "")
		self.assertEqual(rcp.match_twss("THAT'S WHAT SHE SAID"), "")
		self.assertEqual(rcp.match_twss("thats what she said."), "")
		self.assertEqual(rcp.match_twss("thats_what_she_said"), "")
		self.assertEqual(rcp.match_twss("  ( ͡° ͜ʖ ͡°)"), "")
		self.assertEqual(rcp.match_twss("( ͡° ͜ʖ ͡°) "), "")
		self.assertEqual(rcp.match_twss("( ͡° ͜ʖ ͡°)\n"), "")
		
	def test_simple_false_positives(self):
		self.assertEqual(rcp.match_twss("That's what she said about Python."), None)
		self.assertEqual(rcp.match_twss("( ͡° ͜ʖ ͡°) Hello"), None)
		
	def test_quote_matches(self):
		self.assertEqual(rcp.match_twss(">That's huge!\n\nThat's what she said"), "That's huge!")
		self.assertEqual(rcp.match_twss("> It's hard\n\n( ͡° ͜ʖ ͡°)"), "It's hard")
		self.assertEqual(rcp.match_twss(">I'm exhausted    \n\n( ͡° ͜ʖ ͡°)"), "I'm exhausted")
		
	def test_rejects_multi_quotes(self):
		self.assertEqual(rcp.match_twss(">That's huge!\n\n>Another quote.\n\nThat's what she said"), None)
		
	def test_extracts_bold(self):
		self.assertEqual(rcp.match_twss(">__It's hard__ to sleep\n\nThat's what she said"), "It's hard")
		# A real comment: https://www.reddit.com/r/programming/comments/9sc0qj/deepcreampy_decensoring_hentai_with_deep_neural/e8npbse.
		test_comment = ">Image Inpainting for **Irregular Holes** Using Partial Convolutions\n\n( ͡° ͜ʖ ͡°)"
		self.assertEqual(rcp.match_twss(test_comment), "Irregular Holes")
		
	def test_match_strips_formatting(self):
		self.assertEqual(rcp.match_twss(">_It's_ hard\n\nThat's what she said"), "It's hard")
		self.assertEqual(rcp.match_twss(">It's *hard*\n\nThat's what she said"), "It's hard")
		
	def test_strip_italics(self):
		self.assertEqual(rcp.strip_formatting("_Hello_"), "Hello")
		self.assertEqual(rcp.strip_formatting("*Hello*"), "Hello")
		self.assertEqual(rcp.strip_formatting("Hello *World!*"), "Hello World!")
		self.assertEqual(rcp.strip_formatting("Hello _World!_"), "Hello World!")
		
	def test_strip_bold(self):
		self.assertEqual(rcp.strip_formatting("__Hello__"), "Hello")
		self.assertEqual(rcp.strip_formatting("**Hello**"), "Hello")
		self.assertEqual(rcp.strip_formatting("Hello **World!**"), "Hello World!")
		self.assertEqual(rcp.strip_formatting("Hello __World!__"), "Hello World!")
		
	def test_strip_superscript(self):
		self.assertEqual(rcp.strip_formatting("Hello^World!"), "Hello World!")
		
	def test_strip_strikethrough(self):
		self.assertEqual(rcp.strip_formatting("This is ~~not~~ a joke"), "This is a joke")
		self.assertEqual(rcp.strip_formatting("I should finish ~~quickly~~."), "I should finish.")
		self.assertEqual(rcp.strip_formatting("~~what's~~ updog"), "updog")
		self.assertEqual(rcp.strip_formatting("fire~~truck~~"), "fire")
		self.assertEqual(rcp.strip_formatting("~~fire~~truck"), "truck")
		
	def test_strip_escapes(self):
		self.assertEqual(rcp.strip_formatting("3 \* 4"), "3 * 4")
		self.assertEqual(rcp.strip_formatting(r"3\\4"), r"3\4")
		self.assertEqual(rcp.strip_formatting("3\^4"), "3^4")