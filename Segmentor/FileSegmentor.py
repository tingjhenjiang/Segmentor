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

import os,re,sys
import string
from DocSegmentor import *
from Struct import *

## set ../Data directory as default model directory 

__default_model_dir__=os.path.abspath(os.path.dirname(__file__)+'/../Data')

class FilePOSTagger(DocPOSTagger):
	def __init__(self, model_dir=__default_model_dir__):
		super(FilePOSTagger, self).__init__(model_dir)

	#def procFile(self, infile, outfile):


class FileSegmentor(DocSegmentor):
	def __init__(self, model_dir=__default_model_dir__, segment=True, postag=False, encoding='UTF-8'):
		super(FileSegmentor, self).__init__(model_dir, segment=segment, postag=postag)
		self.encoding=encoding
		self.outputdir=None
		self.suffix=".seg"
		self.line_mode=False

	def setOutputDir(self, outputdir):
		self.outputdir=outputdir

	def setSuffix(self, suffix):
		self.suffix=suffix

	def procFile(self, infile, outfile=None):
		#print "DEBUG:line_mode:%s"%(self.line_mode)
		if '::' in infile and outfile==None:
			L=infile.split('::')
			infile=L[0]
			outfile=L[1]

		if infile=="-":
			inf=sys.stdin
		elif not isinstance(infile,file):
			inf=open(infile)
		else:
			inf=infile

		if not outfile:
			outfile=infile+self.suffix
			if self.outputdir:
				outfile=os.path.join(self.outputdir,outfile.lstrip('/'))
				parentdir=os.path.dirname(outfile)
				if not os.path.exists(parentdir):
					os.makedirs(parentdir)
			outf=open(outfile,"w")
		elif outfile=="-":
			outf=sys.stdout
		elif not isinstance(outfile,file):
			outf=open(outfile,"w")
		else:
			outf=outfile

		if not self.line_mode:
			doc=inf.read().decode(self.encoding)
			seged_doc=self.procDoc(doc)
			outf.write(seged_doc.encode(self.encoding))
		else:
			for line in inf:
				line=line.decode(self.encoding)
				seged_line=self.procDoc(line)
				outf.write(seged_line.encode(self.encoding))

	def __gen_file_list(self, inputdir, outputdir=None, suffix=".seg",recursive=False, include=None, exclude=None):
		if not outputdir:
			outputdir=inputdir

		if recursive:
			for (dirpath, dirnames, filenames) in os.walk(inputdir):
				outdirpath=os.path.join(outputdir,dirpath[len(inputdir):].lstrip('/'))
				for filename in filenames:
					input=os.path.join(dirpath,filename)
					if include and not re.search(include, input):
						continue
					if exclude and re.search(exclude, input):
						continue
					output=os.path.join(outdirpath,filename+suffix)
					if not os.path.isfile(input):
						continue
					yield (input, output)
		else:
			for filename in os.listdir(inputdir): 
				input=os.path.join(inputdir,filename)
				output=os.path.join(outputdir, filename+suffix)
				if include and not re.search(include, input):
					continue
				if exclude and re.search(exclude, input):
					continue
				if not os.path.isfile(input):
					continue
				yield (input, output)

	def procDir(self, inputdir, outputdir=None, suffix=".seg", recursive=False, include=None, exclude=None, verbose=False):
		for (input, output) in self.__gen_file_list(inputdir, outputdir, suffix, recursive, include, exclude):
			outputdir=os.path.dirname(output)
			if not os.path.exists(outputdir):
				if verbose:
					sys.stderr.write('mkdir %s\n'%(outputdir))
				os.makedirs(outputdir)

			if verbose:
				sys.stderr.write("Processing %s (output %s) ... "%(input, output))

			self.procFile(input, output)

			if verbose:
				sys.stderr.write("done.\n")

if __name__=="__main__":
	a=FileSegmentor(postag=True)
	a.procDir(sys.argv[1], sys.argv[2], recursive=False, include='\.txt$', exclude='_big5', verbose=True)
