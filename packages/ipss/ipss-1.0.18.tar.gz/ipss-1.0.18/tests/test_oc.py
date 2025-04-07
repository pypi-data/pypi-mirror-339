# Analyze human cancer data from The Cancer Genome Atlas via LinkedOmics
# source: https://www.linkedomics.org/login.php

import random

from ipss import ipss
import numpy as np

from examples.load_cancer_data import load_data

# set random seed
np.random.seed(302)

# load data
cancer_type = 'ovarian'
feature_types = ['mirna']
response = ('clinical', 'Tumor_purity')

data = load_data(cancer_type, feature_types, response=response)
X, y, feature_names = data['X'], data['Y'], data['feature_names']

# run ipss
ipss_output = ipss(X,y)

# print q-values
q_value_threshold = 0.2
q_values = ipss_output['q_values']
sorted_features = sorted(q_values, key=q_values.get)
print(f'Top ranked microRNA by q-value')
print(f'--------------------------------')
for feature_index in sorted_features:
	q_value = q_values[feature_index]
	if q_value <= q_value_threshold:
		print(f'{feature_names[feature_index]}: {np.round(q_value,5)}')

print(f'')

# print efp scores
efp_score_threshold = 1
efp_scores = ipss_output['efp_scores']
sorted_features = sorted(efp_scores, key=efp_scores.get)
print(f'Top ranked microRNA by efp score')
print(f'----------------------------------')
for feature_index in sorted_features:
	efp_score = efp_scores[feature_index]
	if efp_score <= efp_score_threshold:
		print(f'{feature_names[feature_index]}: {np.round(efp_score,2)}')












