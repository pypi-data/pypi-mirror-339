# -*- coding: utf-8 -*-
from numbers import Number
from textwrap import dedent
from typing import Any
import cantera as ct
import logging

from ..common import T_NORMAL
from ..common import P_NORMAL
from ..common import CompositionType
from ..common import report_title


class CombustionAtmosphereCHON:
    """ Combustion atmosphere calculations for CHON system.

    Parameters
    ----------
    mechanism: str
        Kinetics mechanism/database to use in computations.
    """
    def __init__(self, mechanism: str) -> None:
        self._solution = ct.Solution(mechanism)

    def _state_standard(self, X):
        """ Set internal solution to standard state / composition. """
        self._solution.TPX = 273.15, ct.one_atm, X

    def _state_premix(self, phi, Y_c, Y_o, basis="mass"):
        """ Set internal solution to combustion premix composition. """
        self._solution.set_equivalence_ratio(phi, Y_c, Y_o, basis=basis)

    def _state_initial(self, species, oxidizer):
        """ Before combustion: reference state, stoichiometric. """
        self._solution.TP = 298.15, ct.one_atm
        self._solution.set_equivalence_ratio(1.0, species, oxidizer)
        return self._solution.enthalpy_mass, self._solution[species].Y[0]

    def _state_final(self):
        """ After combustion: complete combustion products. """
        self._solution.TPX = None, None, {
            "CO2": 1.0 * self._solution.elemental_mole_fraction("C"),
            "H2O": 0.5 * self._solution.elemental_mole_fraction("H"),
            "N2":  0.5 * self._solution.elemental_mole_fraction("N")
        }
        return self._solution.enthalpy_mass

    def _species_heating_value(self, species, oxidizer):
        """ Lower heating value of a single species [MJ/kg]. """
        h1, Y_fuel = self._state_initial(species, oxidizer)
        return (self._state_final() - h1) / Y_fuel

    def solution_heating_value(self,
            fuel: CompositionType,
            oxidizer: CompositionType
        ) -> float:
        """ Evaluate lower heating value of mixture.

        Parameters
        ----------
        fuel: CompositionType
            Composition of fuel in species mole fractions.
        oxidizer: CompositionType
            Composition of oxidizer in species mole fractions.

        Returns
        -------
        float
            Lower heating value of provided mixture [MJ/kg].
        """
        self._solution.TPX = None, None, fuel
        Y_fuel = self._solution.mass_fraction_dict()

        hv = sum(Y * self._species_heating_value(species, oxidizer)
                 for species, Y in Y_fuel.items())

        return -1.0e-06 * float(hv)

    def combustion_setup(self,
            power: float,
            phi: float,
            fuel: CompositionType,
            oxidizer: CompositionType,
            species: str = "O2"
        ) -> tuple[float, float, float]:
        """ Evaluates combustion setup for given quantities.

        Parameters
        ----------
        power: float
            Total supplied power [kW]
        phi: float
            Air-fuel equivalence ratio.
        fuel: CompositionType
            Composition of fuel in species mole fractions.
        oxidizer: CompositionType
            Composition of oxidizer in species mole fractions.
        species: str = "O2"
            Reference species for oxidizer mass balance.
        """
        lhv = self.solution_heating_value(fuel, oxidizer)
        mdot_c = 0.001 * power / lhv

        self._state_standard(fuel)
        Y_c = self._solution.mass_fraction_dict()

        self._state_standard(oxidizer)
        Y_o = self._solution.mass_fraction_dict()

        self._state_premix(phi, Y_c, Y_o)
        Y_m = self._solution.mass_fraction_dict()

        y_c = Y_c.get(species, 0.0)
        y_o = Y_o.get(species, 0.0)
        y_m = Y_m.get(species, 0.0)

        mdot_t = mdot_c * (y_c - y_o) / (y_m - y_o)
        mdot_o = mdot_t - mdot_c

        return (lhv, mdot_c, mdot_o)

    def normal_density(self, X: CompositionType) -> float:
        """ Compute solution normal density.

        Parameters
        ----------
        X: CompositionType
            Composition of solution in species mole fractions.

        Returns
        -------
        float
            Solution density under standard state [kg/Nm³].
        """
        self._state_standard(X)
        return self._solution.density_mass

    def normal_flow(self, mdot: float, X: CompositionType) -> float:
        """ Computes volume flow rate from mass flow and composition.

        Parameters
        ----------
        mdot: float
            Solution mass flow rate [kg/s].
        X: CompositionType
            Composition of solution in species mole fractions.

        Returns
        -------
        float
            Volume flow rate under standard state [Nm³/h].
        """

        return 3600 * mdot / self.normal_density(X)


class CombustionPowerSupply:
    """ Provides combustion calculations for given power supply.

    Parameters
    ----------
    power: float
        Total supplied power [kW]
    equivalence: float
        Air-fuel equivalence ratio.
    fuel: CompositionType
        Composition of fuel in species mole fractions.
    oxidizer: CompositionType
        Composition of oxidizer in species mole fractions.
    mechanism: str
        Kinetics mechanism/database to use in computations.
    species: str = "O2"
        Reference species for oxidizer mass balance.
    emissions: bool = True
        If true, compute emissions of water and carbon dioxide.
    """
    def __init__(self,
            power: float,
            equivalence: float,
            fuel: CompositionType,
            oxidizer: CompositionType,
            mechanism: str,
            species: str = "O2",
            emissions: bool = True
        ) -> None:
        self._ca = CombustionAtmosphereCHON(mechanism)

        (self._lhv, self._mdot_c, self._mdot_o) = self._ca.combustion_setup(
            power, equivalence, fuel, oxidizer, species=species)

        self._power = power
        self._Xc = fuel
        self._Xo = oxidizer

        if emissions:
            self._m_h2o, self._m_co2 = self._emissions(mechanism)

    def _emissions(self, mechanism, h2o="H2O", co2="CO2"):
        """ Evaluate complete combustion products for a gas. """
        mixer = CombustionAtmosphereMixer(mechanism)
        mixer.add_quantity(self._mdot_o, self._Xo)
        mixer.add_quantity(self._mdot_c, self._Xc)

        qty = mixer.solution
        qty.TP = 298.15, ct.one_atm
        qty.equilibrate("TP")
        # print(qty.report())

        Y = qty.mass_fraction_dict()
        m_1 = qty.mass * Y.get(h2o, 0.0)
        m_2 = qty.mass * Y.get(co2, 0.0)

        return m_1, m_2

    @property
    def power(self) -> float:
        """ Access to combustion power [kW]. """
        return self._power

    @property
    def fuel_mass(self) -> float:
        """ Access to fuel mass flow rate. """
        return self._mdot_c

    @property
    def oxidizer_mass(self) -> float:
        """ Access to oxidizer mass flow rate. """
        return self._mdot_o

    @property
    def fuel_volume(self) -> float:
        """ Access to fuel volume flow rate. """
        if not hasattr(self, "_qdot_c"):
            self._qdot_c = self._ca.normal_flow(self._mdot_c, self._Xc)
        return self._qdot_c

    @property
    def oxidizer_volume(self) -> float:
        """ Access to oxidizer volume flow rate. """
        if not hasattr(self, "_qdot_o"):
            self._qdot_o = self._ca.normal_flow(self._mdot_o, self._Xo)
        return self._qdot_o

    @property
    def fuel(self) -> CompositionType:
        """ Access to fuel mole fractions. """
        return self._Xc

    @property
    def oxidizer(self):
        """ Access to oxidizer mole fractions. """
        return self._Xo

    @property
    def fuel_normal_density(self):
        """ Fuel normal density. """
        if not hasattr(self, "_rho_c"):
            self._rho_c = self._ca.normal_density(self._Xc)
        return self._rho_c

    @property
    def oxidizer_normal_density(self):
        """ Oxidizer normal density. """
        if not hasattr(self, "_rho_o"):
            self._rho_o = self._ca.normal_density(self._Xo)
        return self._rho_o

    @property
    def production_water(self) -> float:
        """ Access to complete combustion H2O mass flow rate. """
        if not hasattr(self, "_m_h2o"):
            raise RuntimeError("Emissions not computed")
        return self._m_h2o

    @property
    def production_carbon_dioxide(self) -> float:
        """ Access to complete combustion CO2 mass flow rate. """
        if not hasattr(self, "_m_co2"):
            raise RuntimeError("Emissions not computed")
        return self._m_co2

    def __repr__(self) -> str:
        """ Standard representation of class instance. """
        args = f"P={self._power:.4e} kW LHV={self._lhv:.4e} MJ/kg"
        return f"<CombustionPowerSupply {args} />"

    def report(self) -> str:
        """ Generate combustion power and flow rates report."""
        if not hasattr(self, "_report"):
            mdot = self._mdot_c + self._mdot_o
            qdot = self.fuel_volume + self.oxidizer_volume

            report = dedent(f"""\
            - Required power              {self._power:7.1f} kW
            - Lower heating value         {self._lhv:7.1f} MJ/kg
            """)

            self._report = report_title("General", report)

            report = dedent(f"""\
            - Total mass flow rate        {3600*mdot:7.3f} kg/h
            - Fuel mass flow rate         {3600*self._mdot_c:7.3f} kg/h
            - Oxidizer mass flow rate     {3600*self._mdot_o:7.3f} kg/h
            """)

            self._report += report_title("Mass flow", report)

            report = dedent(f"""\
            - Total volume flow rate      {qdot:7.3f} Nm³/h
            - Fuel volume flow rate       {self.fuel_volume:7.3f} Nm³/h
            - Oxidizer volume flow rate   {self.oxidizer_volume:7.3f} Nm³/h
            """)

            self._report += report_title("Volume flow", report)

            if hasattr(self, "_m_h2o"):
                mdot =  self._m_h2o + self._m_co2

                report = dedent(f"""\
                - Total emissions             {3600*mdot:7.3f} kg/h
                - Water production            {3600*self._m_h2o:7.3f} kg/h
                - Carbon dioxide production   {3600*self._m_co2:7.3f} kg/h
                """)

                self._report += report_title("Emissions", report)

        return self._report


class CombustionAtmosphereMixer:
    """ Provides addition of thermochemical quantities.

    Parameters
    ----------
    mechanism: str
        Kinetics mechanism/database to use in computations.
    """
    def __init__(self, mechanism: str) -> None:
        self._mechanism = mechanism
        self._quantity = None

    def _new_quantity(self, mass, T, P, X):
        """ Create a new quantity with provided state. """
        solution = ct.Solution(self._mechanism)
        solution.TPX = T, P, X
        return ct.Quantity(solution, mass=mass)

    def add_quantity(self,
            mass: float,
            X: CompositionType,
            T: float = 273.15,
            P: float = ct.one_atm
        ) -> None:
        """ Add quantity at given state to global mixture.

        Parameters
        ----------
        mass: float
            Amount of matter in kilograms.
        X: CompositionType
            Composition of quantity in mole fractions.
        T: float = 273.15
            Solution temperature in kelvin.
        P: float = ct.one_atm
            Solution pressure in pascal.
        """
        quantity = self._new_quantity(mass, T, P, X)

        if self._quantity is None:
            self._quantity = quantity
        else:
            self._quantity += quantity

    @property
    def solution(self) -> ct.Quantity:
        """ Provides access to computed solution, if any. """
        if self._quantity is None:
            raise RuntimeError("First add some quantities")
        return self._quantity


#######################################################################
# LEGACY
#######################################################################


class Solution:
    """ Wrapper around Cantera's solution object. """
    def __init__(self, mech: str, /, **kwargs) -> None:
        self._mech = mech
        self._sol = self._handle_init(mech, **kwargs)

    @staticmethod
    def _handle_init(mech, **kwargs):
        """ Create a standard solution from mechanism. """
        sol = ct.Solution(mech)
        T = kwargs.get("T", sol.T)
        P = kwargs.get("P", sol.P)
        X = kwargs.get("X", sol.mole_fraction_dict())
        sol.TPX = T, P, X
        return sol

    def density(self, /, **kwargs) -> float:
        """ Density of provided mixture under normal conditions [kg/m³]. """
        T = kwargs.get("T", self._sol.T)
        P = kwargs.get("P", self._sol.P)
        X = kwargs.get("X", None)
        X = X if X else self._sol.mole_fraction_dict()
        sol = self._handle_init(self._mech, X=X, T=T, P=P)
        return sol.density_mass

    def density_normal(self, /, X: CompositionType = None) -> float:
        """ Density of provided mixture under normal conditions [kg/m³]. """
        return self.density(X=X, T=T_NORMAL, P=P_NORMAL)

    @property
    def solution(self) -> ct.Solution:
        """ Provides access to the wrapped solution object. """
        return self._sol


class FuelMixture:
    """ Create a fuel mixture for combustion calculations.

    Parameters
    ----------
    mech: str
        Kinetics mechanism used for evaluation of fuel properties.
    X: Composition
        Fuel composition [mole fractions].
    """
    def __init__(self, mech: str, X: CompositionType, /, **kwargs) -> None:
        self._sol = self._handle_init(mech, X, **kwargs)
        self._lhv = self._lower_heating_value()

    @staticmethod
    def _handle_init(mech, X, **kwargs):
        """ Create a standard mixture from mechanism. """
        T = kwargs.get("T", T_NORMAL)
        P = kwargs.get("P", P_NORMAL)
        sol = Solution(mech, X=X, T=T, P=P)
        return sol

    @staticmethod
    def species_lower_heating_value(
            gas: ct.Solution,
            fuel: CompositionType,
            T: Number,
        ) -> float:
        """ Returns the lower heating value of species [MJ/kg]. """
        gas.TP = T, ct.one_atm
        gas.set_equivalence_ratio(1.0, fuel, "O2: 1.0")
        h1 = gas.enthalpy_mass
        Y_fuel = gas[fuel].Y[0]

        gas.TPX = None, None, chon_complete_combustion(gas)
        h2 = gas.enthalpy_mass

        return -1.0e-06 * (h2 - h1) / Y_fuel

    def _lower_heating_value(self):
        """ Mixture mass weighted average heating value [MJ/kg]. """
        sol = self._sol.solution
        Hv = sum(Y * self.species_lower_heating_value(sol, name, sol.T)
                 for name, Y in sol.mass_fraction_dict().items())
        return float(Hv)

    def power_supply(self, mdot: Number) -> float:
        """ Total fuel computed power supply [kW].

        Parameters
        ----------
        mdot: Number
            Fuel mass flow rate [kg/h].
        """
        return 0.001 * (mdot / 3600.0) * (self._lhv * 1.0e+06)

    @property
    def lower_heating_value(self):
        """ Mixture mass weighted average heating value [MJ/kg]. """
        return self._lhv


def chon_complete_combustion(gas: ct.Solution) -> dict[str, float]:
    """ Evaluate complete combustion products for a gas. """
    return {
        "CO2": 1.0 * gas.elemental_mole_fraction("C"),
        "H2O": 0.5 * gas.elemental_mole_fraction("H"),
        "N2":  0.5 * gas.elemental_mole_fraction("N")
    }


class FluidStream:
    """ Represents a fluid mass flow stream of a Cantera solution. """
    def __init__(self, mech, mass, T=298.15, P=ct.one_atm, **kwargs):
        self._solution = self._handle_init(mech, T, P, **kwargs)
        self._quantity = ct.Quantity(self._solution, mass=mass)

    @staticmethod
    def _handle_init(mech, T, P, **kwargs):
        """ Object solution creation with option and error handling. """
        solution = ct.Solution(mech)

        if "X" in kwargs and "Y" in kwargs:
            raise ValueError("Only one of `X` or `Y` can be specified")

        if "X" not in kwargs and "Y" not in kwargs:
            raise ValueError("At least one of `X` or `Y` must be specified")

        if "X" in kwargs:
            solution.TPX = T, P, kwargs.get("X")

        if "Y" in kwargs:
            solution.TPY = T, P, kwargs.get("Y")

        return solution

    @property
    def quantity(self):
        """ Provides access to underlining quantity of matter. """
        return self._quantity

    @classmethod
    def copy(cls, other):
        """ Copy `other` into a new `FluidStream`. """
        mech = other.quantity.source
        mass = other.quantity.mass
        T, P, X = other.quantity.TPX
        return cls(mech, mass, T=T, P=P, X=X)


def mix_streams(streams: list[FluidStream]):
    """ Perform stream algebra to produce the resulting fluid. """
    quantity = FluidStream.copy(streams[0]).quantity

    for stream in streams[1:]:
        quantity += stream.quantity

    return quantity


def complete_combustion(streams, threshold=1.0e-06):
    """ Compute equivalent stream of complete combustion. """
    mixture = mix_streams(streams)
    mixture.equilibrate("TP")

    X = mixture.mole_fraction_dict()
    X = {k: v for k, v in X.items() if v > threshold}

    mixture = mix_streams(streams)
    mixture.equilibrate("HP")

    mixture.TPX = None, None, X
    return mixture
