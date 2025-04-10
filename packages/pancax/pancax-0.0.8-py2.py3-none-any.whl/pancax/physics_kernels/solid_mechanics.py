from abc import abstractmethod
from .base import BaseEnergyFormPhysics
from pancax.math.tensor_math import tensor_2D_to_3D
import equinox as eqx
import jax.numpy as jnp


# different formulations e.g. plane strain/stress, axisymmetric etc.
class BaseMechanicsFormulation(eqx.Module):
    n_dimensions: int = eqx.field(static=True)  # does this need to be static?

    @abstractmethod
    def modify_field_gradient(self, grad_u):
        pass


# note for this formulation we're getting NaNs if the
# reference configuration is used during calculation
# of the loss function
class IncompressiblePlaneStress(BaseMechanicsFormulation):
    n_dimensions = 2

    def __init__(self) -> None:
        print(
            "WARNING: Do not include a time of 0.0 with this formulation. "
            "You will get NaNs."
        )

    def deformation_gradient(self, grad_u):
        F = tensor_2D_to_3D(grad_u) + jnp.eye(3)
        F = F.at[2, 2].set(1.0 / jnp.linalg.det(grad_u + jnp.eye(2)))
        return F

    def modify_field_gradient(self, grad_u):
        F = self.deformation_gradient(grad_u)
        return F - jnp.eye(3)


class PlaneStrain(BaseMechanicsFormulation):
    n_dimensions: int = 2

    def extract_stress(self, P):
        return P[0:2, 0:2]

    def modify_field_gradient(self, grad_u):
        return tensor_2D_to_3D(grad_u)


class ThreeDimensional(BaseMechanicsFormulation):
    n_dimensions: int = 3

    def modify_field_gradient(self, grad_u):
        return grad_u


class SolidMechanics(BaseEnergyFormPhysics):
    field_value_names: tuple[str, ...]
    constitutive_model: any
    formulation: BaseMechanicsFormulation

    def __init__(self, constitutive_model, formulation) -> None:
        # TODO clean this up below
        field_value_names = ("displ_x", "displ_y")
        super().__init__(field_value_names)
        if formulation.n_dimensions > 2:
            field_value_names = field_value_names + ("displ_z",)

        self.field_value_names = field_value_names
        self.constitutive_model = constitutive_model
        self.formulation = formulation

    def energy(self, params, x, t, u, grad_u, *args):
        grad_u = self.formulation.modify_field_gradient(grad_u)
        return self.constitutive_model.energy(grad_u)
