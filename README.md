# 國教院中文斷詞系統

## 安裝
* 下載程式碼：

	```$ git clone https://github.com/naernlp/Segmentor```
    
* 下載斷詞及詞性標記模型：
	* 下載處：
		* [naer-segmentor-models-20160318.tar.gz](http://120.127.233.228/download/Segmentor/naer-segmentor-models-20160318.tar.gz)
	* 下載後於 Segmentor 目錄下解壓縮
*  安裝程式與資料：
	* 在 Segmentor 目錄下執行安裝：

	    ```
	    $ sudo python setup.py install
	    ```
	    
## 參數說明
```
Usage: naer_seg [options] input_file1[::output_file1] ...

Options:
  -h, --help            show this help message and exit
  -s SUFFIX, --suffix=SUFFIX
                        suffix for output file
  -m MODEL, --model=MODEL
                        directory of models for word segmention and POS
                        tagging
  -p, --postag          POS tagging switch
  -n, --disable-segment
                        segmentation switch
  -b BOUNDARY, --boundary=BOUNDARY
                        word boundary
  -f FORMAT, --format=FORMAT
                        output format for a tagged word
  --output-dir=OUTPUTDIR
                        save output files to specific directory
  -l LIST, --list=LIST  read input file list from file
  -v, --verbose         enable verbose mode
  -e ENCODING, --encoding=ENCODING
                        set input and output encoding
  --region=REGION       set processing region. e.g.
                        --region="<chtitle>::</chtitle>" will segment text
                        between <chtitle> and </chtitle> tags. "::" is the
                        separator of the start and end tags.
  --mask=MASK           set mask region which will not be processed. e.g.
                        --mask="<[^>]+>" will prevent html tags, such as <font
                        size="12">, to be segmented.
  -D DIRECTORY, --directory=DIRECTORY
                        set input (and output) directory. e.g.
                        --directory="dir1::dir2" will process files in dir1
                        and output to dir2.
  --exclude=EXCLUDE     set exclude regular expression.
  --include=INCLUDE     set include regular expression.
```
