import requests
import concurrent.futures
import time
urlpart="https://xkcd.com/"
matcher= "https://imgs.xkcd.com/comics/"


def get_image(url,name):
	file=requests.get(url)
	with open(name,"wb") as handle:
		handle.write(file.content)

def get_url(base_url):
	html=requests.get(base_url)
	strings=html.text
	string_list=strings.split()

	for words in string_list:
		if words.startswith(matcher):
			return words

def get_name(url):
	return url.split("/")[-1]

def image_retriever(base_url):
	url = get_url(base_url)
	name = get_name(url)
	get_image(url,name)

def threaded_download(minimum=1,maximum=2):
	with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
		for i in range(minimum,maximum):
			base_url=urlpart+str(i)
			executor.submit(image_retriever,base_url)


def non_threaded_download(minimum,maximum):
	for i in range(minimum,maximum):
		base_url=urlpart+str(i)
		image_retriever(base_url)


t1=time.perf_counter()
threaded_download(minimum=100,maximum=2206)
t2=time.perf_counter()
print(f"finished in {t1-t2} seconds")