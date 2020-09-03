# people_daily-ner-pretreatment
人民日报命名实体识别数据集预处理程序，生成BMES标记的数据，并保留分词信息、词性标注信息。renminribao NER pretreatment.
注： 忽然发现原来fastnlp已经给了人民日报的bio标注版本，下载地址：[fastnlp人民日报ner数据集](http://212.129.155.247/dataset/peopledaily.zip)，后续只要进行bio到bmeso的处理就行了。如果用fastnlp提供的版本，直接把 bio2bmeso.py文件放到解压后的文件夹里，执行就可以得到目标文件。

## 获取数据集处理成conll格式
参考[howl-anderson的教程](https://github.com/howl-anderson/tools_for_corpus_of_people_daily)，分别执行前两步编码格式更改与原始语料库解析

## 由conll格式数据生成char_ner.bmes文件
下载本项目中的conll2bmes.py文件，并放在[howl-anderson的教程](https://github.com/howl-anderson/tools_for_corpus_of_people_daily)项目解压后的根目录，与其他py文件同级，执行conll2bmes.py文件，生成bmes编码的ner数据。conll2bmes文件在split_data.py与conll_to_char_crfppp.py文件的基础上进行修改，在此感谢howl-anderson同学。
