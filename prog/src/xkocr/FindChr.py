
import os
import numpy
import re
K = filter(lambda x: x[1] or x[0], [[i, j] for i in [-1,0,1] for j in [-1, 0 , 1]])
import StringIO
import sys

def Delta(arr1, arr2):
	z = zip(arr1, arr2)
	return sum(map(lambda x:abs(int(x[0])-int(x[1])), z))


def MaxEnhance(NP):
	J = numpy.zeros(NP.shape[:2])
	ZeroColor = NP[13][79]
	for i in range(NP.shape[0]):
		for j in range(NP.shape[1]):
			EnhanceList = filter(lambda x:(x[0] >= 0 and x[0] < NP.shape[0]) and (x[1] >= 0 and x[1] < NP.shape[1]), [(i+k[0], j+k[1]) for k in K])
			try:
				Surrounding = sum(sorted(map(lambda zero,delta:Delta(NP[zero[0]][zero[1]], NP[delta[0]][delta[1]]), [[i, j ],]*len(EnhanceList), EnhanceList ))[-3:])
				ZeroDistance = Delta(NP[i][j], ZeroColor)
				if ZeroDistance > 100:
					J[i][j] = Surrounding
			except KeyboardInterrupt:
				raise
			except:
				pass
	return J

def x_Ran(IMG_Arr):
	G = numpy.transpose(IMG_Arr)
	Gx_bit = [[1 if j>0 else 0 for j in i] for i in G]
	Mark = []
	for i in range(len(Gx_bit)-1):
		pre = Gx_bit[i]
		now = Gx_bit[i+1]
		Has_White = False
		Need_Split = True
		for j in range(1, len(pre)-1):
			if pre[j] == 1:
				Has_White = True
				if now[j-1] == 1 or now[j] == 1 or now[j+1] == 1:
					Need_Split = False
			if now[j] == 1:
				Has_White = True
				if pre[j-1] == 1 or pre[j] == 1 or pre[j+1] == 1:
					Need_Split = False

		if Has_White and Need_Split:
			Mark.append(i+1)
	return Mark

def y_Ran(Sub_IMG_Arr):
	G = numpy.transpose(Sub_IMG_Arr)
	#G = Sub_IMG_Arr
	for i in range(len(G)):
		if numpy.any(G[i]):
			down = i
	for i in range(len(G)-1, -1, -1):
		if numpy.any(G[i]):
			up = i
	return [up, down]



def CutBox(im):
	Q = numpy.asarray(im)
	Arr = MaxEnhance(Q)
	MAX = numpy.amax(Arr)
	Arr = numpy.where(Arr>((30*MAX)/255), 255, 0)
	X_range = x_Ran(Arr)
	Arr = numpy.transpose(Arr)
	Tmp = []
	for i in range(len(X_range)-1):
		X_Box  = Arr[X_range[i]:X_range[i+1]]
		if numpy.any(X_Box):
			Y_range = y_Ran(X_Box)
			if Y_range[0] == Y_range[1]:
				pass
			else:
				Tmp.append(numpy.transpose(Arr[ X_range[i]:X_range[i+1] , Y_range[0]:Y_range[1]+1]))

	return Tmp
if __name__ =="__main__":
	from PIL import Image
	root = os.path.split(os.path.realpath(__file__))[0]+"/ph/"
	rootd = os.path.split(os.path.realpath(__file__))[0]+"/phd/"	
	for i in os.listdir(rootd):
		os.remove(rootd+i)
	
	for i in os.listdir(root):
		try:
			k = 0
			BOX = (CutBox(Image.open(root+i)))
			for j in BOX:
				k += 1
				Image.fromarray(abs(255 - j)).convert("L").save(rootd+os.path.splitext(i)[0]+"-%s.bmp"%k)
		except KeyboardInterrupt:
			break
		except :
			raise
	
