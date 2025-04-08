import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from torch.utils.data import TensorDataset, DataLoader

from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import numpy as np

from .base import Function


class MLP(nn.Module):
    def __init__(self, input_dim, search_space, **kwargs):
        super(MLP,self).__init__()

        self.input_layer    = nn.Linear(input_dim, search_space['hidden_size0'])
        self.hidden_layer1  = nn.Linear(search_space['hidden_size0'], search_space['hidden_size1'])
        self.output_layer   = nn.Linear(search_space['hidden_size1'], 3)

        self.learning_rate = kwargs.get('learning_rate', 1e-2)
        self.criterion = kwargs.get('criterion', nn.CrossEntropyLoss())
        self.optimiser = kwargs.get(
            'optimiser', 
            torch.optim.Adam(self.parameters(), lr=self.learning_rate)
        )
        self.n_epochs = kwargs.get('n_epochs', 100)
        self.batch_size = kwargs.get('batch_size', 128)

        self.score = kwargs.get('score', accuracy_score)

    def forward(self, x):
        x = F.relu(self.input_layer(x))
        x = F.relu(self.hidden_layer1(x))
        x = F.softmax(self.output_layer(x), dim=-1)
        return x
    
    def fit(self, X_train, y_train):

        dataset = TensorDataset(X_train, y_train)

        for _ in range(self.n_epochs):
            for X_batch, y_batch in DataLoader(dataset, batch_size=self.batch_size, shuffle=True, drop_last=True):
            
                y_pred = self(X_batch)
                loss = self.criterion(y_pred, y_batch)
                
                self.optimiser.zero_grad()
                loss.backward()
                self.optimiser.step()

    def val(self, x_test, y_test):
        pred = self(x_test)
        pred = pred.detach().numpy()
        return self.score(y_test, np.argmax(pred, axis=1))


class MLSolver(Function):
    def __init__(self, model, **kwargs):
        self.dim =           kwargs.get('dim', 2)
        self.domain =        kwargs.get('domain', np.array([[1, 100], [1, 100]]))
        self.name =          "NN hyperparams"
        self.glob_min =      np.array([120, 45])
        self.f =             lambda x: self.__call__(x)
        self.log_transform = kwargs.get('log_transform', True)
        self.log_eps =       kwargs.get('log_eps', 1e-8)
        self.sigma =         kwargs.get('sigma', 1e-1)
        self.n_obs =         13 * 3
        self.model =         model
        self.dataset =       kwargs.get('dataset', load_iris(return_X_y=True))
        self.minimise =      kwargs.get('minimise', True)
        self.seed =          kwargs.get('seed', 73)

        self.X = Variable(torch.from_numpy(self.dataset[0])).float()
        self.y = Variable(torch.from_numpy(self.dataset[1]))
    

    def __call__(self, neurons : np.array):

        x_train, x_test, y_train, y_test = train_test_split(self.X, self.y, random_state=self.seed, shuffle=True)
        outputs = []

        for pack in neurons:

            self.model.__init__(x_train.shape[-1], pack)

            self.model.fit(x_train, y_train)
            roc_auc_ = self.model.val(x_test, y_test)
            outputs.append(roc_auc_)

        if self.minimise:
            return -1.0 * np.array(outputs)
        else:
            return np.array(outputs)
    

    def sample(self, neurons):

        X, y = None, None

        for n in neurons:
            X_ = np.array(self.n_obs * [n])

            x = torch.normal(torch.mean(self.X), torch.std(self.X), (self.n_obs, self.X.shape[-1]))
            proba = self.model(x).detach().numpy()
            y_ = self.f([n]) + proba

            if X is None:
                X, y = X_, y_
            else:
                X = np.concatenate((X, X_))
                y = np.concatenate((y, y_))

        return X, y
