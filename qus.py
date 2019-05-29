import os
from subprocess import Popen, PIPE
from multiprocessing import Process
import datetime
try:
	from requests import request
except ImportError:
	print "Yous must Install requests moduls\nfor running this script"
def banner():
	g = "="*20
	print "{}\nSimple Costum Url Finders\nBy QiubyZhukhi\n{}".format(g, g)
def real_path(file_name):
    return os.path.dirname(os.path.abspath(__file__)) + file_name
def urlparse(u):
	return "/"+u if u[0] != "/" else u
def color(color="G", teks=None):
	values = {
		"G":"\033[1;32m",
		"R":"\033[31m",
		"w":"\033[0m",
		"RD":"\033[33m"
		}
	colors = "{}[{}] {} [FOUND]{}".format(
		values.get(color),
		datetime.datetime.now().strftime('%H:%M:%S'),
		teks,
		values.get("w"))
	if color is "RD":
		colors=colors.replace("FOUND", "REDIRECT")
	elif color is "R":
		colors=colors.replace("FOUND", "NOT FOUND")
	return colors
def scanner(s):
	format = "http://"+s.replace("https://", "")
	result = request("GET", format, allow_redirects=False)
	if result.status_code == 200:
		print color(teks=format, color= "G")
		save_data(format)
	elif result.status_code == 302:
		print color(teks=result.headers["Location"], color="RD")
		save_data(result.headers["Location"])
	else:
		print color(teks=format, color="R")
def save_data(isi):
	with open(real_path("/logs.txt"), "a+") as saved:
		saved.write("{}\n".format(isi))
		saved.close()
def ope_files():
	with open(real_path("/check.txt")) as read_files:
		a = [urlparse(i.replace("\n","")) for i in read_files.readlines()]
		return a
def starting():
	banner()
	site = raw_input("Inser domain: ")
	multiprocess = []
	for scanners in ope_files():
		t = Process(target=scanner, args=(site+scanners,))
		multiprocess.append(t)
		t.daemon = True
		t.start()
	join = [i.join() for i in multiprocess]
if __name__ == "__main__":
	starting()
