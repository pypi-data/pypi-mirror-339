from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.calculation_composition import CalculationComposition
from ..models.api_fluid import ApiFluid
from ..types import UNSET, Unset

T = TypeVar("T", bound="EosPropertiesTPnCalculationInput")


@attr.s(auto_attribs=True)
class EosPropertiesTPnCalculationInput:
    """Input to EoS TPn property calculation. 

    Attributes
    ----------
    access_key : str
        Access key for the API. This is used to authenticate the user.
    components : List[CalculationComposition]
        List of components in the mixture.
    units : str
        Units for the calculation.
    volumetype : str
        Volume root to use. Allowed values are: `{'Auto', 'Liquid', 'Vapor'}`
    fluidid : str
        Id of fluid on webserver. Must be defined if no fluid given in fluid argument
    fluid : ApiFluid
        Fluid information
    temperature : float
        Temperature in units given in `units` argument.
    pressure : float
        Pressure in units given in `units` argument.
    """

    access_key: str
    components: List[CalculationComposition]
    units: str
    volumetype: str # Volume root to use. Allowed values are: Auto, Liquid, Vapor
    fluidid: Union[Unset, str] = UNSET #Id of fluid on webserver. Must be defined if no fluid given in fluid argument
    fluid: Union[Unset, ApiFluid] = UNSET #Fluid information
    temperature: Union[Unset, float] = UNSET
    pressure: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of this object."""
        access_key = self.access_key
        components = []
        for components_item_data in self.components:
            components_item = components_item_data.to_dict()
            components.append(components_item)

        units = self.units
        volumetype = self.volumetype
        
        temperature = self.temperature
        pressure = self.pressure

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
                "components": components
            }
        )
        if not isinstance(units, Unset):
            field_dict["units"] = units
        if not isinstance(volumetype, Unset):
            field_dict["volumetype"] = volumetype
        if not isinstance(fluidid, Unset):
            field_dict["fluidId"] = fluidid
        if not isinstance(fluid, Unset):
            field_dict["fluid"] = fluid
        if not isinstance(temperature, Unset):
            field_dict["temperature"] = temperature
        if not isinstance(pressure, Unset):
            field_dict["pressure"] = pressure

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of `EosPropertiesTPnCalculationInput` from a dict representation."""
        d = src_dict.copy()

        access_key = d.pop("accessKey")

        components = []
        _components = d.pop("components")
        for components_item_data in _components:
            components_item = CalculationComposition.from_dict(components_item_data)

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

        units = d.pop("units", UNSET)
        volumetype = d.pop("volumetype", UNSET)
        
        temperature = d.pop("temperature", UNSET)

        pressure = d.pop("pressure", UNSET)

        eospropertiestpn_calculation_input = cls(
            access_key=access_key,
            components=components,
            fluidid=fluidid,
            fluid=fluid,
            units=units,
            volumetype=volumetype,
            temperature=temperature,
            pressure=pressure,
        )

        return eospropertiestpn_calculation_input

    def __str__(self) -> str:
        """
        Returns a readable string representation of the TPn calculation input.
        """
        lines = ["EosPropertiesTPnCalculationInput:"]

        lines.append(f"  Fluid ID: {self.fluidid if not isinstance(self.fluidid, Unset) else 'N/A'}")
        lines.append(f"  Units: {self.units}")
        lines.append(f"  Temperature: {self.temperature if not isinstance(self.temperature, Unset) else 'N/A'}")
        lines.append(f"  Pressure: {self.pressure if not isinstance(self.pressure, Unset) else 'N/A'}")
        lines.append(f"  Volume Type: {self.volumetype}")

        # Components
        if self.components:
            lines.append("  Components:")
            for comp in self.components:
                lines.append("    " + str(comp).replace("\n", "\n    "))
        else:
            lines.append("  Components: None")

        # Fluid
        if not isinstance(self.fluid, Unset) and self.fluid:
            lines.append("  Fluid:")
            lines.append("    " + str(self.fluid).replace("\n", "\n    "))
        else:
            lines.append("  Fluid: N/A")

        return "\n".join(lines)
