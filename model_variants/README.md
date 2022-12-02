# Model Variants

This directory is for different backbones used for learning stage of active learning. In total we tested 3 models, GCN, GAT, and SGC.

## Usage

All following procedures should be run using conda virtual environment.

### GCN

For GCN backbone (main algorithm), refer to the folder DS-AGE

### GAT

```bash
conda env create -f age_gat.yml
conda activate age_gat
# in repo GAT
# example model usage follows:
python gat.py [your-dataset] [your-active-learning-score]
```

### SGC

```bash
conda env create -f age_sgc.yml
conda activate age_sgc
# in repo SGC
# example model usage follows:
python citation.py cora [your-dataset] [your-active-learning-score]
```

## Options

For this section, the available options for [your-dataset] includes "cora" and "citeseer".

The availale options for [your-active-learning-score] includes "baseline" (AGE), "f_similarity" (AGE+FDS), "s_similarity" (AGE+SDS), "e_similarity" (AGE+EDS), and "combined" (AGE+FDS+SDS).

Feel free to include your own datasets and your own score designs in the code.
