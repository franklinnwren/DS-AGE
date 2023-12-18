# DS-AGE 

This code is modified based on the AGE algorithm proposed in https://arxiv.org/abs/1705.05085 using GCN model.

## Dependencies

networkx==2.6.3

numpy==1.21.6

scikit_learn==1.1.1

scipy==1.4.1

tensorflow==2.8.2

## Usage

```# In the algcn folder
python train_entropy_density_graphcentral_ts.py
    --dataset [your_dataset_name]
    --method [your_method]
    --learning_rate [your_learning_rate]
    --epochs [num_epochs]
    --hidden1 [num_hidden_units]
    --dropout [dropout_value]
    --weight_decay [weight_decay_value]
    --early_stopping [early_stopping_value]
    --max_degree [max_degree_value]
    --inicount [inicount_value]
    --num_classes [num_classes_value]
    --model [your_model_type]
```

## Options

For this section, the available options for [your-dataset] include "cora", "citeseer" and "pubmed".

The available options for [your-active-learning-score] includes "all" "se_similarity" "fe_similarity" "fs_similarity" "e_similarity" "s_similarity" "f_similarity" "baseline"

The default value for [your_dataset_name] is 'cora'.
The default value for [your_method] is "all".
The default value for [your_learning_rate] is 0.01.
The default value for [num_epochs] is 300.
The default value for [num_hidden_units] is 16.
The default value for [dropout_value] is 0.5.
The default value for [weight_decay_value] is 5e-4.
The default value for [early_stopping_value] is 5.
The default value for [max_degree_value] is 3.
The default value for [inicount_value] is 4.
The default value for [num_classes_value] is 6.
The default value for [your_model_type] is 'gcn'.
