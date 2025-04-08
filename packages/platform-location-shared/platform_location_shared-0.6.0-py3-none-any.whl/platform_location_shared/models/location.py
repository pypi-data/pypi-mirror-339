from typing import Dict, Union

from platform_location_shared.models.mixins.serialise import Serialisable
from platform_location_shared.validations.postcode import postcode_field, Postcode


class InitialInputLocation(Serialisable):
    post_code: Postcode = postcode_field


class GooglePlacesLocation(InitialInputLocation):
    latitude: float
    longitude: float
    street_address: str
    city: str
    province: str
    province_code: str
    state: str
    state_code: str
    country: str
    country_code: str


class ONSLocation(InitialInputLocation):
    lsoa: str
    itl: str
    icb: str
    sicbl: str
    oslaua: str
    pcon: str
    population_area_km2: float
    population_population: int
    population_people_per_km2: int


class FullLocation(GooglePlacesLocation, ONSLocation):
    pass


BatchGooglePlacesLocation = Dict[str, Union[FullLocation, None]]
