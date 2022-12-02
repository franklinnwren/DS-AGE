# Dissimilar Nodes Improve Graph Active Learning

Code for the paper "Dissimilar Nodes Improve Graph Active Learning", in NeurIPS 2022 Workshop GLFrontiers.

Feel free to check out our paper at https://openreview.net/pdf?id=oyCzkPJTm3f

Cite as

@inproceedings{

ren2022dissimilar,

title={Dissimilar Nodes Improve Graph Active Learning},

author={Zhicheng Ren and Yifu Yuan and Yuxin Wu and Xiaxuan Gao and YEWEN WANG and Yizhou Sun},

booktitle={NeurIPS 2022 Workshop: New Frontiers in Graph Learning},

year={2022},

url={https://openreview.net/forum?id=oyCzkPJTm3f}

}

## Introduction

In this paper, we introduce a novel active learning concept, dissimilarity, and propose three scoring functions based on this idea: feature dissimilarity score (FDS), structure dissimilarity score (SDS), and embedding dissimilarity score (EDS).

Our experimental results shows that our proposed method could boost the performance of node classification tasks of Graph Convolutional Networks by about 2.1% when the number of labels is fixed.

We also provide an ablation study to show that our methods are generalizable to many other GNN variants.

We examine the effectiveness of our AL scoring functions on heterophilic datasets.

## Descriptions

Folder "DS-AGE" is our main algorithm, which incorporate our dissimilarity scores into the active learning framework based on GCN backbone.

Folder "model_variants" includes implementation of other GNN-variants which is adaptable for our main algorithm.

Folder "AGE-Heterophily" includes experiments on heterophilic datasets.

And folder "KMedoids" includes ablation studies about the choice of clustering algorithms.
