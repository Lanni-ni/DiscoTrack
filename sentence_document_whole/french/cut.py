import csv
import os
import re

input_file = "/Users/lanybu/PythonProject3/sentence_document_dev/french/document_level.tsv"
output_file = "/Users/lanybu/PythonProject3/sentence_document_dev/french/document_level_short.tsv"

# 切分句子：句号/问号/感叹号后断句
def split_sentences(text):
    return re.split(r'(?<=[\.\!\?])\s+', text)

with open(input_file, 'r', encoding='utf-8') as fin, \
     open(output_file, 'w', encoding='utf-8') as fout:

    reader = csv.DictReader(fin, delimiter='\t')
    writer = csv.DictWriter(fout, fieldnames=["doc_id", "text"], delimiter='\t')
    writer.writeheader()

    for row in reader:
        doc_id = row["doc_id"]
        full_text = row["text"].strip()

        sentences = split_sentences(full_text)
        target_char_len = len(full_text) // 3

        selected = []
        current_len = 0
        for s in sentences:
            if current_len >= target_char_len:
                break
            selected.append(s)
            current_len += len(s)

        short_text = " ".join(selected).strip()
        writer.writerow({"doc_id": doc_id, "text": short_text})