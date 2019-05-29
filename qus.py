import os

from multiprocessing import Process
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

def scanner(s):
	format = s.replace("http://", "").replace("https://", "")
	result = request("GET", "http://"+format, allow_redirects=False)
	if result.status_code == 200:
		print "[+]\033[1;32m{} [{}]\033[0m".format(format, "Found")
		save_data(format)
	elif result.status_code == 302:
		print "[+]\033[33m{} redirect to \n{}\033[0m".format(format, result.headers["Location"])
		save_data(result.headers["Location"])
	else:
		print "[+]\033[31m{} [{}]\033[0m".format(format, "Not Found")
		
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
