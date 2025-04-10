# -*- coding: utf-8 -*-
# file: merge_json.py
# time: 09:06 12/03/2025
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2025. All Rights Reserved.

import json

with open("solved_sequences.json", "r") as f:
    a = json.load(f)

with open("solved_sequences_legacy.json", "r") as f:
    b = json.load(f)
a.update(b)
print(len([v for v in a.values() if isinstance(v['best_sequence'], list)]))

with open("solved_sequences.json", "w") as f:
    json.dump(a, f)