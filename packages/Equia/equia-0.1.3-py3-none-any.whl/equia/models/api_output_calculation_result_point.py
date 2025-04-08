from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.api_output_calculation_result_phase import ApiOutputCalculationResultPhase
from ..models.api_value_pressure import ApiValuePressure
from ..models.api_value_temperature import ApiValueTemperature
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiOutputCalculationResultPoint")


@attr.s(auto_attribs=True)
class ApiOutputCalculationResultPoint:
    """Result for a point"""

    temperature: Union[Unset, ApiValueTemperature] = UNSET
    pressure: Union[Unset, ApiValuePressure] = UNSET
    phases: Union[Unset, None, List[ApiOutputCalculationResultPhase]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        temperature: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.temperature, Unset):
            temperature = self.temperature.to_dict()

        pressure: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pressure, Unset):
            pressure = self.pressure.to_dict()

        phases: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.phases, Unset):
            if self.phases is None:
                phases = None
            else:
                phases = []
                for phases_item_data in self.phases:
                    phases_item = phases_item_data.to_dict()

                    phases.append(phases_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if pressure is not UNSET:
            field_dict["pressure"] = pressure
        if phases is not UNSET:
            field_dict["phases"] = phases

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _temperature = d.pop("temperature", UNSET)
        temperature: Union[Unset, ApiValueTemperature]
        if isinstance(_temperature, Unset):
            temperature = UNSET
        else:
            temperature = ApiValueTemperature.from_dict(_temperature)

        _pressure = d.pop("pressure", UNSET)
        pressure: Union[Unset, ApiValuePressure]
        if isinstance(_pressure, Unset):
            pressure = UNSET
        else:
            pressure = ApiValuePressure.from_dict(_pressure)

        phases = []
        _phases = d.pop("phases", UNSET)
        for phases_item_data in _phases or []:
            phases_item = ApiOutputCalculationResultPhase.from_dict(phases_item_data)

            phases.append(phases_item)

        api_output_calculation_result_point = cls(
            temperature=temperature,
            pressure=pressure,
            phases=phases,
        )

        return api_output_calculation_result_point

    def __str__(self, include_compositions: bool=True) -> str:
        """String representation of the flash calculation result."""
        def format_num(x):
            try:
                if isinstance(x, (int, float)):
                    return f"{float(x):.4f}"
            except Exception:
                pass
            return str(x)

        # Build header: first two columns are fixed ("Property" and "Unit")
        # Then one column per phase (using phase_label as header)
        phase_labels = [phase.phase_label for phase in self.phases]
        headers = ["Property", "Unit"] + phase_labels

        rows = []
        phase_count = len(self.phases)

        # Add Temperature row: value only in the first (System) phase column
        temp_obj = self.temperature
        temp_val = getattr(temp_obj, "value", None)
        temp_unit = getattr(temp_obj, "units", "")
        temp_formatted = format_num(temp_val) if temp_val is not None else "N/A"
        temp_row = ["Temperature", temp_unit] + [temp_formatted] + [""] * (phase_count - 1)
        rows.append(temp_row)

        # Add Pressure row: value only in the first (System) phase column
        press_obj = self.pressure
        press_val = getattr(press_obj, "value", None)
        press_unit = getattr(press_obj, "units", "")
        press_formatted = format_num(press_val) if press_val is not None else "N/A"
        press_row = ["Pressure", press_unit] + [press_formatted] + [""] * (phase_count - 1)
        rows.append(press_row)

        # List of phase-level properties to display (rows below Temperature/Pressure)
        phase_props = [
            ("Volume", "volume"),
            ("Density", "density"),
            ("Entropy", "entropy"),
            ("Enthalpy", "enthalpy"),
            ("Cp", "cp"),
            ("Cv", "cv"),
            ("JT Coefficient", "jt_coefficient"),
            ("Speed of Sound", "speed_of_sound"),
            ("Solubility Parameter", "solubility_parameter"),
            ("Molecular Weight", "molecular_weight"),
            ("Compressibility", "compressibility"),
            ("Mole Percent", "mole_percent"),
            ("Weight Percent", "weight_percent"),
        ]

        # For each property, build a row with property name, unit, and the value for each phase
        for disp_name, attr_name in phase_props:
            # Determine the unit from the first phase that has this attribute
            unit = ""
            for phase in self.phases:
                attr_obj = getattr(phase, attr_name, None)
                if attr_obj is not None:
                    unit = getattr(attr_obj, "units", "")
                    break
            row = [disp_name, unit]
            for phase in self.phases:
                attr_obj = getattr(phase, attr_name, None)
                if attr_obj is None:
                    row.append("N/A")
                else:
                    value = getattr(attr_obj, "value", attr_obj)
                    row.append(format_num(value))
            rows.append(row)

        # If compositions should be included...
        if include_compositions:
            # Add a divider row
            divider_row = ["-" * 5] * len(headers)
            rows.append(divider_row)
            # Check if the first phase has a composition
            if self.phases and hasattr(self.phases[0], "composition") and self.phases[0].composition is not None:
                comp0 = self.phases[0].composition
                comp_units = getattr(comp0, "composition_units", "")
                components = comp0.composition.components
                # For each composition component, add a row
                for i, comp in enumerate(components):
                    # Place composition_units only in the first composition row
                    unit_str = comp_units if i == 0 else ""
                    prop_name = comp.name
                    row = [prop_name, unit_str]
                    # For each phase, get the corresponding composition value (assume same ordering)
                    for phase in self.phases:
                        if hasattr(phase, "composition") and phase.composition is not None:
                            try:
                                comp_arr = phase.composition.composition.components
                                phase_comp = comp_arr[i]
                                val = getattr(phase_comp, "value", "N/A")
                                row.append(format_num(val))
                            except IndexError:
                                row.append("N/A")
                        else:
                            row.append("N/A")
                    rows.append(row)
                
        # Determine column widths
        all_rows = [headers] + rows
        num_cols = len(headers)
        col_widths = [
            max(len(str(all_rows[r][c])) for r in range(len(all_rows)))
            for c in range(num_cols)
        ]

        # Format the header and rows
        header_line = " | ".join(str(item).ljust(width) for item, width in zip(headers, col_widths))
        separator = "-+-".join("-" * width for width in col_widths)
        row_lines = [
            " | ".join(str(item).ljust(width) for item, width in zip(row, col_widths))
            for row in rows
        ]

        # Build the table
        table = "\n".join([header_line, separator] + row_lines)
        title = "Flash Calculation Result Point"
        return "\n" + title + "\n\n" + table
