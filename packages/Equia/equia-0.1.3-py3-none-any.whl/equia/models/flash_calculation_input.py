"""
Module for representing a flash calculation input.
"""
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.calculation_composition import CalculationComposition
from ..models.api_fluid import ApiFluid
from ..types import UNSET, Unset

T = TypeVar("T", bound="FlashCalculationInput")


@attr.s(auto_attribs=True)
class FlashCalculationInput:
    """Input for flash calculation.

    Attributes
    ----------
    access_key : str
        Access key for the API.
    components : List[CalculationComposition] 
        Component composition
    flashtype : str 
        Type of flash to perform. 
        Allowed options: `{'Fixed Temperature/Pressure', 'Fixed Pressure/Enthalpy', 'Fixed Pressure/Entropy'}`
    units : str 
        Units used for input and output.
    fluidid : str 
        Id of fluid on webserver. Must be defined if `fluid` argument is not given.
    fluid : ApiFluid
        Fluid information
    temperature : float
        Temperature in units given in `units` argument.
    pressure : float
        Pressure in units given in `units` argument.
    enthalpy : float
        Enthalpy in units given in `units` argument.
    entropy : float
        Entropy in units given in `units` argument.
    """
    access_key: str
    components: List[CalculationComposition] # Component composition
    flashtype: str # Type of flash to perform. Allowed option: Fixed Temperature/Pressure, Fixed Pressure/Enthalpy or Fixed Pressure/Entropy
    units: str # Units used for input and output
    fluidid: Union[Unset, str] = UNSET #Id of fluid on webserver. Must be defined if no fluid given in fluid argument
    fluid: Union[Unset, ApiFluid] = UNSET #Fluid information
    temperature: Union[Unset, float] = UNSET #Temperature in units given in 'Units' argument
    pressure: Union[Unset, float] = UNSET #Pressure in units given in 'Units' argument
    enthalpy: Union[Unset, float] = UNSET #Enthalpy in units given in 'Units' argument
    entropy: Union[Unset, float] = UNSET #Entropy in units given in 'Units' argument

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of this object."""
        access_key = self.access_key
        components = []
        for components_item_data in self.components:
            components_item = components_item_data.to_dict()
            components.append(components_item)

        flashtype = self.flashtype
        units = self.units
        temperature = self.temperature
        pressure = self.pressure
        enthalpy = self.enthalpy
        entropy = self.entropy

        fluidid: Union[Unset, str] = UNSET
        if not isinstance(self.fluidid, Unset):
            fluid = self.fluidid

        fluid: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fluid, Unset):
            fluid = self.fluid.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "accessKey": access_key,
                "components": components,
                "flashType": flashtype,
            }
        )
        if not isinstance(units, Unset):
            field_dict["units"] = units
        if not isinstance(fluidid, Unset):
            field_dict["fluidId"] = fluidid
        if not isinstance(fluid, Unset):
            field_dict["fluid"] = fluid
        if not isinstance(temperature, Unset):
            field_dict["temperature"] = temperature
        if not isinstance(pressure, Unset):
            field_dict["pressure"] = pressure
        if not isinstance(enthalpy, Unset):
            field_dict["enthalpy"] = enthalpy
        if not isinstance(entropy, Unset):
            field_dict["entropy"] = entropy

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of `FlashCalculationInput` from a dict representation."""
        d = src_dict.copy()
        access_key = d.pop("accessKey")
        flashtype = d.pop("flashType")
        units = d.pop("units", UNSET)

        components = []
        _components = d.pop("components")
        for components_item_data in _components:
            components_item = CalculationComposition.from_dict(
                components_item_data)

            components.append(components_item)

        _fluidid = d.pop("fluidId", UNSET)
        fluidid: Union[Unset, str]
        if isinstance(_fluidid, Unset):
            fluidid = UNSET
        else:
            fluidid = _fluidid

        _fluid = d.pop("fluid", UNSET)
        fluid: Union[Unset, ApiFluid]
        if isinstance(_fluid, Unset):
            fluid = UNSET
        else:
            fluid = ApiFluid.from_dict(_fluid)

        temperature = d.pop("temperature", UNSET)
        pressure = d.pop("pressure", UNSET)
        enthalpy = d.pop("enthalpy", UNSET)
        entropy = d.pop("entropy", UNSET)

        flash_calculation_input = cls(
            access_key=access_key,
            components=components,
            flashtype=flashtype,
            units=units,
            fluidid=fluidid,
            fluid=fluid,
            temperature=temperature,
            pressure=pressure,
            enthalpy=enthalpy,
            entropy=entropy,
        )

        return flash_calculation_input

    def __str__(self) -> str:
        """
        Returns a string representation of the `FlashCalculationInput` instance.
        
        Includes:
        - Flash type, units, specifications, fluid composition and parameters.
        """
        parts = ["\n"]
        parts.append("FlashCalculationInput:")
        
        # Flash Info
        parts.append(f"  Flash Type: {self.flashtype}")
        parts.append(f"  Units: {self.units}")
        parts.append(f"  Fluid ID: {self.fluidid if not isinstance(self.fluidid, Unset) else 'N/A'}")
        
        # Specifications
        def fmt_val(val, label):
            return f"  {label}: {val}" if not isinstance(val, Unset) else f"  {label}: N/A"

        parts.append(fmt_val(self.temperature, "Temperature"))
        parts.append(fmt_val(self.pressure, "Pressure"))
        parts.append(fmt_val(self.enthalpy, "Enthalpy"))
        parts.append(fmt_val(self.entropy, "Entropy"))

        # Composition
        if self.components:
            parts.append("  Components:")
            for c in self.components:
                parts.append("    " + str(c).replace("\n", "\n    "))
        else:
            parts.append("  Components: N/A")

        # Fluid
        if not isinstance(self.fluid, Unset) and self.fluid is not None:
            parts.append("  Fluid:")
            parts.append("    " + str(self.fluid).replace("\n", "\n    "))
        else:
            parts.append("  Fluid: N/A")

        return "\n".join(parts)
