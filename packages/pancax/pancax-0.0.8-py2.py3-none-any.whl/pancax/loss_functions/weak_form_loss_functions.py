from .base_loss_function import PhysicsLossFunction
from jax import vmap
from typing import Optional
import jax.numpy as jnp


class EnergyLoss(PhysicsLossFunction):
    r"""
    Energy loss function akin to the deep energy method.

    Calculates the following quantity

    .. math::
      \mathcal{L} = w\Pi\left[u\right] = \
        w\int_\Omega\psi\left(\mathbf{F}\right)

    :param weight: weight for this loss function
    """

    weight: float

    def __init__(self, weight: Optional[float] = 1.0):
        self.weight = weight

    def __call__(self, params, problem):
        energies = vmap(self.load_step, in_axes=(None, None, 0))(
            params, problem, problem.times
        )
        energy = jnp.sum(energies)
        loss = energy
        return self.weight * loss, dict(energy=energy)

    def load_step(self, params, problem, t):
        field, physics, state = params
        us = physics.vmap_field_values(field, problem.coords, t)
        pi = physics.potential_energy(physics, problem.domain, t, us)
        return pi


class ResidualMSELoss(PhysicsLossFunction):
    weight: float

    def __init__(self, weight: Optional[float] = 1.0):
        self.weight = weight

    def __call__(self, params, domain):
        mses = vmap(self.load_step, in_axes=(None, None, 0))(
            params, domain, domain.times
        )
        mse = mses.mean()
        return self.weight * mse, dict(residual=mse)

    def load_step(self, params, domain, t):
        field, physics, state = params
        us = physics.vmap_field_values(field, domain.coords, t)
        rs = jnp.linalg.norm(physics.vmap_element_residual(
            field, domain, t, us
        ))
        return rs.mean()


class EnergyAndResidualLoss(PhysicsLossFunction):
    r"""
    Energy and residual loss function used in Hamel et. al

    Calculates the following quantity

    .. math::
      \mathcal{L} = w_1\Pi\left[u\right] + w_2\delta\Pi\left[u\right]_{free}

    :param energy_weight: Weight for the energy w_1
    :param residual_weight: Weight for the residual w_2
    """

    energy_weight: float
    residual_weight: float

    def __init__(
        self,
        energy_weight: Optional[float] = 1.0,
        residual_weight: Optional[float] = 1.0,
    ):
        self.energy_weight = energy_weight
        self.residual_weight = residual_weight

    def __call__(self, params, domain):
        pis, Rs = vmap(self.load_step, in_axes=(None, None, 0))(
            params, domain, domain.times
        )
        pi, R = jnp.sum(pis), jnp.sum(Rs)
        loss = self.energy_weight * pi + self.residual_weight * R
        return loss, dict(energy=pi, residual=R)

    def load_step(self, params, domain, t):
        # field_network, props = params
        # us = domain.field_values(field_network, t)
        # props = props()
        # pi, R = potential_energy_and_residual(domain, us, props)
        # return pi, R
        field, physics, state = params
        us = physics.vmap_field_values(field, domain.coords, t)
        return physics.potential_energy_and_residual(params, domain, t, us)


class EnergyResidualAndReactionLoss(PhysicsLossFunction):
    energy_weight: float
    residual_weight: float
    reaction_weight: float

    def __init__(
        self,
        energy_weight: Optional[float] = 1.0,
        residual_weight: Optional[float] = 1.0,
        reaction_weight: Optional[float] = 1.0,
    ):
        self.energy_weight = energy_weight
        self.residual_weight = residual_weight
        self.reaction_weight = reaction_weight

    def __call__(self, params, domain):
        pis, Rs, reactions = vmap(self.load_step, in_axes=(None, None, 0))(
            params, domain, domain.times
        )
        pi, R = jnp.sum(pis), jnp.sum(Rs) / len(domain.times)
        reaction_loss = \
            jnp.square(reactions - domain.global_data.outputs).mean()
        loss = (
            self.energy_weight * pi
            + self.residual_weight * R
            + self.reaction_weight * reaction_loss
        )
        return loss, dict(
            energy=pi, residual=R,
            global_data_loss=reaction_loss, reactions=reactions
        )

    def load_step(self, params, domain, t):
        # field_network, props = params
        field, physics, state = params
        # us = domain.field_values(field_network, t)
        us = physics.vmap_field_values(field, domain.coords, t)
        return physics.potential_energy_residual_and_reaction_force(
            params, domain, t, us, domain.global_data
        )


class PathDependentEnergyLoss(PhysicsLossFunction):
    weight: float

    def __init__(self, weight: Optional[float] = 1.0) -> None:
        self.weight = weight

    def __call__(self, params, domain):
        # TODO for a naive implementation
        pass

    def load_step(self, field, physics, state_old, t, dt):
        us = physics.vmap_field_values(field, domain.coords, t)
        pi, state_new = physics.potential_energy(
            physics,
        )
        print(us)
        assert False, 'Implement this'
