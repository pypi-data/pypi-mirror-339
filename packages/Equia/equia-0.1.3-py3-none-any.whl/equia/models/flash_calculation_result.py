from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.api_output_calculation_result_point import ApiOutputCalculationResultPoint
from ..models.api_profile_information import ApiProfileInformation
from ..models.exception_info import ExceptionInfo
from ..types import UNSET, Unset

T = TypeVar("T", bound="FlashCalculationResult")


@attr.s(auto_attribs=True)
class FlashCalculationResult:
    """Holds calculation result for a point. 
    
    Attributes
    ----------
    success : bool
        Indicates if the calculation was successful.
    calculation_id : str
        Unique identifier for the calculation.
    exception_info : ExceptionInfo
        Information about any exceptions that occurred during the calculation.
    profiling : ApiProfileInformation
        Information about the profiling of the calculation.
    point : ApiOutputCalculationResultPoint
        Calculation result for the point.
    """

    success: Union[Unset, bool] = UNSET
    calculation_id: Union[Unset, None, str] = UNSET
    exception_info: Union[Unset, ExceptionInfo] = UNSET
    profiling: Union[Unset, ApiProfileInformation] = UNSET
    point: Union[Unset, ApiOutputCalculationResultPoint] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Dictionary representation of the object."""
        success = self.success
        calculation_id = self.calculation_id
        exception_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.exception_info, Unset):
            exception_info = self.exception_info.to_dict()

        profiling: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.profiling, Unset):
            profiling = self.profiling.to_dict()

        point: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.point, Unset):
            point = self.point.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if not isinstance(success, Unset):
            field_dict["success"] = success
        if not isinstance(calculation_id, Unset):
            field_dict["calculationId"] = calculation_id
        if not isinstance(exception_info, Unset):
            field_dict["exceptionInfo"] = exception_info
        if not isinstance(profiling, Unset):
            field_dict["profiling"] = profiling
        if not isinstance(point, Unset):
            field_dict["point"] = point

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of `FlashCalculationResult` from a dict representation."""
        d = src_dict.copy()
        success = d.pop("success", UNSET)

        calculation_id = d.pop("calculationId", UNSET)

        _exception_info = d.pop("exceptionInfo", UNSET)
        exception_info: Union[Unset, ExceptionInfo]
        if isinstance(_exception_info, Unset):
            exception_info = UNSET
        else:
            exception_info = ExceptionInfo.from_dict(_exception_info)

        _profiling = d.pop("profiling", UNSET)
        profiling: Union[Unset, ApiProfileInformation]
        if isinstance(_profiling, Unset):
            profiling = UNSET
        else:
            profiling = ApiProfileInformation.from_dict(_profiling)

        _point = d.pop("point", UNSET)
        point: Union[Unset, ApiOutputCalculationResultPoint]
        if isinstance(_point, Unset):
            point = UNSET
        else:
            point = ApiOutputCalculationResultPoint.from_dict(_point)

        flash_calculation_result = cls(
            success=success,
            calculation_id=calculation_id,
            exception_info=exception_info,
            profiling=profiling,
            point=point,
        )

        return flash_calculation_result

    def __str__(self) -> str:
        """
        Returns a string representation of the FlashCalculationResult instance.
        
        The string includes:
        - Success (True/False),
        - Calculation ID (if available; otherwise, "N/A"),
        - Exception Info (if available; otherwise, "N/A"),
        - Profiling (if available; otherwise, "N/A"),
        - Point (if available; otherwise, "N/A").

        Returns
        -------
        str
            A string representation of the instance.
        """
        parts = ["\n"]
        parts.append("FlashCalculationResult:")
        # Success and Calculation ID
        success_str = self.success if not isinstance(self.success, Unset) else "N/A"
        calc_id_str = self.calculation_id if not isinstance(self.calculation_id, Unset) else "N/A"
        parts.append(f"  Success: {success_str}")
        parts.append(f"  Calculation ID: {calc_id_str}")
        
        # Exception Info
        if not isinstance(self.exception_info, Unset) and self.exception_info is not None:
            parts.append(f"  Exception Info: {self.exception_info}")
        else:
            parts.append("  Exception Info: N/A")
        
        # Profiling
        if not isinstance(self.profiling, Unset) and self.profiling is not None:
            parts.append("  Profiling:")
            # Call the __str__ method of profiling
            parts.append("    " + str(self.profiling).replace("\n", "\n    "))
        else:
            parts.append("  Profiling: N/A")
        
        # Point
        if not isinstance(self.point, Unset) and self.point is not None:
            parts.append("  Point:")
            # Call the __str__ method of point
            parts.append("    " + str(self.point).replace("\n", "\n    "))
        else:
            parts.append("  Point: N/A")
        
        return "\n".join(parts)
