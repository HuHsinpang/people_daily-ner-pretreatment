# ****************************************************************************** #
#                           BosonNER Data Pretreatment                           #
#                                                                                #
#  Author: Hsinpang    Email:hsinpang@alumni.hust.edu.cn   Time:2020.6.24        #
#  Envirenment: linux, python3.x, tokenizer_tools0.9.0                           #
#                                                                                #
# ****************************************************************************** #

# !/usr/bin/python
# -*-coding:utf-8 -*-
import os
import random
random.seed(0)
import utils
from nltk.util import LazyMap
from nltk.corpus.reader.conll import ConllCorpusReader
from tokenizer_tools.tagset.NER.BILUO import BILUOEncoderDecoder

current_dir = os.path.dirname(os.path.abspath(__file__))


# ****************************************************************************** #
#                               源目文件存储位置及配置                              #
# ****************************************************************************** #
# conll source file
conll_root = os.path.join(current_dir, './data/conllu')
utils.create_if_dir_not_exists(conll_root)
fileids=['data_False-True-True-True-True-True-False.conllu']
# conll file column info
columntypes=(
    ConllCorpusReader.IGNORE,
    ConllCorpusReader.WORDS,
    ConllCorpusReader.POS,
    ConllCorpusReader.NE,
    ConllCorpusReader.IGNORE
)

# step1: split data storage
split_data_dir = os.path.join(current_dir, 'data', 'split_data')
utils.create_if_dir_not_exists(split_data_dir)

# step2: BMES char file storage
token_dir = os.path.join(current_dir, 'data/split_char_crfpp')
utils.create_if_dir_not_exists(token_dir)


# ****************************************************************************** #
#                              现有类的继承与方法的重写                              #
# ****************************************************************************** #
class ConllPosNeReader(ConllCorpusReader):
    def _get_tagged_words(self, grid, tagset=None):
        pos_tags = self._get_column(grid, self._colmap['pos'])
        ne_tags = self._get_column(grid, self._colmap['ne'])
        if tagset and tagset != self._tagset:
            pos_tags = [map_tag(self._tagset, tagset, t) for t in pos_tags]
        return list(zip(self._get_column(grid, self._colmap['words']), pos_tags, ne_tags))

    def tagged_sents(self, fileids=None, tagset=None):
        self._require(self.WORDS, self.POS, self.NE)

        def get_tagged_words(grid):
            return self._get_tagged_words(grid, tagset)

        return LazyMap(get_tagged_words, self._grids(fileids))


class BMESEncoderDecoder(BILUOEncoderDecoder):
    def encode(self, sequence):
        len_of_sequence = len(sequence)

        if len_of_sequence == 1:
            return [self.generate_tag('S')]

        elif len_of_sequence == 2:
            return [self.generate_tag('B'), self.generate_tag('E')]

        else:
            return [self.generate_tag('B')] + [self.generate_tag('M')] * (len_of_sequence - 2) + [self.generate_tag('E')]


# ****************************************************************************** #
#               数据处理的两步流程：conll数据的切分；标注内容的处理                     #
# ****************************************************************************** #
class DataSplitter:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.corpus_reader = ConllPosNeReader(conll_root, fileids, columntypes)

    def split_data(self, train=0.90, dev=0.00):
        sent_list = []
        for sent in self.corpus_reader.tagged_sents():
            sent_list.append(sent)

        random.shuffle(sent_list)

        sent_list_len = len(sent_list)

        train_set_len = int(sent_list_len * train)
        dev_set_len = int(sent_list_len * dev)
        test_set_len = sent_list_len - train_set_len - dev_set_len

        train_set = sent_list[:train_set_len]
        dev_set = sent_list[train_set_len: train_set_len + dev_set_len]
        test_set = sent_list[- test_set_len:]

        self.write_data(train_set, 'train')
        self.write_data(dev_set, 'dev')
        self.write_data(test_set, 'test')

    def write_data(self, data, data_set_name):
        output_file = self.get_output_file(data_set_name)

        with open(output_file, 'w') as fd:
            for sent in data:
                for id, token_and_more in enumerate(sent, start=1):
                    fd.write("\t".join([str(id)] + list(token_and_more)) + "\n")
                fd.write('\n')

    def get_output_file(self, data_set_name):
        return os.path.join(self.output_dir, data_set_name + '.conllu')


def split2bmes(delimit=" "):
    encoder_cache = {}
    for split_root, dirs, files in os.walk(split_data_dir):
        for file_ in files:

            # ignore hidden file
            if os.path.basename(file_).startswith('.'):
                continue

            corpus_reader = ConllPosNeReader(split_root, [file_], columntypes)

            output_file = 'people.'+os.path.splitext(file_)[0] + '.bmes'

            with open(os.path.join(token_dir, output_file), 'w') as fd:
                for word_tag_pair_list in corpus_reader.tagged_sents():
                    for word, pos, tag in word_tag_pair_list:
                        if tag not in encoder_cache:
                            encoder_cache[tag] = BMESEncoderDecoder(tag)

                        encoder = encoder_cache[tag]
                        coding = encoder.encode(word)
                        char_position_in_word, word_pos = [str(i) for i in range(len(word))], [pos for i in range(len(word))]

                        word_coding_pair_list = zip(word, word_pos, char_position_in_word, coding)   # 符号^作为一个占位符

                        for word_coding_pair in word_coding_pair_list:
                            fd.write(delimit.join(word_coding_pair) + "\n")
                    fd.write('\n')


if __name__ == "__main__":
    # step one：数据切分
    data_splitter = DataSplitter(split_data_dir)
    data_splitter.split_data()
    
    # step two: 数据标注处理
    split2bmes()
