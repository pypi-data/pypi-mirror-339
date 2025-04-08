"""
Module for representing a component composition of a fluid mixture.

This class is intended to serialize/deserialize data in a format compatible with the VLXE API.
"""
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.api_fluid_distribution_moment import ApiFluidDistributionMoment
from ..models.calculation_block_info import CalculationBlockInfo
from ..types import UNSET, Unset

T = TypeVar("T", bound="CalculationComposition")


@attr.s(auto_attribs=True)
class CalculationComposition:
    """Holds composition information for a component.
    
    Stores the compositional information for a component, which is to be stored in the `FlashCalculationInput.components` attribute.
    
    Attributes
    ----------
    component_id : str
        Id of the component.
    component_name : str
        Name of the component.
    mass : float
        Mass fraction of the component.
    sorting_order : int
        Index for sorting the components.
    moment : ApiFluidDistributionMoment
        Distribution moment information for the component.
    block_infos : List[CalculationBlockInfo]
        Block information for the component.
    """

    component_id: Union[Unset, str] = UNSET
    component_name: Union[Unset, None, str] = UNSET
    mass: Union[Unset, float] = UNSET
    sorting_order: Union[Unset, int] = UNSET
    moment: Union[Unset, ApiFluidDistributionMoment] = UNSET
    block_infos: Union[Unset, None, List[CalculationBlockInfo]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of this object."""
        component_id = self.component_id
        component_name = self.component_name
        mass = self.mass
        sorting_order = self.sorting_order
        moment: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.moment, Unset):
            moment = self.moment.to_dict()

        block_infos: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.block_infos, Unset):
            if self.block_infos is None:
                block_infos = None
            else:
                block_infos = []
                for block_infos_item_data in self.block_infos:
                    block_infos_item = block_infos_item_data.to_dict()

                    block_infos.append(block_infos_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if not isinstance(component_id, Unset):
            field_dict["componentId"] = component_id
        if not isinstance(component_name, Unset):
            field_dict["componentName"] = component_name
        if not isinstance(mass, Unset):
            field_dict["mass"] = mass
        if not isinstance(sorting_order, Unset):
            field_dict["sortingOrder"] = sorting_order
        if not isinstance(moment, Unset):
            field_dict["moment"] = moment
        if not isinstance(block_infos, Unset):
            field_dict["blockInfos"] = block_infos

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of this class from a dict."""
        d = src_dict.copy()
        component_id = d.pop("componentId", UNSET)

        component_name = d.pop("componentName", UNSET)

        mass = d.pop("mass", UNSET)

        sorting_order = d.pop("sortingOrder", UNSET)

        _moment = d.pop("moment", UNSET)
        moment: Union[Unset, ApiFluidDistributionMoment]
        if isinstance(_moment, Unset):
            moment = UNSET
        else:
            moment = ApiFluidDistributionMoment.from_dict(_moment)

        block_infos = []
        _block_infos = d.pop("blockInfos", UNSET)
        for block_infos_item_data in _block_infos or []:
            block_infos_item = CalculationBlockInfo.from_dict(block_infos_item_data)

            block_infos.append(block_infos_item)

        calculation_composition = cls(
            component_id=component_id,
            component_name=component_name,
            mass=mass,
            sorting_order=sorting_order,
            moment=moment,
            block_infos=block_infos,
        )

        return calculation_composition

    def __str__(self) -> str:
        """
        Returns a string representation of the `CalculationComposition` instance.
        
        Includes:
        - Component name, ID, mass, sorting order, moment, and block infos.
        """
        parts = []
        name = self.component_name if not isinstance(self.component_name, Unset) else "N/A"
        comp_id = self.component_id if not isinstance(self.component_id, Unset) else "N/A"
        mass = self.mass if not isinstance(self.mass, Unset) else "N/A"
        order = self.sorting_order if not isinstance(self.sorting_order, Unset) else "N/A"
        
        parts.append(f"Component: {name} (ID: {comp_id})")
        parts.append(f"  Mass: {mass}")
        parts.append(f"  Sorting Order: {order}")

        # Moment
        if not isinstance(self.moment, Unset) and self.moment is not None:
            parts.append("  Moment:")
            parts.append("    " + str(self.moment).replace("\n", "\n    "))
        else:
            parts.append("  Moment: N/A")

        # Block Infos
        if not isinstance(self.block_infos, Unset) and self.block_infos:
            parts.append("  Block Infos:")
            for b in self.block_infos:
                parts.append("    " + str(b).replace("\n", "\n    "))
        else:
            parts.append("  Block Infos: N/A")

        return "\n".join(parts)
