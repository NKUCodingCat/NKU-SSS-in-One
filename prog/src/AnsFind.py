#coding=utf-8
import os, difflib, re
import fileinput
class AnsFind:
	def __init__(self, F=os.path.split(os.path.realpath(__file__))[0]+"/ans.txt"):
		self.K = []
		for line in fileinput.input(F):
			self.K.append(re.split("//",re.sub("\s+","",unicode(line.decode("utf-8"))))[:2])
	def Q_find(self, src):
		#传入题目， 返回题目-答案
		Copy = self.K[:]
		J = [i+[difflib.SequenceMatcher(None, src, i[0]).ratio(),] for i in Copy]
		return sorted(J, key=lambda x:x[2])[-1]
	def A_find(self, ans_dict, correct_ans):
		S = [list(i)+[difflib.SequenceMatcher(None, correct_ans, i[1]).ratio(),] for i in ans_dict.items()]
		#print S
		return sorted(S, key=lambda x:x[2])[-1]
	def Manual_Select(self, Q_S_Tuple):
		print u"请手动选择答案"
		print Q_S_Tuple[0]
		k = 1
		for i in Q_S_Tuple[1].keys():
			print k, Q_S_Tuple[1][i]
			k+=1
		while True:
			try:
				Ans = raw_input("请输入序号：".decode("utf-8").encode("GBK"))
				return [Q_S_Tuple[1].keys()[int(Ans)-1], Q_S_Tuple[1][Q_S_Tuple[1].keys()[int(Ans)-1]], 1.0]
			except:
				print "请输入正确的序号"
	def FindAns(self, Q_S_Tuple):
		
		Que = Q_S_Tuple[0]
		An =  self.Q_find(Que)
		#print Que,"/" , An[0] ,"/",An[1],"/ ", An[2]
		if An[2] < 0.8:
			print "题库中未找到对应题目"
			print Que,"/" , An[0] ,"/",An[1],"/ ", An[2]
			return self.Manual_Select(Q_S_Tuple)
		Sel = Q_S_Tuple[1]
		FinalRes = self.A_find(Sel, An[1])
		#print Sel
		if FinalRes[2] < 0.90:
			print "题库中未找到正确答案"
			print Que,"/" , An[0] ,"/",An[1],"/ ", An[2]
			#for i in Sel.keys():
			#	print i, Sel[i]
			return self.Manual_Select(Q_S_Tuple)
		#print FinalRes[2],"/",
		return FinalRes
if __name__ == "__main__":
	M = AnsFind()
	import json
	for i in json.loads(open(os.path.split(os.path.realpath(__file__))[0]+"/res.txt").read()).items():
		LL = M.FindAns(i)