# -*- coding: utf-8 -*-
# file: ssp.py
# time: 23:27 17/02/2025
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# Homepage: https://yangheng95.github.io
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2025. All Rights Reserved.
import os

import autocuda
import torch
from metric_visualizer import MetricVisualizer

from omnigenome import OmniGenomeDatasetForTokenClassification
from omnigenome import ClassificationMetric
from omnigenome import OmniSingleNucleotideTokenizer
from omnigenome import OmniGenomeModelForTokenClassification
from omnigenome import Trainer

# Predefined dataset label mapping
label2id = {"(": 0, ")": 1, ".": 2}

# The is FM is exclusively powered by the OmniGenome package
model_name_or_path = "anonymous8/OmniGenome-186M"

# Generally, we use the tokenizers from transformers library, such as AutoTokenizer
# tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)

# However, OmniGenome provides specialized tokenizers for genomic data, such as single nucleotide tokenizer and k-mers tokenizer
# we can force the tokenizer to be used in the model
tokenizer = OmniSingleNucleotideTokenizer.from_pretrained(model_name_or_path)

# We have implemented a diverse set of genomic models in OmniGenome, please refer to the documentation for more details
ssp_model = OmniGenomeModelForTokenClassification(
    model_name_or_path,
    tokenizer=tokenizer,
    label2id=label2id,
)

# necessary hyperparameters
epochs = 10
learning_rate = 2e-5
weight_decay = 1e-5
batch_size = 4
max_length = 512
seeds = [45]  # Each seed will be used for one run


# Load the dataset according to the path
train_file = "toy_datasets/Archive2/train.json"
test_file = "toy_datasets/Archive2/test.json"
valid_file = "toy_datasets/Archive2/valid.json"

train_set = OmniGenomeDatasetForTokenClassification(
    data_source=train_file,
    tokenizer=tokenizer,
    label2id=label2id,
    max_length=max_length,
)
test_set = OmniGenomeDatasetForTokenClassification(
    data_source=test_file,
    tokenizer=tokenizer,
    label2id=label2id,
    max_length=max_length,
)
valid_set = OmniGenomeDatasetForTokenClassification(
    data_source=valid_file,
    tokenizer=tokenizer,
    label2id=label2id,
    max_length=max_length,
)
train_loader = torch.utils.data.DataLoader(
    train_set, batch_size=batch_size, shuffle=True
)
valid_loader = torch.utils.data.DataLoader(valid_set, batch_size=batch_size)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=batch_size)

compute_metrics = [
    ClassificationMetric(ignore_y=-100).accuracy_score,
    ClassificationMetric(ignore_y=-100, average="macro").f1_score,
    ClassificationMetric(ignore_y=-100).matthews_corrcoef,
]


# Initialize the MetricVisualizer for logging the metrics
mv = MetricVisualizer(name="OmniGenome-186M-SSP")

for seed in seeds:
    optimizer = torch.optim.AdamW(
        ssp_model.parameters(), lr=learning_rate, weight_decay=weight_decay
    )
    trainer = Trainer(
        model=ssp_model,
        train_loader=train_loader,
        eval_loader=valid_loader,
        test_loader=test_loader,
        batch_size=batch_size,
        epochs=epochs,
        optimizer=optimizer,
        compute_metrics=compute_metrics,
        seeds=seed,
        device=autocuda.auto_cuda(),
    )

    metrics = trainer.train()
    # test_metrics = metrics["test"][-1]
    # mv.log(model_name_or_path.split("/")[-1], "F1", test_metrics["f1_score"])
    # mv.log(
    #     model_name_or_path.split("/")[-1],
    #     "Accuracy",
    #     test_metrics["accuracy_score"],
    # )
    # print(metrics)
    # mv.summary()

path_to_save = "OmniGenome-186M-SSP"
ssp_model.save(path_to_save, overwrite=True)

# Load the model checkpoint
ssp_model = ssp_model.load(path_to_save)
results = ssp_model.inference("CAGUGCCGAGGCCACGCGGAGAACGAUCGAGGGUACAGCACUA")
print(results["predictions"])
print("logits:", results["logits"])

# We can load the model checkpoint using the ModelHub
from omnigenome import ModelHub

ssp_model = ModelHub.load("OmniGenome-186M-SSP")
results = ssp_model.inference("CAGUGCCGAGGCCACGCGGAGAACGAUCGAGGGUACAGCACUA")
print(results["predictions"])
print("logits:", results["logits"])


examples = [
    "GCUGGGAUGUUGGCUUAGAAGCAGCCAUCAUUUAAAGAGUGCGUAACAGCUCACCAGC",
    "AUCUGUACUAGUUAGCUAACUAGAUCUGUAUCUGGCGGUUCCGUGGAAGAACUGACGUGUUCAUAUUCCCGACCGCAGCCCUGGGAGACGUCUCAGAGGC",
]

results = ssp_model.inference(examples)
structures = ["".join(prediction) for prediction in results["predictions"]]
print(results)
print(structures)