# DS-AGE-Heterophily

This code is modified based on the AGE algorithm proposed in https://arxiv.org/abs/1705.05085 using GCN-cheby model.

## Dependencies

networkx==2.6.3

numpy==1.21.6

scikit_learn==1.1.1

scipy==1.4.1

tensorflow==2.8.2

## Usage

```# In the algcn folder
python train_entropy_density_graphcentral_ts.py [your-active-learning-score] [initial-number-of-labels] [number-of-classes] [your-dataset]
```

## Options

For this section, the available options for [your-dataset] includes "chameleon", "squirrel", "taxas", "cornell", and "wisconsin".

The last three datasets are just toy examples which include hundred of nodes only.

The availale options for [your-active-learning-score] includes "baseline" (AGE), "f_similarity" (AGE+FDS), "s_similarity" (AGE+SDS), "e_similarity" (AGE+EDS), "combined" (AGE+FDS+SDS), "random" (None), "c_only" (Centrality), "e_only" (Entropy), "fs_only" (FDS), "ss_only" (SDS), and "es_only" (EDS).

The default value for [initial-number-of-labels] is 4.

Feel free to include your own datasets and your own score designs in the code.
