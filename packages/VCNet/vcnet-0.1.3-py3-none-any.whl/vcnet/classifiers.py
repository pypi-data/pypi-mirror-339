"""Classifier Model for VCNet."""

import torch
import torch.nn as nn
import torch.optim as optim
import lightning as L
import pandas as pd

# pylint: disable=W0611
# pylint: disable=W0123
# pylint: disable=C0103

from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

class SKLearnClassifier:
    """Wrapper for using a sklearn classifiers in the VCNet pipeline.

    Example of minimal configuration:
    ---------------------------------
    ```{python}
    {
        "dataset": {
            "target":"income",
        },
        "classifier_params" : {
            "skname":  "RandomForestClassifier",
            "kwargs": {
                "n_estimators" : 50,
            }
        }
    }
    classifier = SKLearnClassifier(hp)
    classifier.fit(dataset.df_train)
    ```

    Attributes:
        hp (Dict): configuration of the classifier (hyperparameters) and the dataset


    Remark
    --------
    This class allows to use an `XGBoostClassifier`


    Remark
    -------
    The _kwargs_ of the classifier have to be checked from the sklearn API or 
    the (XGBoost API)[https://xgboost.readthedocs.io/en/stable/python/sklearn_estimator.html]
    """

    def __init__(self, hp):
        if "classifier_params" in hp and "skname" in hp["classifier_params"]:
            if "kwargs" in hp["classifier_params"]:
                self.clf = eval(hp["classifier_params"]["skname"])(
                    **hp["classifier_params"]["kwargs"]
                )
            else:
                self.clf = eval(hp["classifier_params"]["skname"])()
            self.hp = hp
        else:
            raise RuntimeError(
                "invalid parameters: the ['classifier_params']['skname'] parameter is missing."
            )

    def __call__(self, x: torch.tensor) -> torch.tensor:
        """Application of the classifier on a tensor

        Args:
            x (torch.tensor):

        Returns:
            np.array: vector containing the probability of the class 1
        """

        p = self.clf.predict_proba(x.detach().cpu())
        return torch.tensor(
            p[:, 1], dtype=torch.float32, requires_grad=False, device=device
        ).unsqueeze(1)

    def fit(self, X: pd.DataFrame):
        """function to fit the model

        Args:
            X (pd.DataFrame): dataset to train the model on
        """
        self.clf.fit(
            X.drop(self.hp["dataset"]["target"], axis=1).to_numpy(),
            X[self.hp["dataset"]["target"]],
        )


class Classifier(L.LightningModule):
    """Simple fully convolutional classifier that can be used

    Args:
        hp (Dict): configuration of the classifier (hyperparameters) and the dataset
    """

    def __init__(self, hp):
        super().__init__()

        self._hp = hp

        self.model = nn.Sequential(
            nn.Linear(
                hp["dataset"]["feature_size"], hp["classifier_params"]["l1_size"]
            ),
            nn.ReLU(),
            # nn.BatchNorm1d(hp['classifier_params']["l1_size"]),
            # nn.Dropout(p=0.1),
            nn.Linear(
                hp["classifier_params"]["l1_size"], hp["classifier_params"]["l2_size"]
            ),
            nn.ReLU(),
            # nn.BatchNorm1d(hp['classifier_params']["l2_size"]),
            # nn.Dropout(p=0.1),
            nn.Linear(
                hp["classifier_params"]["l2_size"], hp["classifier_params"]["l3_size"]
            ),
            nn.ReLU(),
            nn.Linear(
                hp["classifier_params"]["l3_size"], hp["dataset"]["class_size"] - 1
            ),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.tensor):  # pylint: disable=W0221
        return self.model(x)

    def training_step(self, batch, batch_idx):  # pylint: disable=W0221,W0613
        x, y = batch
        output_class = self.forward(x).squeeze()
        loss = nn.BCELoss(reduction="sum")(output_class, y)
        return loss

    def configure_optimizers(self):
        optimizer = optim.Adam(
            self.parameters(), lr=self._hp["classifier_params"]["lr"]
        )
        return optimizer
