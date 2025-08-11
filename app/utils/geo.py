import math

from ..schemas import TransportMode

MODE_MAP = {
    TransportMode.foot: "walking",
    TransportMode.bike: "bicycling",
    TransportMode.car: "driving",
    TransportMode.public: "transit",
}


def normalize_mode(mode: TransportMode) -> str:
    return MODE_MAP[mode]


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c
