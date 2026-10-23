import csv

# ✅ 你所有要处理的 conllu 文件路径列表
input_conllu_files = [
    "/Users/lanybu/PythonProject3/discourse relation/disrpt/eng.erst.gum/eng.erst.gum_dev.conllu",
    "/Users/lanybu/PythonProject3/discourse relation/disrpt/eng.erst.gum/eng.erst.gum_train.conllu",
]

output_tsv = "tokens_output.tsv"  # 输出的 tsv 文件路径

rows = []

for input_conllu in input_conllu_files:
    doc_id = None
    sent_id = None
    tokens = []

    with open(input_conllu, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# newdoc id"):
                if doc_id and sent_id and tokens:
                    rows.append([doc_id, sent_id, str(tokens)])
                    tokens = []
                doc_id = line.split("=", 1)[1].strip()
            elif line.startswith("# sent_id"):
                if sent_id and tokens:
                    rows.append([doc_id, sent_id, str(tokens)])
                    tokens = []
                sent_id = line.split("=", 1)[1].strip()
            elif not line or line.startswith("#"):
                continue
            else:
                cols = line.split("\t")
                if "-" in cols[0]:
                    continue
                tokens.append(cols[1])

    # 最后一组别忘记保存
    if doc_id and sent_id and tokens:
        rows.append([doc_id, sent_id, str(tokens)])

# ✅ 写入 TSV 文件
with open(output_tsv, "w", encoding="utf-8", newline="") as out:
    writer = csv.writer(out, delimiter="\t")
    writer.writerow(["doc_id", "sent_id", "tokens"])
    writer.writerows(rows)