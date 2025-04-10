
"""Constants

Provides access to universal constants and known values.
"""

# Import statements
from dataclasses import dataclass, field
from enum import Enum

from .collections import ImmutableDict, crystallize, crystalline


@dataclass(frozen=True)
class Elements:
    """Provides access to data from the Periodic Table of the Elements.

    You should not attempt to directly mutate members of this class.
    Instead, should you need to alter the provided default values for
    any reason, you should work with a copy of the data, e.g., via:

    ```
    # Creates a mutable copy of the `Elements.H` object.
    h = Elements.H
    ```

    Attempting to mutate the `Elements` class directly is an error
    in crude 1.0 and will raise `IllegalMutationError`. (For more
    information about the errors and exceptions that ship with the
    crude framework, try `help(crude.exceptions)` or
    `help(crude.errors)`.
    """
    
    H: dict = field(default_factory=lambda: {
          "name": "hydrogen",
         "symbol": "H",
         "number": 1,
         "weight": 1.00794,
         "boilingPoint": -252.87,
         "meltingPoint": -259.14,
         "density": 0.0899,
         "eneg": 2.2}
         )
    
    He: dict = field(default_factory=lambda: {
          "name": "helium",
          "symbol": "He",
          "number": 2,
          "weight": 4.002602,
          "boilingPoint": -268.93,
          "meltingPoint": -272.2,
          "density": 0.1785,
          "eneg": None}
         )
    
    Li: dict = field(default_factory=lambda: {
          "name": "lithium",
          "symbol": "Li",
          "number": 3,
          "weight": 6.941,
          "boilingPoint": 1342,
          "meltingPoint": 180.54,
          "density": 0.534,
          "eneg": 0.98}
         )
    
    Be: dict = field(default_factory=lambda: {
          "name": "beryllium",
          "symbol": "Be",
          "number": 4,
          "weight": 9.012182,
          "boilingPoint": 2970,
          "meltingPoint": 1287,
          "density": 1.85,
          "eneg": 1.57}
         )
    
    B: dict = field(default_factory=lambda: {
         "name": "boron",
         "symbol": "B",
         "number": 5,
         "weight": 10.811,
         "boilingPoint": 4000,
         "meltingPoint": 2075,
         "density": 2.34,
         "eneg": 2.04}
         )
    
    C: dict = field(default_factory=lambda: {
         "name": "carbon",
         "symbol": "C",
         "number": 6,
         "weight": 12.0107,
         "boilingPoint": 4300,
         "meltingPoint": 3550,
         "density": 2.26,
         "eneg": 2.55}
         )
    
    N: dict = field(default_factory=lambda: {
         "name": "nitrogen",
         "symbol": "N",
         "number": 7,
         "weight": 14.0067,
         "boilingPoint": -195.79,
         "meltingPoint": -210.0,
         "density": 0.001251,
         "eneg": 3.04}
         )
    
    O: dict = field(default_factory=lambda: {
         "name": "oxygen",
         "symbol": "O",
         "number": 8,
         "weight": 15.9994,
         "boilingPoint": -182.95,
         "meltingPoint": -218.79,
         "density": 0.001429,
         "eneg": 3.44}
         )
    
    F: dict = field(default_factory=lambda: {
         "name": "fluorine",
         "symbol": "F",
         "number": 9,
         "weight": 18.9984032,
         "boilingPoint": -188.12,
         "meltingPoint": -219.62,
         "density": 0.001696,
         "eneg": 3.98}
         )
    
    Ne: dict = field(default_factory=lambda: {
          "name": "neon",
          "symbol": "Ne",
          "number": 10,
          "weight": 20.1797,
          "boilingPoint": -246.08,
          "meltingPoint": -248.59,
          "density": 0.0009,
          "eneg": None}
         )
    
    Na: dict = field(default_factory=lambda: {
          "name": "sodium",
          "symbol": "Na",
          "number": 11,
          "weight": 22.98976928,
          "boilingPoint": 882.9,
          "meltingPoint": 97.72,
          "density": 0.971,
          "eneg": 0.93}
         )
    
    Mg: dict = field(default_factory=lambda: {
          "name": "magnesium",
          "symbol": "Mg",
          "number": 12,
          "weight": 24.305,
          "boilingPoint": 1090,
          "meltingPoint": 650,
          "density": 1.738,
          "eneg": 1.31}
         )
    
    Al: dict = field(default_factory=lambda: {
          "name": "aluminum",
          "symbol": "Al",
          "number": 13,
          "weight": 26.9815386,
          "boilingPoint": 2519,
          "meltingPoint": 660.32,
          "density": 2.698,
          "eneg": 1.61}
         )
    
    Si: dict = field(default_factory=lambda: {
          "name": "silicon",
          "symbol": "Si",
          "number": 14,
          "weight": 28.0855,
          "boilingPoint": 3265,
          "meltingPoint": 1414,
          "density": 2.3296,
          "eneg": 1.9}
         )
    
    P: dict = field(default_factory=lambda: {
          "name": "phosphorus",
         "symbol": "P",
         "number": 15,
         "weight": 30.973762,
         "boilingPoint": 280.5,
         "meltingPoint": 44.15,
         "density": 1.82,
         "eneg": 2.19}
         )
    
    S: dict = field(default_factory=lambda: {
          "name": "sulfur",
         "symbol": "S",
         "number": 16,
         "weight": 32.065,
         "boilingPoint": 444.6,
         "meltingPoint": 115.21,
         "density": 2.067,
         "eneg": 2.58}
         )
    
    Cl: dict = field(default_factory=lambda: {
          "name": "chlorine",
          "symbol": "Cl",
          "number": 17,
          "weight": 35.453,
          "boilingPoint": -34.04,
          "meltingPoint": -101.5,
          "density": 0.003214,
          "eneg": 3.16}
         )
    
    Ar: dict = field(default_factory=lambda: {
          "name": "argon",
          "symbol": "Ar",
          "number": 18,
          "weight": 39.948,
          "boilingPoint": -185.85,
          "meltingPoint": -189.34,
          "density": 0.0017837,
          "eneg": None}
         )
    
    K: dict = field(default_factory=lambda: {
          "name": "potassium",
         "symbol": "K",
         "number": 19,
         "weight": 39.0983,
         "boilingPoint": 759,
         "meltingPoint": 63.38,
         "density": 0.862,
         "eneg": 0.82}
         )
    
    Ca: dict = field(default_factory=lambda: {
          "name": "calcium",
          "symbol": "Ca",
          "number": 20,
          "weight": 40.078,
          "boilingPoint": 1484,
          "meltingPoint": 842,
          "density": 1.54,
          "eneg": 1.0}
         )

    Fe: dict = field(default_factory=lambda: {
          "name": "iron",
          "symbol": "Fe",
          "number": 26,
          "weight": 55.845,
          "boilingPoint": 2861,
          "meltingPoint": 1538,
          "density": 7.874,
          "eneg": 1.83}
         )
    
    Cu: dict = field(default_factory=lambda: {
          "name": "copper",
          "symbol": "Cu",
          "number": 29,
          "weight": 63.546,
          "boilingPoint": 2562,
          "meltingPoint": 1084.62,
          "density": 8.96,
          "eneg": 1.9}
         )
    
    Zn: dict = field(default_factory=lambda: {
          "name": "zinc",
          "symbol": "Zn",
          "number": 30,
          "weight": 65.38,
          "boilingPoint": 907,
          "meltingPoint": 419.53,
          "density": 7.134,
          "eneg": 1.65}
         )
    
    Ag: dict = field(default_factory=lambda: {
          "name": "silver",
          "symbol": "Ag",
          "number": 47,
          "weight": 107.8682,
          "boilingPoint": 2162,
          "meltingPoint": 961.78,
          "density": 10.49,
          "eneg":1.93}
         )
    
    Au: dict = field(default_factory=lambda: {
          "name": "gold",
          "symbol": "Au",
          "number": 79,
          "weight": 196.966569,
          "boilingPoint": 2856,
          "meltingPoint": 1064.18,
          "density": 19.3,
          "eneg": 2.54}
         )
    
    Hg: dict = field(default_factory=lambda: {
          "name": "mercury",
          "symbol": "Hg",
          "number": 80,
          "weight": 200.59,
          "boilingPoint": 356.73,
          "meltingPoint": -38.83,
          "density": 13.546,
          "eneg": 2.0}
         )
    
    Pb: dict = field(default_factory=lambda: {
          "name": "lead",
          "symbol": "Pb",
          "number": 82,
          "weight": 207.2,
          "boilingPoint": 1749,
          "meltingPoint": 327.46,
          "density": 11.34,
          "eneg": 2.33}
         )
    
    U: dict = field(default_factory=lambda: {
         "name": "uranium",
         "symbol": "U",
         "number": 92,
         "weight": 238.02891,
         "boilingPoint": 4131,
         "meltingPoint": 1135,
         "density": 19.1,
         "eneg": 1.38}
         )

    @crystalline
    def __post_init__(self):
        pass

    @classmethod
    def cp(cls, element_dict) -> dict:
        if isinstance(element_dict, ImmutableDict):
            return dict(element_dict)
        return element_dict.copy()


class Constants(Enum):
    AVOGADRO: float = 6.0221408e+23     # Unitless
    GAS: float = 8.314                  # J/(mol•K)
    PLANCK: float = 6.63e-34            # (kg•m²)/s
    LIGHTSPEED: float = 2.99792458e+8   # m/s


# Reexport members of the `Constants` enum to use convenience aliases.
NA: float = Constants.AVOGADRO.value
R: float = Constants.GAS.value
h: float = Constants.PLANCK.value
c: float = Constants.LIGHTSPEED.value

