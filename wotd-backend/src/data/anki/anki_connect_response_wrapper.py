from dataclasses import dataclass

@dataclass
class AnkiConnectResponseWrapper:
    result: str
    error: str
