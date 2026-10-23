import os

dep_dir = "/Users/lanybu/PythonProject3/entity tracking/dep"
sentence_file = "sentence_level.tsv"
document_file = "document_level.tsv"

genres_with_speaker = {"conversation", "court", "interview", "podcast", "speech", "vlog"}

doc_texts = {}
sentence_rows = []

for filename in sorted(os.listdir(dep_dir)):
    if not filename.endswith(".conllu") or not filename.startswith("GUM_") or filename.startswith("GUM_reddit_"):
        continue
    filepath = os.path.join(dep_dir, filename)
    doc_id = filename.replace(".conllu", "")

    current_genre = None
    current_speaker = None
    current_sent_id = None
    current_text = None

    if doc_id not in doc_texts:
        doc_texts[doc_id] = []

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# meta::genre ="):
                current_genre = line.split("=", 1)[1].strip()
            elif line.startswith("# sent_id ="):
                current_sent_id = line.split("=", 1)[1].strip()
            elif line.startswith("# speaker ="):
                current_speaker = line.split("=", 1)[1].strip()
            elif line.startswith("# text ="):
                current_text = line.split("=", 1)[1].strip()
                if current_genre in genres_with_speaker and current_speaker:
                    sent_text = f"[Speaker: {current_speaker}] {current_text}"
                else:
                    sent_text = current_text
                doc_texts[doc_id].append(sent_text)
                sentence_rows.append((doc_id, current_sent_id, sent_text))

with open(sentence_file, "w", encoding="utf-8") as f:
    f.write("doc_id\tsent_id\tsentence\n")
    for doc_id, sent_id, sent_text in sentence_rows:
        f.write(f"{doc_id}\t{sent_id}\t{sent_text}\n")

with open(document_file, "w", encoding="utf-8") as f:
    f.write("doc_id\ttext\n")
    for doc_id, sentence_list in doc_texts.items():
        full_text = " ".join(sentence_list)
        f.write(f"{doc_id}\t{full_text}\n")

print(f"Total documents: {len(doc_texts)}")