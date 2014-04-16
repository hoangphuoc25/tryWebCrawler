#!python3
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
			# print(attrs)
			for (key, value) in attrs:
				if key == 'href':
					newUrl = parse.urljoin(self.baseUrl, value)
					if newUrl in self.baseUrl or '?' in value:
						# print("DISCARDED: ",newUrl, "BECAUSE OF: ", self.baseUrl)
						continue
					testNewUrl = requests.get(newUrl)
					# print(newUrl)
					if testNewUrl.status_code == 200 and \
							testNewUrl.headers['content-type'].split(";")[0] != 'text/html':
						# print("PDF:    ",newUrl)
						self.links.append(newUrl)
					elif testNewUrl.status_code != 404 and \
							testNewUrl.headers['content-type'].split(";")[0] == 'text/html':
						#print ("HTML: ",newUrl)
						self.htmlLinks.append(newUrl)
						#print(self.htmlLinks)
	def getLink(self):
		while self.htmlLinks != []:
			visiting = self.htmlLinks[0]
			print("VISITING: ",visiting)
			self.htmlLinks = self.htmlLinks[1:]
			response = requests.get(visiting)
			if response.headers['content-type'].split(";")[0] == 'text/html':
				# print("Link OK, feeding into HTMLParser")
				htmlString = response.content.decode("utf-8")
				self.baseUrl = visiting
				self.feed(htmlString)
		# print(self.links)

def fileName(url):
	split = url.split('/')[-1]
	return split
def download(parser):
	for x in parser.links:
		# filePath = os.path.join("C:/OSS/download", fileName(x))
		filePath = "C:/OSS/download/" + fileName(x)
		print(filePath)
		f = open(filePath, 'wb')
		r = requests.get(x)
		f.write(r.content)
		f.close()

def tryRequests():
	url = "http://clgiles.ist.psu.edu/IST441/materials/"
	parser = LinkParser(url)
	parser.getLink()
	download(parser)
	#print(parser.links)

if __name__ == "__main__":
	tryRequests()