import os


sentence_file = "sentence_level.tsv"
document_file = "document_level.tsv"

# 数据目录
base_path = "/Users/lanybu/PythonProject3/entity tracking/coref/CorefUD_Spanish-AnCora"
splits = ["train", "dev"]

doc_texts = {}
sentence_rows = []

for split in splits:
    conllu_path = os.path.join(base_path, f"es_ancora-corefud-{split}.conllu")

    with open(conllu_path, 'r', encoding='utf-8') as f:
        current_doc = None
        current_sent_id = None
        current_text = None

        for line in f:
            line = line.strip()

            if line.startswith("# newdoc id ="):
                current_doc = line.split("=", 1)[1].strip()
                if current_doc not in doc_texts:
                    doc_texts[current_doc] = []

            elif line.startswith("# sent_id ="):
                current_sent_id = line.split("=", 1)[1].strip()

            elif line.startswith("# text ="):
                current_text = line.split("=", 1)[1].strip()
                if current_doc and current_sent_id:
                    doc_texts[current_doc].append(current_text)
                    sentence_rows.append((current_doc, current_sent_id, current_text))


# 写入 sentence-level 文件
with open(sentence_file, "w", encoding="utf-8") as f:
    f.write("doc_id\tsent_id\tsentence\n")
    for doc_id, sent_id, sent_text in sentence_rows:
        f.write(f"{doc_id}\t{sent_id}\t{sent_text}\n")

# 写入 document-level 文件
with open(document_file, "w", encoding="utf-8") as f:
    f.write("doc_id\ttext\n")
    for doc_id, sentence_list in doc_texts.items():
        full_text = " ".join(sentence_list)
        f.write(f"{doc_id}\t{full_text}\n")