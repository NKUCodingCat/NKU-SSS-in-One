#coding=utf-8
import B
import urllib
import urllib2 
import cookielib
import re

import sys



nID = ''
while 1:
    nID = raw_input("Input your id and press Enter plz    ")
    if len(nID) != 7:
		print 'wrong length of id,input again'
    else:
        break
Pass = raw_input("Input your password and press Enter plz     ")




url = 'http://fuxue.nankai.edu.cn/index.php/assessment/question/mod/show'
urllogin = 'http://fuxue.nankai.edu.cn/index.php/Account/doLogin'

cj = cookielib.CookieJar()
pattern = re.compile(r'<h3>\S*:\S*')
pattern1 = re.compile(r'"[0-9]+" >\S*')
valueslogin ={
'Host':' fuxue.nankai.edu.cn',
'Connection':' keep-alive',
'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
'DNT':' 1',
'Accept-Encoding':' gzip,deflate,sdch',
'Accept-Language':' zh-CN,zh;q=0.8'
} 
postdata = urllib.urlencode({'username':nID,'password':Pass})

req3 = urllib2.Request(urllogin,headers=valueslogin) 
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
response = opener.open(req3,postdata)
print 'Account Checking.........'
if not re.findall(re.escape("url=http://fuxue.nankai.edu.cn/index.php/index/index\' >"), response.read()):
	print 'Password Error'
	raw_input("Press Enter to continue")
	sys.exit(0)
for cookie in cj:
	cookie = cookie.value
IDStart = ''
while 1:
    IDStart = raw_input("Input the first id you want to assess and press Enter plz    ")
    if len(IDStart) != 7:
        print 'wrong length of id,input again'
    else:
        break	
IDEnd = ''
while 1:
    IDEnd = raw_input("Input the last id you want to assess and press Enter  plz    ")
    if len(IDEnd) != 7:
        print 'wrong length of id,input again'
    else:
        break
values = {
'Host':' fuxue.nankai.edu.cn',
'Connection':' keep-alive',
'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
'DNT':' 1',
'Referer':'http://fuxue.nankai.edu.cn/index.php/assessment/xnmSelfAssessment',
'Accept-Encoding':' gzip,deflate,sdch',
'Accept-Language':' zh-CN,zh;q=0.8',
'Cookie':' PHPSESSID='+cookie
}
IDS=int(IDStart)
IDE=int(IDEnd)
print 'connecting...................'




count = IDS
strup = 'http://fuxue.nankai.edu.cn/index.php/assessment/appraise_ajax'

Cook=' PHPSESSID='+cookie
for i in range(IDS,IDE+1):
	Re='http://fuxue.nankai.edu.cn/index.php/assessment/appraise/num/'
	values2 = {
	'Host':' fuxue.nankai.edu.cn',
	'Connection':' keep-alive',
	'Accept':'  */*',
	'Origin':' http://fuxue.nankai.edu.cn',
	'X-Requested-With':' XMLHttpRequest',
	'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
	'Content-Type':' application/x-www-form-urlencoded; charset=UTF-8',
	'DNT':' 1',
	'Referer':Re+str(count),
	'Accept-Encoding':' gzip,deflate,sdch',
	'Accept-Language':' zh-CN,zh;q=0.8',
	'Cookie':Cook
	}
	'''
	Search
	'''
	req4 = urllib2.Request((Re+str(count)),headers=values)
	content2 = urllib2.urlopen(req4).read()
	url2=(strup)
	'''
	Upload
	'''
	req = urllib2.Request(url2,headers=values2)
	content = urllib2.urlopen(req,urllib.urlencode([('num',str(count)),('assproid','9'),('gong','6'),('neng1','6'),('neng2','6'),('neng3','6'),('neng4','6'),('neng5','6'),('good1',''),('good2',''),('good3',''),('bad1',''),('bad2',''),('bad3','')])).read()
	print count
	
	count=count + 1
	
raw_input("\nMission Complete\nPress Enter to continue")