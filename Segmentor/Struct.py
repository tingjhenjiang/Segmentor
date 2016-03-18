#!/usr/bin/python
#-*- encoding: UTF-8 -*-
#
#    This file is part of the NAER Segmentor  - 
#    Copyright (c) 2016 National Academy for Educational Research
# 
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
# 
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
Struct 模組
===========

----

這個模組提供了最基礎的資料結構，包括 Struct 及 StructList 類別。 
Struct 及 StructList 分別繼承了 dict 及 list 兩個內建類別，並額
外提供了下列的成員函數：

1. dumps(indent): 將結構以 json 的格式 dump 出來

2. loads(string): 將 json 字串剖析成樹狀結構

3. 這兩個結構內的資料可以以資料成員的方式存取，例如：

	>>> x=Struct()
	>>> x.data=10
	>>> print x.dumpJson(indent=4)
	{
		'data': 10
	}
"""

import json
import string

class Struct(dict):
	"""Struct 提供了基礎的節點結構。 
	"""
	def __init__(self, data=None):
		""" 
		**Parameters:**
			data : Struct 結構可接受初始值，初始值以 dict 形態傳入。
		"""
		if data:
			for k,v in data.items():
				if isinstance(v,dict):
					data[k]=Struct(v)
				elif isinstance(v,list):
					data[k]=StructList(v)
			self.update(data)

	def dumps(self, indent=None):
		""" 
		將結構及子結構 dump 成 json 字串。

		 **Parameters:**
			indent : dump 出的字串可以指定縮排的格式。預設值爲 None。
		"""
		return json.dumps(self, ensure_ascii=False, indent=indent)

	def loads(self, string):
		""" 
		從 json 字串載入樹狀結構。

		**Parameters:**
			string : 樹狀結構的 json 表示式。
		"""

		self.__init__(json.loads(string))


	def __getattr__(self, name):
		""" 
		提供__getattr__的資料設定方式。

		"""

		if name=='__deepcopy__':
			return None
		return self[name]

	def __setattr__(self, name, value):
		""" 
		提供__setattr__的資料設定方式。例如: 

		>>> x=Struct()
		>>> x.data=10
		>>> x.dumpJson(indent=4)
		{
			'data': 10
		}

		"""

		self[name]=value


class StructList(list):
	"""StructList 提供了 EHowNet 及 TreeBank 最基礎的 List 結構。 
	"""
	def __init__(self, data=None):
		if data:
			for idx in range(len(data)):
				if isinstance(data[idx],dict):
					data[idx]=Struct(data[idx])
				elif isinstance(v,list):
					data[idx]=StructList(data[idx])
			list.__init__(self, data)

	def dumps(self, indent=None):
		""" 
		將結構及子結構 dump 成 json 字串。

		**Parameters:**
			indent : dump 出的字串可以指定縮排的格式。預設值爲 None。
		"""

		return json.dumps(self, ensure_ascii=False, indent=indent)

	def loads(self, string):
		""" 
		從 json 字串載入 List 樹狀結構。

		**Parameters:**
			string : 樹狀結構的 json 表示式。
		"""

		list.__init__(self, json.loads(string))


class Word(unicode):
	def __new__(cls, *args, **kw):
		self=super(Word, cls).__new__(cls, *args, **kw)
		return self

class WordPos(tuple):
	format=u"%s(%s)"
	def __new__(cls, word, pos=u''):
		return tuple.__new__(cls, (word, pos))

	def __unicode__(self):
		if len(self[1])==0:
			return "%s"%(self[0])
		else:
			return WordPos.format%(self)

	def __str__(self, encoding="UTF-8"):
		return self.__unicode__().encode(encoding)

	def __getattr__(self, name):
		if name=='word':
			return self[0]
		elif name=='pos':
			return self[1]

class Sentence(StructList):
	boundary=u" "
	def __init__(self, data=[]):
		super(StructList,self).__init__(data)

	def __unicode__(self):
		L=[unicode(x) for x in self]
		str=string.join(L,Sentence.boundary)
		return str

	def __str__(self, encoding="UTF-8"):
		return self.__unicode__().encode(encoding)
	
if __name__=="__main__":
	a=Word(u'中文')
	print "Word=",a

	a=WordPos(word=u'中文',pos=u'Na')
	b=WordPos(word=u'英文',pos=u'Na')

	#print "WordPos.dumps()",a.dumps().encode("UTF-8")
	print "WordPos",a
	WordPos.format="%s/%s"
	print "WordPos",a

	x=a
	a=Sentence([a,b])
	print "Sentence.dumps():",a.dumps().encode("UTF-8")
	print "Sentence:",str(a)
	print unicode(a).encode("UTF-8")
	Sentence.boundary="XXX"
	print unicode(a).encode("UTF-8")

