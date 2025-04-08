from datasets import Dataset, Features, Sequence, Value, ClassLabel
from math import ceil

class TokenLabelAligner:
    def __init__(self, tokenizer, label2id=None):
        self.tokenizer = tokenizer
        self.label2id = label2id
        self.id2label = {v: k for k, v in label2id.items()} if label2id else None

    def _extract_label2id(self, tags_list):
        unique_labels = sorted(set(tag for tags in tags_list for tag in tags), key=lambda x: (x != "O", x))
        self.label2id = {label: idx for idx, label in enumerate(unique_labels)}
        self.id2label = {idx: label for label, idx in self.label2id.items()}

    def prepare_hf_dataset(self, tokens_list, tags_list):
        if self.label2id is None:
            self._extract_label2id(tags_list)

        features = Features({
            "tokens": Sequence(Value("string")),
            "ner_tags": Sequence(ClassLabel(names=[label for label in self.label2id])),
            "id": Value("int32")
        })

        data = {
            "id": list(range(len(tokens_list))),
            "tokens": tokens_list,
            "ner_tags": [[self.label2id[tag] for tag in tags] for tags in tags_list],
        }

        return Dataset.from_dict(data, features=features)

    def tokenize_and_align(
        self,
        tokens_list,
        tags_list,
        truncation=False,
        label_all_tokens=False,
        padding=True,
        batch_size=32,
        return_dataset=False
    ):
        assert len(tokens_list) == len(tags_list), "Tokens and tags must have the same number of sequences."
        for tokens, tags in zip(tokens_list, tags_list):
            assert len(tokens) == len(tags), "Each sequence of tokens must match the sequence length of tags."

        if self.label2id is None:
            self._extract_label2id(tags_list)

        all_encoded = {
            "input_ids": [],
            "attention_mask": [],
            "labels": []
        }

        num_batches = ceil(len(tokens_list) / batch_size)
        for i in range(num_batches):
            batch_tokens = tokens_list[i * batch_size: (i + 1) * batch_size]
            batch_tags = tags_list[i * batch_size: (i + 1) * batch_size]

            batch_encodings = self.tokenizer(
                batch_tokens,
                is_split_into_words=True,
                truncation=truncation,
                padding=padding,
                return_token_type_ids=False,
                return_attention_mask=True,
                return_offsets_mapping=False
            )

            for j, word_ids in enumerate(batch_encodings.word_ids(batch_index=k) for k in range(len(batch_tokens))):
                previous_word_idx = None
                label_ids = []
                original_labels = [self.label2id[tag] for tag in batch_tags[j]]

                for word_idx in word_ids:
                    if word_idx is None:
                        label_ids.append(-100)
                    elif word_idx != previous_word_idx:
                        label_ids.append(original_labels[word_idx])
                    else:
                        label_ids.append(original_labels[word_idx] if label_all_tokens else -100)
                    previous_word_idx = word_idx

                all_encoded["input_ids"].append(batch_encodings["input_ids"][j])
                all_encoded["attention_mask"].append(batch_encodings["attention_mask"][j])
                all_encoded["labels"].append(label_ids)

        if return_dataset:
            hf_ds = self.prepare_hf_dataset(tokens_list, tags_list)
            hf_ds = hf_ds.add_column("input_ids", all_encoded["input_ids"])
            hf_ds = hf_ds.add_column("attention_mask", all_encoded["attention_mask"])
            hf_ds = hf_ds.add_column("labels", all_encoded["labels"])
            return hf_ds

        return all_encoded