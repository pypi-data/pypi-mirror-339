# -*- coding: utf-8 -*-
# file: evaluation.py
# time: 00:02 08/04/2025
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2025. All Rights Reserved.
import findfile
import numpy as np

from omnigenome import RegressionMetric, ClassificationMetric

prediction_path = 'predictions'
ground_truth_path = 'ground_truth'

task2metric = {
    'RNA-mRNA': RegressionMetric().root_mean_squared_error,
    'RNA-SNMD': ClassificationMetric(average='macro').roc_auc_score,
    'RNA-SNMR': ClassificationMetric(average='macro').f1_score,
    'RNA-SSP-Archive2': ClassificationMetric(average='macro').f1_score,
    'RNA-SSP-rnastralign': ClassificationMetric(average='macro').f1_score,
    'RNA-SSP-bpRNA': ClassificationMetric(average='macro').f1_score,
    'DNA-Ineffective-Antibiotic': ClassificationMetric(average='macro').f1_score
}

for task in task2metric.keys():
    test_pred = findfile.find_cwd_file([prediction_path, task, 'test.npy'])
    test_gt = findfile.find_cwd_file([ground_truth_path, task, 'test.npy'])
    prediction = np.load(test_pred, allow_pickle=True).item()['pred'].reshape(-1)
    ground_truth = np.load(test_gt, allow_pickle=True).item()['true'].reshape(-1)
    mask = ground_truth != -100
    ground_truth = ground_truth[mask]
    prediction = prediction[mask]
    metric = task2metric[task](ground_truth, prediction)
    print(f"{task} : {metric}")