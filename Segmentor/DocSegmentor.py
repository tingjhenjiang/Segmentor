#!/usr/bin/python
#coding: utf8
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

##==========================================
##  use crf POS tagger
##==========================================

import os,re
import string
from Segmentor import *
from POSTagger import *
from Struct import *

## set ../Data directory as default model directory 

__default_model_dir__=os.path.abspath(os.path.dirname(__file__)+'/../Data')

class DocPOSTagger(POSTagger):

	_sent_rule='[^\r\n]+'

	def __init__(self, model_dir=__default_model_dir__):
		super(DocPOSTagger, self).__init__(model_dir)
		self._mask_rule=None
		self._sent_callback=self._sent_postag_callback

	def _assemble_tokens(self, tagged_tokens):
		   
		result=Sentence()
		for data in tagged_tokens:
			word=data[0].decode("UTF-8")
			result.append(WordPos(word, data[-1])) 

		return result

	def _assemble_tokens_mask(self, tagged_tokens):
		   
		result=Sentence()
		for data in tagged_tokens:
			word=data[0].decode("UTF-8")
			if self._mask_rule.match(word):
				result.append(WordPos(word)) 
			else:
				result.append(WordPos(word, data[-1])) 

		return result

	def setFormat(self, format):
		WordPos.format=format

	def setBoundary(self, boundary):
		Sentence.boundary=boundary
		self.boundary=re.compile(re.escape(boundary))

	def setMask(self, mask_list):
		if isinstance(mask_list, list):
			mask=u'|'.join([x+u'$' for x in mask_list])
		else:
			mask=mask_list+u'$'
		self._mask_rule=re.compile(mask)
		self._assemble_tokens=self._assemble_tokens_mask

	def setRegion(self, region_list):
		L=[]
		for region in region_list:
			(start,end)=region.split("::")
			L.append(u"(?<=%s).*?(?=%s)"%(start,end))
		self._region_rule=string.join(L,u'|')
		self._proc_callback=self._region_callback
		self._proc_rule=self._region_rule

	def _sent_postag_callback(self, m):
		tagged_sent=self.procSentStr(m.group(0))
		out_buf=tagged_sent.__unicode__()
		return out_buf

	def _region_callback(self, m):
		region=m.group(0)
		out_buf=re.sub(DocPOSTagger._sent_rule, self._sent_callback, region)
		return out_buf

	def procDoc(self, doc):
		out_buf=re.sub(self._proc_rule, self._proc_callback, doc, flags=re.MULTILINE|re.DOTALL)
		return out_buf

class DocSegmentor(Segmentor):

	_sent_rule='[^\r\n]+'

	def __init__(self, model_dir=__default_model_dir__, segment=True, postag=False):
		super(DocSegmentor, self).__init__(model_dir)

		self._mask_rule=None
		self._region_rule=None
		self.postag=postag

		if postag:
			self.POSTagger=DocPOSTagger(model_dir)
			if segment:
				self._sent_callback=self._sent_segment_postag_callback
			else:
				self._sent_callback=self._sent_postag_callback
		else:
			self._sent_callback=self._sent_segment_callback

		self._proc_callback=self._sent_callback
		self._proc_rule=DocSegmentor._sent_rule

	@staticmethod
	def setFormat(format):
		WordPos.format=format

	@staticmethod
	def setBoundary(boundary):
		Sentence.boundary=boundary

	def setMask(self, mask_list):
		# mask rule 也要合併進 _to_tokens_rule

		if isinstance(mask_list, list):
			mask1=u'|'.join([x for x in mask_list])
			mask2=u'|'.join([x+u'$' for x in mask_list])
		else:
			mask1=mask_list
			mask2=mask_list+u'$' 

		rule="%s|%s"%(mask1,Segmentor._to_tokens_pattern)
		self._to_tokens_rule=re.compile(rule)
		self._mask_rule=re.compile(mask2)
		self._assemble_tokens=self._assemble_tokens_mask

		if self.postag:
			self.POSTagger.setMask(mask_list)

	def setRegion(self, region_list):
		L=[]
		for region in region_list:
			(start,end)=region.split("::")
			L.append(u"(?<=%s).*?(?=%s)"%(start,end))
		self._region_rule=string.join(L,u'|')
		self._proc_callback=self._region_callback
		self._proc_rule=self._region_rule

	def _sent_segment_callback(self, m):
		seged_sent=self.procSent(m.group(0))
		out_buf=seged_sent.__unicode__()
		return out_buf

	def _sent_segment_postag_callback(self, m):
		seged_sent=self.procSent(m.group(0))
		tagged_sent=self.POSTagger.procSent(seged_sent)
		out_buf=tagged_sent.__unicode__()
		return out_buf

	def _sent_postag_callback(self, m):
		tagged_sent=self.POSTagger.procSentStr(m.group(0))
		out_buf=tagged_sent.__unicode__()
		return out_buf

	def _region_callback(self, m):
		region=m.group(0)
		out_buf=re.sub(DocSegmentor._sent_rule, self._sent_callback, region)
		return out_buf

	def _assemble_tokens(self, tagged_tokens):
		## start to assemble the tokens
		words = Sentence()
		temp_word = ""
		for now_char,BI in tagged_tokens:
			if BI == "S":
				if len(temp_word) > 0:##已經有詞 先輸出 
					words.append(Word(temp_word))
				##加上本身自己的詞
				words.append(Word(now_char))
				temp_word = ""

			elif BI == "B":					
				if len(temp_word) > 0:##已經有詞 先輸出 
					words.append(Word(temp_word))
					
				temp_word = now_char
			elif BI == "I" or BI =="E":

				if re.match(u'[a-zA-Z0-9_][a-zA-Z0-9_\\/,.&\-]*$',now_char):
					temp_word += " "+now_char  ##(英文及符號之後須考慮多加空白)
				else:
					temp_word += now_char  
		if len(temp_word) > 0:
			words.append(Word(temp_word)) ##最後一個詞

		return words


	def _assemble_tokens_mask(self, tagged_tokens):
		## start to assemble the tokens
		words = Sentence()
		temp_word = ""
		for now_char,BI in tagged_tokens:
			if self._mask_rule.match(now_char) or BI == "S":
				if len(temp_word) > 0:##已經有詞 先輸出 
					words.append(Word(temp_word))
				##加上本身自己的詞
				words.append(Word(now_char))
				temp_word = ""

			elif BI == "B":					
				if len(temp_word) > 0:##已經有詞 先輸出 
					words.append(Word(temp_word))
					
				temp_word = now_char
			elif BI == "I" or BI =="E":

				if re.match(u'[a-zA-Z0-9_][a-zA-Z0-9_\\/,.&\-]*$',now_char):
					temp_word += " "+now_char  ##(英文及符號之後須考慮多加空白)
				else:
					temp_word += now_char  
		if len(temp_word) > 0:
			words.append(Word(temp_word)) ##最後一個詞

		return words


	def procDoc(self, doc):
		out_buf=re.sub(self._proc_rule, self._proc_callback, doc, flags=re.MULTILINE|re.DOTALL)
		return out_buf


if __name__=="__main__":
	xml_doc=u'''\
<title>這是xml的測試</title>

<xxx>這一段不要斷詞</xxx>

<desc>這 是 desc 的 測試</desc>

<body>

<text>市面上很少有「教科書設計」的專書，因為我們總覺得那是出版社的事！
然而，真的是這樣嗎？

教科書設計其實與課程綱要、教師的教學、學生的學習息息相關，是課程、教學、學習三位一體間一個重要的環節，除了有教育學與學科專業等內容涵納其中，也與編輯、版式等視覺設計元素的概念有關。
有鑒於此議題的重要，本院教科書發展中心邀請淡江大學課程與教學研究所陳麗華所長，於8月27日上午進行「教科書設計研究」專題演講，除了院內同仁，也邀請出版社編輯企劃相關人員參與。</text>

<text>市面上很少有「<strong>教科書設計</strong>」的專書，因為我們總覺得那是出版社的事！
然而，真的是這樣嗎？

教科書設計其實與課程綱要、教師的教學、學生的學習息息相關，是課程、教學、學習三位一體間一個重要的環節，除了有教育學與學科專業等內容涵納其中，也與編輯、版式等視覺設計元素的概念有關。
有鑒於此議題的重要，本院教科書發展中心邀請淡江大學課程與教學研究所陳麗華所長，於8月27日上午進行「教科書設計研究」專題演講，除了院內同仁，也邀請出版社編輯企劃相關人員參與。</text>
</body>
'''

	print "DEBUG1: 測試 region and mask"
	b=DocSegmentor(postag=True)
	b.setMask('<[^>]+>')
	b.setRegion(region_list=[u'<title>::</title>',u'<text>::</text>'])
	xml_doc1=b.procDoc(xml_doc)
	print xml_doc1.encode("UTF-8")

	print "DEBUG2: 測試 region on desc"
	b=DocSegmentor(postag=True)
	b.setRegion(region_list=[u'<desc>::</desc>'])
	xml_doc2=b.procDoc(xml_doc1)
	print xml_doc2.encode("UTF-8")

	doc=u"""你摸著一下\n對@@@你先摸\nOK\n拿自己的車\n馬祖的那個島是不太大\n但是它們的坡度很大\n所以我們在一輪車的練習方面
要多練習這個上坡的　下坡的
感謝主
我們要出發以前
確切的仰望我們主向我們施恩
保佑所看顧我們一切
能夠平安順利
好 出發了"""

	# 半型空白不可以 mask 因為 CRFPP 以空白當分隔符號

	print "DEBUG3: 測試 mask and boundary"
	c=DocSegmentor(postag=True)
	c.setMask(mask_list=[u'　', u'@@@', u' '])
	c.setBoundary(boundary=u'|||')
	doc2=c.procDoc(doc)
	print doc2.encode("UTF-8")

	print "DEBUG4: 測試 POStagger and boundary"
	d=DocSegmentor(postag=False)
	d.setRegion(region_list=[u'<title>::</title>',u'<text>::</text>'])
	d.setBoundary(boundary=u'|||')
	d.setMask('<[^>]+>')
	xml_doc2=d.procDoc(xml_doc)
	print xml_doc2.encode("UTF-8")

	d1=DocPOSTagger()
	d1.setRegion(region_list=[u'<title>::</title>',u'<text>::</text>'])
	d1.setBoundary(boundary='|||')
	d1.setMask('<[^>]+>')
	xml_doc3=d1.procDoc(xml_doc2)
	print xml_doc3.encode("UTF-8")


