# people_daily-ner-pretreatment
人民日报命名实体识别数据集预处理程序，生成BMES标记的数据，并保留分词信息、词性标注信息。renminribao NER pretreatment.

## 获取数据集处理成conll格式
参考[howl-anderson的教程](https://github.com/howl-anderson/tools_for_corpus_of_people_daily)，分别执行前两步编码格式更改与原始语料库解析

## 由conll格式数据生成char_ner.bmes文件
下载本项目中的conll2bmes.py文件，并放在[howl-anderson的教程](https://github.com/howl-anderson/tools_for_corpus_of_people_daily)项目解压后的根目录，与其他py文件同级，执行conll2bmes.py文件，生成bmes编码的ner数据。conll2bmes文件在split_data.py与conll_to_char_crfppp.py文件的基础上进行修改，在此感谢howl-anderson同学。
