"""
import vk
import json

EVGENY_ACCESS_TOKEN='a047f68667b928a2d3f788041cb297b5c5bf4da5e9aab11ce63084fa9a6d34dfe6d6419c989c2eb1cd8a9'
"""
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import json
import logging
import cgi

import sys

PORT = 80

class ServerHandler(BaseHTTPRequestHandler):

	def do_POST(self):
		logging.warning("======= POST STARTED =======\n")
		logging.warning(self.headers)
		content_len = int(self.headers.getheader('content-length', 0))
		post_body = self.rfile.read(content_len)
		logging.warning("======= POST VALUES =======\n")
		#decoded = json.loads(post_body)
		#logging.warning(decoded["username"])
		logging.warning(post_body)
		logging.warning("\n")

if __name__ == '__main__':
	server = HTTPServer(('localhost', 80), ServerHandler)
	server.serve_forever()