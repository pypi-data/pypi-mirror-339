from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.api_value_composition_array import ApiValueCompositionArray
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiOutputCalculationResultPhaseComposition")


@attr.s(auto_attribs=True)
class ApiOutputCalculationResultPhaseComposition:
    """Holds composition information for a phase.
    
    Attributes
    ----------
    composition_units : str
        Units of the composition.
    molar_mass_units : str
        Units of the molar mass.
    composition : ApiValueCompositionArray
        Composition of the phase.
    """

    composition_units: Union[Unset, None, str] = UNSET
    molar_mass_units: Union[Unset, None, str] = UNSET
    composition: Union[Unset, ApiValueCompositionArray] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of this object."""
        composition_units = self.composition_units
        molar_mass_units = self.molar_mass_units
        composition: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.composition, Unset):
            composition = self.composition.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if not isinstance(composition_units, Unset):
            field_dict["compositionUnits"] = composition_units
        if not isinstance(molar_mass_units, Unset):
            field_dict["molarMassUnits"] = molar_mass_units
        if not isinstance(composition, Unset):
            field_dict["composition"] = composition

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of this class from a dictionary."""
        d = src_dict.copy()
        composition_units = d.pop("compositionUnits", UNSET)

        molar_mass_units = d.pop("molarMassUnits", UNSET)

        _composition = d.pop("composition", UNSET)
        composition: Union[Unset, ApiValueCompositionArray]
        if isinstance(_composition, Unset):
            composition = UNSET
        else:
            composition = ApiValueCompositionArray.from_dict(_composition)

        api_output_calculation_result_phase_composition = cls(
            composition_units=composition_units,
            molar_mass_units=molar_mass_units,
            composition=composition,
        )

        return api_output_calculation_result_phase_composition

    def __str__(self) -> str:
        """
        Returns a string representation of the phase composition.
        """
        units = self.composition_units if not isinstance(self.composition_units, Unset) else "N/A"
        mm_units = self.molar_mass_units if not isinstance(self.molar_mass_units, Unset) else "N/A"
        lines = [f"Units: {units}, Molar Mass Units: {mm_units}"]

        if not isinstance(self.composition, Unset) and self.composition is not None:
            lines.append(str(self.composition))
        else:
            lines.append("Composition: N/A")

        return "\n".join(lines)
