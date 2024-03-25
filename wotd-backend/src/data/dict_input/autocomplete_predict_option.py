from dataclasses import dataclass


@dataclass
class AutocompletePredictOption:
    text: str
    logProb: float
