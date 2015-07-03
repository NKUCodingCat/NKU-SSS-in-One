#coding=utf-8
import B
import requests, re, json
from lxml import etree
from urllib import urlencode
import encodings.idna
Ans = [["44", "4"], ["45", "3"], ["46", "2"], ["47", "1"], ["48", "0"], ["49", "4"], ["50", "3"], ["51", "2"], ["52", "1"], ["53", "0"], ["59", "4"], ["60", "3"], ["61", "2"], ["62", "1"], ["63", "0"], ["64", "4"], ["65", "3"], ["66", "2"], ["67", "1"], ["68", "0"], ["69", "4"], ["70", "3"], ["71", "2"], ["72", "1"], ["73", "0"], ["74", "4"], ["75", "3"], ["76", "2"], ["77", "1"], ["78", "0"], ["84", "4"], ["85", "3"], ["86", "2"], ["87", "1"], ["88", "0"], ["89", "4"], ["90", "3"], ["91", "2"], ["92", "1"], ["93", "0"], ["94", "4"], ["95", "3"], ["96", "2"], ["97", "1"], ["98", "0"], ["99", "4"], ["100", "3"], ["101", "2"], ["102", "1"], ["103", "0"], ["104", "4"], ["105", "3"], ["106", "2"], ["107", "1"], ["108", "0"], ["109", "4"], ["110", "3"], ["111", "2"], ["112", "1"], ["113", "0"], ["114", "4"], ["115", "3"], ["116", "2"], ["117", "1"], ["118", "0"], ["119", "4"], ["120", "3"], ["121", "2"], ["122", "1"], ["123", "0"], ["124", "4"], ["125", "3"], ["126", "2"], ["127", "1"], ["128", "0"], ["129", "4"], ["130", "3"], ["131", "2"], ["132", "1"], ["133", "0"], ["134", "4"], ["135", "3"], ["136", "2"], ["137", "1"], ["138", "0"], ["139", "4"], ["140", "3"], ["141", "2"], ["142", "1"], ["143", "0"], ["144", "4"], ["145", "3"], ["146", "2"], ["147", "1"], ["148", "0"], ["154", "0"], ["155", "1"], ["156", "2"], ["157", "3"], ["158", "4"], ["164", "4"], ["165", "3"], ["166", "2"], ["167", "1"], ["168", "0"], ["169", "4"], ["170", "3"], ["171", "2"], ["172", "1"], ["173", "0"], ["174", "4"], ["175", "3"], ["176", "2"], ["177", "1"], ["178", "0"], ["179", "4"], ["180", "3"], ["181", "2"], ["182", "1"], ["183", "0"], ["184", "4"], ["185", "3"], ["186", "2"], ["187", "1"], ["188", "0"], ["194", "4"], ["195", "3"], ["196", "2"], ["197", "1"], ["198", "0"], ["199", "4"], ["200", "3"], ["201", "2"], ["202", "1"], ["203", "0"], ["204", "4"], ["205", "3"], ["206", "2"], ["207", "1"], ["208", "0"], ["209", "4"], ["210", "3"], ["211", "2"], ["212", "1"], ["213", "0"], ["214", "4"], ["215", "3"], ["216", "2"], ["217", "1"], ["218", "0"], ["224", "4"], ["225", "3"], ["226", "2"], ["227", "1"], ["228", "0"], ["234", "4"], ["235", "3"], ["236", "2"], ["237", "1"], ["238", "0"], ["239", "4"], ["240", "3"], ["241", "2"], ["242", "1"], ["243", "0"], ["244", "4"], ["245", "3"], ["246", "2"], ["247", "1"], ["248", "0"], ["249", "4"], ["250", "3"], ["251", "2"], ["252", "1"], ["253", "0"], ["254", "4"], ["255", "3"], ["256", "2"], ["257", "1"], ["258", "0"], ["259", "4"], ["260", "3"], ["261", "2"], ["262", "1"], ["263", "0"], ["264", "4"], ["265", "3"], ["266", "2"], ["267", "1"], ["268", "0"], ["269", "4"], ["270", "3"], ["271", "2"], ["272", "1"], ["273", "0"], ["274", "4"], ["275", "3"], ["276", "2"], ["277", "1"], ["278", "0"], ["284", "4"], ["285", "3"], ["286", "2"], ["287", "1"], ["288", "0"], ["289", "4"], ["290", "3"], ["291", "2"], ["292", "1"], ["293", "0"], ["294", "4"], ["295", "3"], ["296", "2"], ["297", "1"], ["298", "0"], ["299", "4"], ["300", "3"], ["301", "2"], ["302", "1"], ["303", "0"], ["304", "4"], ["305", "3"], ["306", "2"], ["307", "1"], ["308", "0"], ["309", "4"], ["310", "3"], ["311", "2"], ["312", "1"], ["313", "0"], ["314", "4"], ["315", "3"], ["316", "2"], ["317", "1"], ["318", "0"], ["319", "4"], ["320", "3"], ["321", "2"], ["322", "1"], ["323", "0"], ["324", "4"], ["325", "3"], ["326", "2"], ["327", "1"], ["328", "0"], ["329", "4"], ["330", "3"], ["331", "2"], ["332", "1"], ["333", "0"], ["334", "4"], ["335", "3"], ["336", "2"], ["337", "1"], ["338", "0"], ["339", "4"], ["340", "3"], ["341", "2"], ["342", "1"], ["343", "0"], ["344", "4"], ["345", "3"], ["346", "2"], ["347", "1"], ["348", "0"], ["354", "4"], ["355", "3"], ["356", "2"], ["357", "1"], ["358", "0"], ["364", "4"], ["365", "3"], ["366", "2"], ["367", "1"], ["368", "0"], ["374", "4"], ["375", "3"], ["376", "2"], ["377", "1"], ["378", "0"], ["379", "4"], ["380", "3"], ["381", "2"], ["382", "1"], ["383", "0"], ["389", "4"], ["390", "3"], ["391", "2"], ["392", "1"], ["393", "0"], ["394", "4"], ["395", "3"], ["396", "2"], ["397", "1"], ["398", "0"], ["399", "4"], ["400", "3"], ["401", "2"], ["402", "1"], ["403", "0"], ["404", "4"], ["405", "3"], ["406", "2"], ["407", "1"], ["408", "0"], ["414", "4"], ["415", "3"], ["416", "2"], ["417", "1"], ["418", "0"], ["419", "4"], ["420", "3"], ["421", "2"], ["422", "1"], ["423", "0"], ["424", "4"], ["425", "3"], ["426", "2"], ["427", "1"], ["428", "0"], ["429", "4"], ["430", "3"], ["431", "2"], ["432", "1"], ["433", "0"], ["434", "4"], ["435", "3"], ["436", "2"], ["437", "1"], ["438", "0"], ["439", "4"], ["440", "3"], ["441", "2"], ["442", "1"], ["443", "0"], ["444", "4"], ["445", "3"], ["446", "2"], ["447", "1"], ["448", "0"], ["449", "4"], ["450", "3"], ["451", "2"], ["452", "1"], ["453", "0"], ["464", "4"], ["465", "3"], ["466", "2"], ["467", "1"], ["468", "0"], ["469", "4"], ["470", "3"], ["471", "2"], ["472", "1"], ["473", "0"], ["474", "4"], ["475", "3"], ["476", "2"], ["477", "1"], ["478", "0"], ["479", "4"], ["480", "3"], ["481", "2"], ["482", "1"], ["483", "0"], ["489", "4"], ["490", "3"], ["491", "2"], ["492", "1"], ["493", "0"], ["494", "4"], ["495", "3"], ["496", "2"], ["497", "1"], ["498", "0"], ["504", "4"], ["505", "3"], ["506", "2"], ["507", "1"], ["508", "0"], ["509", "4"], ["510", "3"], ["511", "2"], ["512", "1"], ["513", "0"], ["514", "4"], ["515", "3"], ["516", "2"], ["517", "1"], ["518", "0"], ["519", "4"], ["520", "3"], ["521", "2"], ["522", "1"], ["523", "0"], ["524", "4"], ["525", "3"], ["526", "2"], ["527", "1"], ["528", "0"], ["529", "4"], ["530", "3"], ["531", "2"], ["532", "1"], ["533", "0"], ["539", "4"], ["540", "3"], ["541", "2"], ["542", "1"], ["543", "0"], ["544", "4"], ["545", "3"], ["546", "2"], ["547", "1"], ["548", "0"], ["549", "4"], ["550", "3"], ["551", "2"], ["552", "1"], ["553", "0"], ["554", "4"], ["555", "3"], ["556", "2"], ["557", "1"], ["558", "0"], ["559", "4"], ["560", "3"], ["561", "2"], ["562", "1"], ["563", "0"], ["564", "4"], ["565", "3"], ["566", "2"], ["567", "1"], ["568", "0"], ["569", "4"], ["570", "3"], ["571", "2"], ["572", "1"], ["573", "0"], ["574", "4"], ["575", "3"], ["576", "2"], ["577", "1"], ["578", "0"], ["579", "4"], ["580", "3"], ["581", "2"], ["582", "1"], ["583", "0"], ["584", "4"], ["585", "3"], ["586", "2"], ["587", "1"], ["588", "0"], ["589", "4"], ["590", "3"], ["591", "2"], ["592", "1"], ["593", "0"], ["594", "4"], ["595", "3"], ["596", "2"], ["597", "1"], ["598", "0"], ["599", "4"], ["600", "3"], ["601", "2"], ["602", "1"], ["603", "0"], ["604", "4"], ["605", "3"], ["606", "2"], ["607", "1"], ["608", "0"], ["614", "4"], ["615", "3"], ["616", "2"], ["617", "1"], ["618", "0"], ["619", "4"], ["620", "3"], ["621", "2"], ["622", "1"], ["623", "0"], ["624", "4"], ["625", "3"], ["626", "2"], ["627", "1"], ["628", "0"], ["629", "4"], ["630", "3"], ["631", "2"], ["632", "1"], ["633", "0"], ["634", "4"], ["635", "3"], ["636", "2"], ["637", "1"], ["638", "0"], ["639", "4"], ["640", "3"], ["641", "2"], ["642", "1"], ["643", "0"], ["649", "4"], ["650", "3"], ["651", "2"], ["652", "1"], ["653", "0"], ["659", "4"], ["660", "3"], ["661", "2"], ["662", "1"], ["663", "0"], ["664", "4"], ["665", "3"], ["666", "2"], ["667", "1"], ["668", "0"], ["669", "4"], ["670", "3"], ["671", "2"], ["672", "1"], ["673", "0"], ["674", "4"], ["675", "3"], ["676", "2"], ["677", "1"], ["678", "0"], ["679", "4"], ["680", "3"], ["681", "2"], ["682", "1"], ["683", "0"], ["684", "4"], ["685", "3"], ["686", "2"], ["687", "1"], ["688", "0"], ["689", "4"], ["690", "3"], ["691", "2"], ["692", "1"], ["693", "0"], ["694", "4"], ["695", "3"], ["696", "2"], ["697", "1"], ["698", "0"], ["699", "4"], ["700", "3"], ["701", "2"], ["702", "1"], ["703", "0"], ["704", "4"], ["705", "3"], ["706", "2"], ["707", "1"], ["708", "0"], ["709", "4"], ["710", "3"], ["711", "2"], ["712", "1"], ["713", "0"], ["714", "4"], ["715", "3"], ["716", "2"], ["717", "1"], ["718", "0"], ["719", "4"], ["720", "3"], ["721", "2"], ["722", "1"], ["723", "0"], ["724", "4"], ["725", "3"], ["726", "2"], ["727", "1"], ["728", "0"], ["729", "4"], ["730", "3"], ["731", "2"], ["732", "1"], ["733", "0"], ["734", "4"], ["735", "3"], ["736", "2"], ["737", "1"], ["738", "0"], ["739", "4"], ["740", "3"], ["741", "2"], ["742", "1"], ["743", "0"], ["744", "4"], ["745", "3"], ["746", "2"], ["747", "1"], ["748", "0"], ["749", "4"], ["750", "3"], ["751", "2"], ["752", "1"], ["753", "0"], ["754", "4"], ["755", "3"], ["756", "2"], ["757", "1"], ["758", "0"], ["759", "4"], ["760", "3"], ["761", "2"], ["762", "1"], ["763", "0"], ["764", "4"], ["765", "3"], ["766", "2"], ["767", "1"], ["768", "0"], ["774", "4"], ["775", "3"], ["776", "2"], ["777", "1"], ["778", "0"], ["779", "4"], ["780", "3"], ["781", "2"], ["782", "1"], ["783", "0"], ["784", "4"], ["785", "3"], ["786", "2"], ["787", "1"], ["788", "0"], ["789", "4"], ["790", "3"], ["791", "2"], ["792", "1"], ["793", "0"], ["794", "4"], ["795", "3"], ["796", "2"], ["797", "1"], ["798", "0"], ["799", "4"], ["800", "3"], ["801", "2"], ["802", "1"], ["803", "0"], ["804", "4"], ["805", "3"], ["806", "2"], ["807", "1"], ["808", "0"], ["809", "4"], ["810", "3"], ["811", "2"], ["812", "1"], ["813", "0"], ["814", "0"], ["815", "1"], ["816", "2"], ["817", "3"], ["818", "4"], ["819", "0"], ["820", "1"], ["821", "2"], ["822", "3"], ["823", "4"], ["824", "0"], ["825", "1"], ["826", "2"], ["827", "3"], ["828", "4"], ["829", "0"], ["830", "1"], ["831", "2"], ["832", "3"], ["833", "4"], ["834", "0"], ["835", "1"], ["836", "2"], ["837", "3"], ["838", "4"], ["839", "0"], ["840", "1"], ["841", "2"], ["842", "3"], ["843", "4"], ["844", "0"], ["845", "1"], ["846", "2"], ["847", "3"], ["848", "4"], ["849", "0"], ["850", "1"], ["851", "2"], ["852", "3"], ["853", "4"], ["854", "0"], ["855", "1"], ["856", "2"], ["857", "3"], ["858", "4"], ["859", "0"], ["860", "1"], ["861", "2"], ["862", "3"], ["863", "4"], ["864", "0"], ["865", "1"], ["866", "2"], ["867", "3"], ["868", "4"], ["869", "0"], ["870", "1"], ["871", "2"], ["872", "3"], ["873", "4"], ["874", "0"], ["875", "1"], ["876", "2"], ["877", "3"], ["878", "4"], ["879", "0"], ["880", "1"], ["881", "2"], ["882", "3"], ["883", "4"], ["884", "0"], ["885", "1"], ["886", "2"], ["887", "3"], ["888", "4"], ["889", "0"], ["890", "1"], ["891", "2"], ["892", "3"], ["893", "4"], ["894", "0"], ["895", "1"], ["896", "2"], ["897", "3"], ["898", "4"], ["899", "0"], ["900", "1"], ["901", "2"], ["902", "3"], ["903", "4"], ["904", "0"], ["905", "1"], ["906", "2"], ["907", "3"], ["908", "4"], ["909", "0"], ["910", "1"], ["911", "2"], ["912", "3"], ["913", "4"], ["914", "0"], ["915", "1"], ["916", "2"], ["917", "3"], ["918", "4"], ["919", "0"], ["920", "4"], ["921", "0"], ["922", "2"], ["923", "4"], ["924", "2"], ["925", "0"], ["926", "2"], ["927", "2"], ["928", "0"], ["929", "4"], ["930", "4"], ["931", "4"], ["932", "0"], ["933", "4"], ["934", "2"], ["935", "2"], ["944", "4"], ["945", "3"], ["946", "2"], ["947", "1"], ["948", "0"], ["949", "4"], ["950", "2"], ["951", "0"], ["952", "2"], ["953", "4"], ["954", "2"], ["955", "0"], ["956", "2"]]
def login(S, usr, pwd):
	S.get("""http://fuxue.nankai.edu.cn/index.php""")
	S.get("""http://fuxue.nankai.edu.cn/index.php/Account/login""")
	RE = S.post("""http://fuxue.nankai.edu.cn/index.php/Account/doLogin""", data = {"username":usr, "password":pwd})
	if re.findall("title", RE.content):
		return None
	else:
		return S
def QueAns(html):
	choose = {}
	page = etree.HTML(html.lower().decode('utf-8'))
	form = page.xpath(u"//form")
	for i in  form[0].xpath(u"input"):
		try:
			choose[i.attrib["name"]].append(i.attrib["value"])
		except KeyError:
			choose[i.attrib["name"]]=[i.attrib["value"], ]
	return AnsGen(choose)
def AnsGen(Que_dict):
	T = {}
	for key in Que_dict.keys():
		D = sorted([j for j in Ans if j[0] in Que_dict[key]], key = lambda x:int(x[1]), reverse=True)
		T[key] = D[0][0]
	return urlencode(T)
def Test(S):
	S.get("""http://fuxue.nankai.edu.cn/index.php/assessment/xnmPropaganda""")
	S.get("""http://fuxue.nankai.edu.cn/index.php/assessment/xnmSelfAssessment""")
	headers = {"Referer": ""}
	i = 1
	T = {}
	while True:
		QuUrl = """http://fuxue.nankai.edu.cn/index.php/assessment/question/fangxiang/xia/pid/%s"""%i
		G = S.get(QuUrl, headers = headers).content
		print u"正在完成第%s页……"%i
		T  = QueAns(G)
		headers["Referer"] = QuUrl
		J = S.post("""http://fuxue.nankai.edu.cn/index.php/assessment/question_ajax/""", data={"answer":T}, headers = headers).content
		try:
			if json.loads(J)["json"]["status"] != "0":
				raise ValueError
			print u"已完成"
		except:
			raise
		i+=1
		if re.findall("\<button id\=\"commit\"\>", G):
			break
	try:
		if json.loads(S.post("""http://fuxue.nankai.edu.cn/index.php/assessment/commit_ajax""", data={"answer":T}).content)["json"]["status"] != "0":
			return False
		else:
			return True
	except:
		return False
	
		
#def lxml_de():
if __name__ == "__main__":
	print(u"""
;;;;;;;;;;;;;;;;;;;;;;;;;    Developed By NKUCodingcat
;;;;;;;;;;;;;;;WWW;;;;;;;    有问题联系admin@nkucodingcat.com
;;;;;;;;WWWWW;;;;WWWi;;;;    欢迎使用南开大学
;;;;;;WWWWWWj;;;;;KWWW;;;    龚能测评自评刷题机
;;;;WWWWWWW;;;;;;;;WWWK;;    能刷完所有的自评题
;;;iWWWWWWWWWi;;;;;KWWW;;    互评的……是另一个程序╮(￣▽￣")╭ 
;;;;;;W;;;WWWWWK;;;WWWW;;    这东西吧……
;;;;;;;;;;;;WWWWWW;WWWW;;    真的看网速
;;;W;;;;;;;;;EWWWWWWWW;;;    反正去年那群家伙说好的3000人
;;WWWWK;;;;;;;;WWWWWW;;;;    结果成功每小时崩溃一次
;WWWWWWWWWWWWWWWWWWWWWW;;    = =某人说外网也能开
;WWW;;;WWWWWWWWW;;;;W;;;;    不知道是不是真的= =
;;;;;;;;;;;;;;;;;;;;;;;;;    实在不行还有小伙伴嘛""")

	print(u"""
    Ver 2015.05.20  抗日还靠Dang中央——银妹\n
=======================================

重要的事情要说三遍

>这货是刷自评的，自带满分技能

>这货是刷自评的，自带满分技能

>这货是刷自评的，自带满分技能

""")
	S = requests.session()
	while 1:
		usr = raw_input("Input your id plz and press Enter  : ")
		if len(usr) != 7:
			print 'wrong length of id,input again'
		else:
			break
	pwd = raw_input("Input Your PassWord and press Enter : ")
	try:
		S = login(S, usr, pwd)
	except:
		raise
		print u"网络好像有点不对= = 请稍后再试……实在不行请联系admin@nkucodingcat.com"
		print u"按enter退出"
		raw_input()
		try:
			exit()
		except:
			pass
	if not S:
		print u"密码错误，请按enter退出，然后重新进入"
		raw_input()
		try:
			exit()
		except:
			pass
	else:
		try:
			j = Test(S)
			if j :
				try:
					S.get("http://fuxue.nankai.edu.cn/index.php/Assessment/judgeStuLevel")
				except:
					print u"请自行访问 http://fuxue.nankai.edu.cn/index.php/Assessment/judgeStuLevel"
				print u"测试完成请按enter退出"
				raw_input()
				try:
					exit()
				except:
					pass
			else:
				print u"有未知错误, 请联系admin@nkucodingcat.com"
		except:
			#raise
			print u"有未知错误, 请联系admin@nkucodingcat.com"