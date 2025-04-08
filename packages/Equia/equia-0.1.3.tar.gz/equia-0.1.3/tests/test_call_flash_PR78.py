import pytest
from equia.models import CalculationComposition, ProblemDetails 
from equia.equia_client import EquiaClient
from equia.demofluids.demofluid_Methane_nHexane_Toluene import demofluid_Methane_nHexane_Toluene
from utility.shared_settings import sharedsettings

@pytest.mark.asyncio
async def test_call_flash_PR78():
    client = EquiaClient(sharedsettings.url, sharedsettings.access_key)

    input = client.get_flash_input()
    input.temperature = 25
    input.pressure = 10
    input.components = [
        CalculationComposition(mass=0.10),
        CalculationComposition(mass=0.50),
        CalculationComposition(mass=0.40)
    ]
    input.flashtype = "Fixed Temperature/Pressure"

    input.fluid = demofluid_Methane_nHexane_Toluene(is_volume_shift=True)
    input.units = "C(In,Massfraction);C(Out,Massfraction);T(In,Celsius);T(Out,Celsius);P(In,Bar);P(Out,Bar);H(In,kJ/Kg);H(Out,kJ/Kg);S(In,kJ/(Kg Kelvin));S(Out,kJ/(Kg Kelvin));Cp(In,kJ/(Kg Kelvin));Cp(Out,kJ/(Kg Kelvin));Viscosity(In,centiPoise);Viscosity(Out,centiPoise);Surfacetension(In,N/m);Surfacetension(Out,N/m)"

    # Print the input for debugging purposes
    print(input)
    
    # Call the flash calculation asynchronously
    result: ProblemDetails = await client.call_flash_async(input)

    # Print the result for debugging purposes
    print(result)
    
    await client.cleanup()

    #assert result.status == 400
    assert result.success
    assert len(result.point.phases) == 3
