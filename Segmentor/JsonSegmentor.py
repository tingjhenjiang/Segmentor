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
from DocSegmentor import *
from Struct import *

## set ../Data directory as default model directory 

__default_model_dir__=os.path.abspath(os.path.dirname(__file__)+'/Data')

class JsonPOSTagger(DocPOSTagger):
	def procJson(self, js_obj, keyL=[]):
		for key in keyL:
			doc=js_obj.get(key,u'')
			js_obj[key]=self.procDoc(doc)
		return js_obj

class JsonSegmentor(DocSegmentor):
	def procJson(self, js_obj, keyL=[]):
		for key in keyL:
			doc=js_obj.get(key,u'')
			js_obj[key]=self.procDoc(doc)
		return js_obj


if __name__=="__main__":

	JsonObj={'RawText':u'''\
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
'''}

	a=JsonSegmentor(postag=True)
	a.setMask('<[^>]+>')
	a.setRegion(region_list=[u'<title>::</title>',u'<text>::</text>'])
	xml_doc1=a.procJson(JsonObj, ['RawText'])
	print(json.dumps(xml_doc1,ensure_ascii=False, indent=4).encode("UTF-8"))

