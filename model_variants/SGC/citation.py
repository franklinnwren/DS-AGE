import time
import argparse
import numpy as np
import torch
import torch.nn.functional as F
import torch.optim as optim
from utils import load_citation, sgc_precompute, set_seed
from models import get_model
from metrics import accuracy
import pickle as pkl
from args import get_citation_args
from time import perf_counter

import scipy as sc
from scipy import stats
from sklearn.metrics import f1_score
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
import sklearn
import sys

seed = 123
np.random.seed(seed)
torch.manual_seed(123)

# Arguments
args = get_citation_args(sys.argv[1])
print(torch.cuda.is_available())
print(torch.cuda.current_device())

if args.dataset == 'cora':
    NL = 140
    NCL = 7
    if sys.argv[2] != 'combined':
      basef = 0.99
    else:
      basef = 0.95
    
elif args.dataset == 'citeseer':
    NL = 120
    NCL = 6
    if sys.argv[2] != 'combined':
      basef = 0.9
    else:
      basef = 0.85
else:
    raise NotImplementedError('Invalid dataset')

def train_regression(model,
                     train_features, train_labels,
                     val_features, val_labels,
                     epochs=args.epochs, weight_decay=args.weight_decay,
                     lr=args.lr, dropout=args.dropout):

    optimizer = optim.Adam(model.parameters(), lr=lr,
                           weight_decay=weight_decay)
    t = perf_counter()
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        output = model(train_features)
        loss_train = F.cross_entropy(output, train_labels)
        loss_train.backward()
        optimizer.step()
    train_time = perf_counter()-t

    with torch.no_grad():
        model.eval()
        output = model(val_features)
        acc_val = accuracy(output, val_labels)

    return model, acc_val, train_time

def test_regression(model, test_features, test_labels):
    model.eval()
    return accuracy(model(test_features), test_labels)

def sample_mask(idx, l):
    """Create mask."""
    mask = np.zeros(l)
    mask[idx] = 1
    return np.array(mask, dtype=bool)

#calculate the percentage of elements smaller than the k-th element
def perc(input,k): return sum([1 if i else 0 for i in input<input[k]])/float(len(input))

#calculate the percentage of elements larger than the k-th element
def percd(input,k): return sum([1 if i else 0 for i in input>input[k]])/float(len(input))


normcen = np.loadtxt("res/"+ args.dataset +"/graphcentrality/normcen")
cenperc = np.asarray([perc(normcen,i) for i in range(len(normcen))])

def train_AL(model,
             features, labels, idx_train, idx_val, idx_test, message_passing, raw_features,
             epochs=args.epochs, weight_decay=args.weight_decay,
             lr=args.lr):
    optimizer = optim.Adam(model.parameters(), lr=lr,
                           weight_decay=weight_decay)
    t = perf_counter()
    softmax = torch.nn.Softmax(dim=1)
    message_passing = message_passing.detach().to('cpu').to_dense().numpy()
    for epoch in range(epochs):
        gamma = np.random.beta(1, 1.005 - basef ** epoch)
        if sys.argv[2] == 'baseline':
          alpha = beta = delta = epsilon = (1-gamma)/2
        elif sys.argv[2] == 'combined':
          alpha = beta = delta = epsilon = (1-gamma)/4
        else:
          alpha = beta = delta = epsilon = (1-gamma)/3
        
        model.train()
        optimizer.zero_grad()
        output = model(features)
        loss_train = F.cross_entropy(output[idx_train], labels[idx_train])
        loss_train.backward()
        optimizer.step()

        embs = softmax(output).cpu().detach().numpy()
        if len(idx_train) < NL:
            curr_features = raw_features[idx_train, :]
            curr_features = sklearn.preprocessing.normalize(curr_features)
            raw_features = sklearn.preprocessing.normalize(raw_features)
            similarity = []
            for i in curr_features:
              similarity.append(np.dot(raw_features, np.squeeze([i])))
            similarity = np.squeeze(np.array(similarity))
            max_similarity = np.max(similarity, axis=0)
            simprec = np.asarray([percd(max_similarity,i) for i in range(len(max_similarity))])

            curr_embeddings = output.to('cpu').detach().numpy()[idx_train, :]
            curr_embeddings = sklearn.preprocessing.normalize(curr_embeddings)
            raw_embeddings = sklearn.preprocessing.normalize(output.to('cpu').detach().numpy())
            em_similarity = []
            for i in curr_embeddings:
              em_similarity.append(np.dot(raw_embeddings, np.squeeze([i])))
            em_similarity = np.squeeze(np.array(em_similarity))
            max_em_similarity = np.max(em_similarity, axis=0)
            em_simprec = np.asarray([percd(max_em_similarity,i) for i in range(len(max_em_similarity))])

            connectivity = message_passing[idx_train, :]
            max_connectivity = np.squeeze(np.array(np.max(connectivity, axis=0)))
            connprec = np.asarray([percd(max_connectivity,i) for i in range(len(max_connectivity))])

            entropy = sc.stats.entropy(embs.T)
            # entropy[train_mask+val_mask+test_mask]=-100
            entrperc = np.asarray([perc(entropy, i) for i in range(len(entropy))])
            kmeans = KMeans(n_clusters=NCL, random_state=0).fit(embs)
            ed = euclidean_distances(embs, kmeans.cluster_centers_)
            ed_score = np.min(ed, axis=1)
            edprec = np.asarray([percd(ed_score, i) for i in range(len(ed_score))])
            if sys.argv[2] == 'baseline':
              finalweight = alpha*entrperc + beta*edprec + gamma*cenperc
              print("entropy weight: ", alpha, " density weight: ", beta, "centrality weight: ", gamma)
            elif sys.argv[2] == 'f_similarity':
              finalweight = alpha*entrperc + beta*edprec + gamma*cenperc + delta*simprec
              print("entropy weight: ", alpha, " density weight: ", beta, " centrality weight: ", gamma, " feature similarity weight: ", delta)
            elif sys.argv[2] == 's_similarity':
              finalweight = alpha*entrperc + beta*edprec + gamma*cenperc + delta*connprec
              print("entropy weight: ", alpha, " density weight: ", beta, " centrality weight: ", gamma, " structural similarity weight: ", delta)
            elif sys.argv[2] == 'e_similarity':
              finalweight = alpha*entrperc + beta*edprec + gamma*cenperc + delta*em_simprec
              print("entropy weight: ", alpha, " density weight: ", beta, " centrality weight: ", gamma, " embedding similarity weight: ", delta)
            else:
              finalweight = alpha*entrperc + beta*edprec + gamma*cenperc + delta*connprec + epsilon*simprec
              print("entropy weight: ", alpha, " density weight: ", beta, " centrality weight: ", gamma, " stuructural similarity weight: ", delta, " feature similarity weight: ", epsilon)
            finalweight[idx_train] = -100
            finalweight[idx_test] = -100
            finalweight[idx_val] = -100
            select = np.argmax(finalweight)
            idx_train.append(select)
        # else:
        #     print('finish select!')

        # print('Epoch: ' + str(epoch) + " loss: " + str(loss_train))

    train_time = perf_counter() - t

    with torch.no_grad():
        model.eval()
        output = model(features[idx_test])
        y_pred = torch.argmax(output, dim=1).cpu()
        y_true = labels[idx_test].cpu()
        macrof1 = f1_score(y_true, y_pred, average='macro')
        microf1 = f1_score(y_true, y_pred, average='micro')

        print("macro {}".format(macrof1))
        print("micro {}".format(microf1))

    return model, train_time, macrof1, microf1

'''
if args.model == "SGC":
    model, acc_val, train_time = train_regression(model, features[idx_train], labels[idx_train], features[idx_val], labels[idx_val],
                     args.epochs, args.weight_decay, args.lr, args.dropout)
    acc_test = test_regression(model, features[idx_test], labels[idx_test])

    print("Validation Accuracy: {:.4f} Test Accuracy: {:.4f}".format(acc_val, acc_test))
    print("Pre-compute time: {:.4f}s, train time: {:.4f}s, total: {:.4f}s".format(precompute_time, train_time, precompute_time+train_time))
'''

if args.tuned:
    if args.model == "SGC":
        with open("{}-tuning/{}.txt".format(args.model, args.dataset), 'rb') as f:
            args.weight_decay = pkl.load(f)['weight_decay']
            print("using tuned weight decay: {}".format(args.weight_decay))
    else:
        raise NotImplemented


# setting random seeds
def one_pass(iter):
    set_seed(args.seed, args.cuda)

    adj, features, labels, idx_train, idx_val, idx_test = \
        load_citation(args.dataset, args.normalization, args.cuda, iter=iter)
    message_passing = adj * adj
  
    # Some preprocessing
    raw_features = features.to('cpu').numpy()
    print(raw_features.shape)
    model = get_model(args.model, features.size(1), labels.max().item()+1, args.hidden, args.dropout, args.cuda)

    if args.model == "SGC":
        features, precompute_time = sgc_precompute(features, adj, args.degree)
        print("{:.4f}s".format(precompute_time))

    idx_train = idx_train.tolist()
    idx_val = idx_val.tolist()
    idx_test = idx_test.tolist()
    _, _, mac, mic = train_AL(model, features, labels, idx_train, idx_val, idx_test, message_passing, raw_features)
    return mac, mic


if __name__ == "__main__":
    mac_list, mic_list = [], []
    for i in range(11):
        mac, mic = one_pass(i)
        mac_list.append(mac)
        mic_list.append(mic)
    print(mac_list)
    print(mic_list)
    print("Average of macrof1 is {}".format(sum(mac_list) / 11))
    print("Average of microf1 is {}".format(sum(mic_list) / 11))
