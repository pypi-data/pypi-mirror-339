"""Module for the VCNet models"""

from abc import ABC, abstractmethod
from typing import Dict

import torch
from torch import nn, optim
from torch.nn import functional as F
import lightning as L

# pylint: disable=C0103


device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

class VCNetBase(L.LightningModule, ABC):
    """
    Class for the general VCNet architecture with handling immutable features.
    This class is abstract.
    It specifies a VCNet model with a classifier and a conditional variational auto-encoder (cVAE)
    and a training procedure.
    The training procedure of a VCNet architecture consists in training the cVAE in a classical
    way.
    The VCNet trick lies in generating counterfactuals by switching the predicted class of an
    example to generate a modified example using the cVAE.

    The VCNet architecture handles natively the immutable features.

    Note that this VCNet architecture handles only numerical features.
    The user of this class has to manage the encoding of categorical features out of this class.

    The current class implements the cVAE and abstract function.
    """

    def __init__(self, model_config: Dict):
        super().__init__()
        self.model_config = model_config

        self.feature_size = int(model_config["dataset"]["feature_size"])
        self.feature_size_immutable = int(
            model_config["dataset"]["feature_size_immutable"]
        )
        self.feature_size_mutable = int(model_config["dataset"]["feature_size_mutable"])
        self.immutables_pos = model_config["dataset"]["immutables_pos"]
        self.class_size = int(model_config["dataset"]["class_size"])
        self.latent_size = int(model_config["vcnet_params"]["latent_size"])
        self.mid_reduce_size = int(model_config["vcnet_params"]["mid_reduce_size"])
        self.lambda_KLD = float(model_config["vcnet_params"]["lambda_KLD"])
        self.lambda_BCE = float(model_config["vcnet_params"]["lambda_BCE"])

        # C-VAE encoding
        self.e1 = nn.Linear(self.feature_size, self.mid_reduce_size)
        self.e2 = nn.Linear(self.mid_reduce_size, self.latent_size)
        self.e3 = nn.Linear(self.mid_reduce_size, self.latent_size)

        # C-VAE Decoding
        self.fd1 = nn.Linear(
            self.latent_size + self.class_size - 1 + self.feature_size_immutable,
            self.mid_reduce_size,
        )
        self.fd2 = nn.Linear(self.mid_reduce_size, self.feature_size)
        self.fd3 = nn.Linear(self.feature_size, self.feature_size_mutable)

        # Activation functions
        self.elu = nn.ELU()
        self.sigmoid = nn.Sigmoid()

    def encode(
        self,
        z: torch.tensor,
        x_mut: torch.tensor, # pylint: disable=W0613
        x_immut: torch.tensor,  # pylint: disable=W0613
    ) -> torch.tensor:
        """C-VAE encoding

        Args:
            z (torch.tensor): pre-encoded input representation. None or tensor of size
                defined by `latent_size_share`
            x_mut (torch.tensor): mutable part of the input tensor
            x_immut (torch.tensor): mutable part of the input tensor

        Returns:
            tuple(torch.tensor, torch.tensor): representation of the gaussian distribution
                in the latent space (mu, sigma). Tensors of dimension `latent_size`.
        """
        h1 = self.elu(self.e1(z))
        z_mu = self.e2(h1)
        z_var = self.e3(h1)
        return z_mu, z_var

    def reparameterize(self, mu: torch.tensor, sigma: torch.tensor) -> torch.tensor:
        """C-VAE Reparametrization trick

        Args:
            mu (torch.tensor): size latent_size
            sigma (torch.tensor): size latent_size

        Returns:
            torch.tensor: size latent_size
        """
        # torch.manual_seed(0)
        std = torch.exp(0.5 * sigma)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z_prime: torch.tensor, c: torch.tensor) -> torch.tensor:
        """C-VAE decoding, computes  P(x|z, c)

        Args:
            z_prime (torch.tensor): _description_
            c (torch.tensor): conditioning of the VAE. For VCNet, the decoding is conditioned
                by the class and the immutable features [class, x_immutable]. Then, its
                dimension is class_size-1 + len(x_immutable)

        Returns:
            torch.tensor: _description_
        """
        inputs = torch.cat([z_prime, c], 1)  # (bs, latent_size+class_size)
        h1 = self.elu(self.fd1(inputs))
        h2 = self.elu(self.fd2(h1))
        h3 = self.fd3(h2)
        return h3

    def pre_encode(self, x_mut: torch.tensor, x_immut: torch.tensor) -> torch.tensor:
        """
        Function that prepares examples (`x`) with a shared pre-coding layers.

        The default behavior is to transmit `x` as it.
        """
        return torch.hstack((x_mut, x_immut))

    @abstractmethod
    def classif(
        self,
        z: torch.tensor,
        x: torch.tensor,
        x_mut: torch.tensor,
        x_immut: torch.tensor,
    ) -> torch.tensor:
        """Forward function of the classification layers.
        It predicts the class of an example `z` prepared by the `encode_classif` function.

        Args:
            z (torch.tensor): examples represented in their latent space for classification.

        Returns:
            torch.tensor: example classification. Dimension self.class_size.
        """

    def forward(self, x: torch.tensor):  # pylint: disable=W0221
        """Forward function used during the training phase of a VCNet model.
        It mainly goes through the three parts of the models: the pre-coding, the C-VAE and the
        classification.
        Finally, it returns the reconstructed example, the output class and VAE distribution
        parameters.

        Args:
            x (torch.tensor): input examples
        """
        x_immutable = x[:, self.immutables_pos]
        x_mutable = x[:, list(set(range(x.shape[1])) - set(self.immutables_pos))]

        z = self.pre_encode(x_mutable, x_immutable)
        # Output of classification layers
        output_class = self.classif(z, x, x_mutable, x_immutable)

        # C-VAE encoding
        mu, logvar = self.encode(z, x_mutable, x_immutable)
        z_prime = self.reparameterize(mu, logvar)

        # Decoded output
        c = self.decode(z_prime, torch.hstack((output_class, x_immutable)))

        # Return Decoded output + output class
        return c, mu, logvar, output_class

    def forward_pred(self, x: torch.tensor) -> torch.tensor:
        """Forward function for prediction in test phase (prediction task).
        It prepares the examples and then classify

        Args:
            x (torch.tensor): _description_
        """
        x_immutable = x[:, self.immutables_pos]
        x_mutable = x[:, list(set(range(x.shape[1])) - set(self.immutables_pos))]

        z = self.pre_encode(x_mutable, x_immutable)
        # Output of classification layers
        output_class = self.classif(z, x, x_mutable, x_immutable)
        # Return classification layers output
        return output_class.to(device)

    def _forward_cvae(self, x: torch.tensor, c_pred: torch.tensor) -> torch.tensor:
        """Forward function through the c-VAE. It encodes and decodes examples `x`
         with imposed class conditions, `c_pred`.

        Args:
            x (torch.tensor): an example to modify
            c_pred (torch.tensor): the class in which the example has to be move into

        Returns:
            torch.tensor: modified examples through the C-VAE with imposed class.
        """
        x_immutable = x[:, self.immutables_pos]
        index_x_mutable = list(set(range(x.shape[1])) - set(self.immutables_pos))
        x_mutable = x[:, index_x_mutable]

        z = self.pre_encode(x_mutable, x_immutable)
        mu, logvar = self.encode(z, x_mutable, x_immutable)
        z_prime = self.reparameterize(mu, logvar)
        c_mutable = self.decode(z_prime, torch.hstack((c_pred, x_immutable)))

        c = torch.clone(x)
        c[:, index_x_mutable] = c_mutable

        return c

    def __change_class(self, pc: torch.tensor) -> torch.tensor:
        """Generate the probablility class of a counterfactual on an example that belongs to
        class `pc`.
        This implementation is made for binary classification.

        Args:
            pc (torch.tensor): probability to belong to class 1 (provided by a classifier).

        Returns:
            torch.tensor: probability vector of the "opposite" class of `pc`. The return has
            the same dimension as the input.
        """
        return (pc < 0.5).int()

    def counterfactuals(self, x: torch.tensor) -> torch.tensor:
        """Generation of counterfactuals for the example `x`.

        Warning
        ------------
        This function has been tested only for binary classification.
        The use with a multiclass problem is still to evaluate.
        """
        self.eval()
        with torch.no_grad():
            # Predicted probas for examples
            predicted_examples_proba = self.forward_pred(x).squeeze(1)

            # Pass to the model to have counterfactuals
            cf_pc = self.__change_class(predicted_examples_proba)
            counterfactuals = self._forward_cvae(x, cf_pc.unsqueeze(1).detach().cpu())

            # Predicted probas for counterfactuals
            predicted_counterfactuals_proba = self.forward_pred(
                counterfactuals
            ).squeeze(1)

            # Predicted classes for counterfactuals
            predicted_counterfactuals_classes = torch.round(
                predicted_counterfactuals_proba
            ).long()

            return counterfactuals, predicted_counterfactuals_classes

    def loss_functions(
        self, recon_x, x, mu, sigma, output_class=None, y_true=None
    ):  # pylint: disable=W0613
        """Evaluate the loss of the reconstruction"""
        x_mutable = x[:, list(set(range(x.shape[1])) - set(self.immutables_pos))]

        # Loss for reconstruction
        BCE = F.mse_loss(recon_x, x_mutable, reduction="sum")
        # KL-divergence loss
        KLD = -0.5 * torch.sum(1 + sigma - mu.pow(2) - sigma.exp())

        # Return individual losses + weighted sum of losses
        return [BCE, KLD], self.lambda_BCE * BCE + self.lambda_KLD * KLD

    def training_step( # pylint: disable=W0221
        self, batch: torch.tensor, batch_idx # pylint: disable=W0613
    ) -> float:
        """Training step for lightning

        Args:
            batch (torch.tensor): batch
            batch_idx (torch.tensor): list of example indices

        Returns:
            float: loss measure for the batch
        """
        x, y = batch
        recon_batch, mu, logvar, output_class = self.forward(x)

        # Compute loss function
        losses, loss = self.loss_functions(
            recon_batch, x, mu, logvar, output_class, y.unsqueeze(1)
        )
        self.log("train_loss", loss)
        self.log("train_BCE_loss", losses[0])
        self.log("train_KLD_loss", losses[1])
        return loss

    def configure_optimizers(self):
        """Setup of the optimizer"""
        optimizer = optim.Adam(
            self.parameters(), lr=self.model_config["vcnet_params"]["lr"]
        )
        return optimizer


class VCNet(VCNetBase):
    """
    Class for VCNet immutable version model architecture.
    VCNet is a joint learning architecture: during the training phase, both the classifier and
    the counterfactual generators are fitted.
    """

    def __init__(self, model_config: Dict):
        super().__init__(model_config)

        try:
            self.lambda_CE = float(model_config["vcnet_params"]["lambda_CE"])
            self.latent_size_share = int(
                model_config["vcnet_params"]["latent_size_share"]
            )
        except KeyError:
            print("missing arguments")

        # Pre-encoding
        self.se = nn.Linear(self.feature_size, self.latent_size_share)

        # C-VAE encoding (redefinition of some layers to match the size)
        self.e1 = nn.Linear(self.latent_size_share, self.mid_reduce_size)

        # C-VAE Decoding (redefinition of some layers)
        self.fd2 = nn.Linear(self.mid_reduce_size, self.latent_size_share)
        self.fd3 = nn.Linear(self.latent_size_share, self.feature_size_mutable)

        # Classification model
        self.fcl1 = nn.Linear(self.latent_size_share, self.latent_size_share)
        self.fcl2 = nn.Linear(self.latent_size_share, self.class_size - 1)

    def pre_encode(self, x_mut: torch.tensor, x_immut: torch.tensor) -> torch.tensor:
        z = self.elu(self.se(torch.hstack((x_mut, x_immut))))
        return z

    # Classification layers (after shared encoding)
    def classif(
        self,
        z: torch.tensor,
        x: torch.tensor,
        x_mut: torch.tensor,
        x_immut: torch.tensor,
    ) -> torch.tensor:
        c1 = self.elu(self.fcl1(z))
        c2 = self.fcl2(c1)
        return self.sigmoid(c2)

    def loss_functions(self, recon_x, x, mu, sigma, output_class=None, y_true=None):
        """Evaluation of the VCNet losses"""
        x_mutable = x[:, list(set(range(x.shape[1])) - set(self.immutables_pos))]

        # Loss for reconstruction
        BCE = F.mse_loss(recon_x, x_mutable, reduction="sum")

        # KL-divergence loss
        KLD = -0.5 * torch.sum(1 + sigma - mu.pow(2) - sigma.exp())

        # Classification loss
        CE = nn.BCELoss(reduction="sum")(output_class, y_true)

        # Return individual losses + weighted sum of losses
        return [
            BCE,
            KLD,
            CE,
        ], self.lambda_BCE * BCE + self.lambda_KLD * KLD + self.lambda_CE * CE

    def training_step(self, batch, batch_idx):
        x, y = batch
        recon_batch, mu, logvar, output_class = self.forward(x)

        # Compute loss function
        losses, loss = self.loss_functions(
            recon_batch, x, mu, logvar, output_class, y.unsqueeze(1)
        )
        self.log("train_loss", loss)
        self.log("train_BCE_loss", losses[0])
        self.log("train_KLD_loss", losses[1])
        self.log("train_CE_loss", losses[2])
        return loss


class PHVCNet(VCNetBase):
    """
    Class for Post-hoc VCNet immutable version model architecture.
    Post-hoc VCNet uses a torch classifier trained on a classification task and trains
    the counterfactual generators.

    A classifier provided to this class is assumed to take examples to be classified.
    """

    def __init__(self, model_config: Dict, classifier: torch.nn.Module):
        super().__init__(model_config)
        self.classifier = classifier
        # freeze the parameters of the classifier
        if isinstance(classifier, nn.Module):
            for p in self.classifier.parameters():
                p.requires_grad = False

    def classif(
        self,
        z: torch.tensor,
        x: torch.tensor,
        x_mut: torch.tensor,
        x_immut: torch.tensor,
    ) -> torch.tensor:
        return self.classifier(x)

    def training_step(self, batch, batch_idx):
        x, _ = batch
        recon_batch, mu, logvar, _ = self.forward(x)

        # Compute loss function
        losses, loss = self.loss_functions(recon_batch, x, mu, logvar)
        self.log("train_loss", loss)
        self.log("train_BCE_loss", losses[0])
        self.log("train_KLD_loss", losses[1])
        return loss
