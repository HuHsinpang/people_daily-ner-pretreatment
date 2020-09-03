import glob

def BIO2BMESO(input_file):
    print("Convert BIO -> BIOES for file:", input_file)

    with open(input_file,'r') as in_file, open(input_file.rstrip('.txt')+'.bmes', 'w') as fout:
        words, labels = [], []
        for line in in_file.readlines():
            if len(line) < 3:
                sent_len = len(words)
                for idx in range(sent_len):
                    if "-" not in labels[idx]:
                        fout.write(words[idx]+" "+labels[idx]+"\n")
                    else:
                        label_type = labels[idx].split('-')[-1]
                        if "B-" in labels[idx]:
                            if (idx == sent_len - 1) or ("I-" not in labels[idx+1]):
                                fout.write(words[idx]+" S-"+label_type+"\n")
                            else:
                                fout.write(words[idx]+" B-"+label_type+"\n")
                        elif "I-" in labels[idx]:
                            if (idx == sent_len - 1) or ("I-" not in labels[idx+1]):
                                fout.write(words[idx]+" E-"+label_type+"\n")
                            else:
                                fout.write(words[idx]+" M-"+label_type+"\n")
                fout.write('\n')
                words = []
                labels = []
            else:
                pair = line.strip('\n').split()
                words.append(pair[0])
                labels.append(pair[-1].upper())

    print("BIOES file generated:")


def main():
    for file in glob.glob('./*.txt'):
        BIO2BMESO(file)


if __name__ == "__main__":
    main()