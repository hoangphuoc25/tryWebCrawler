#!python3
import sys
import os
import requests
from html.parser import HTMLParser
from urllib import parse

class LinkParser(HTMLParser):
	def __init__(self, url):
		HTMLParser.__init__(self)
		self.links = []
		self.baseUrl = url
		self.htmlLinks = [url]

	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			for (key, value) in attrs:
				if key == 'href':
					newUrl = parse.urljoin(self.baseUrl, value)
					if newUrl in self.baseUrl or '?' in value:
						continue
					testNewUrl = requests.get(newUrl)
					if testNewUrl.status_code == 200 and \
							testNewUrl.headers['content-type'].split(";")[0] != 'text/html':
						self.links.append(newUrl)
					elif testNewUrl.status_code != 404 and \
							testNewUrl.headers['content-type'].split(";")[0] == 'text/html':
						self.htmlLinks.append(newUrl)
	def getLink(self):
		while self.htmlLinks != []:
			visiting = self.htmlLinks[0]
			print("VISITING: ",visiting)
			self.htmlLinks = self.htmlLinks[1:]
			response = requests.get(visiting)
			if response.headers['content-type'].split(";")[0] == 'text/html':
				htmlString = response.content.decode("utf-8")
				self.baseUrl = visiting
				self.feed(htmlString)
def fileName(url):
	split = url.split('/')[-1]
	return split
def download(parser, destination):
	for x in parser.links:
		# filePath = os.path.join(destination, fileName(x))
		filePath = destination + fileName(x)
		dir = os.path.dirname(filePath)
		try:
			os.stat(dir)
		except:
			os.mkdir(dir)
		f = open(filePath, 'wb')
		r = requests.get(x)
		f.write(r.content)
		f.close()

def Requests(url, destination):
	parser = LinkParser(url)
	parser.getLink()
	download(parser, destination)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Enter path to search for file and destination folder")
	Requests(sys.argv[1], sys.argv[2])