#!python3

import requests
from html.parser import HTMLParser
from urllib import parse

class LinkParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.links = []

	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			for (key, value) in attrs:
				if key == 'href':
					newUrl = parse.urljoin(self.baseUrl, value)
					if newUrl in self.baseUrl or '?' in value:
						continue
					testNewUrl = requests.get(newUrl)
					if testNewUrl.status_code != 404 and \
							testNewUrl.headers['content-type'].split(";")[0] == 'application/pdf':
						self.links = self.links + [newUrl]
					elif testNewUrl.status_code != 404 and \
							testNewUrl.headers['content-type'].split(";")[0] == 'text/html':
						print ("HTML: ",newUrl)
						self.getLink(newUrl)
	def getLink(self, url):
		self.baseUrl = url
		# while self.htmlLinks != []:
		# 	visiting = self.htmlLinks[0]
		# 	self.htmlLinks = self.htmlLinks[1:]
		visiting = url
		response = requests.get(visiting)
		if response.headers['content-type'].split(";")[0] == 'text/html':
			htmlString = response.content.decode("utf-8")
			self.feed(htmlString)
		

def tryRequests():
	parser = LinkParser()
	url = "http://clgiles.ist.psu.edu/IST441/materials/"
	parser.getLink(url)
	#download(parser)
	#print(parser.links)

if __name__ == "__main__":
	tryRequests()