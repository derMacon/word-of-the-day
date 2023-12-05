import json
from dataclasses import dataclass, field, asdict

from enum import Enum

class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

@dataclass
class Person:
    name: str
    gender: Gender
    age: int

    def __post_init__(self):
        if isinstance(self.gender, str):
            self.gender = Gender(self.gender)

# JSON data
json_data = '''
{
    "name": "John Doe",
    "gender": "MALE",
    "age": 25
}
'''

# Convert JSON to a dictionary
data_dict = json.loads(json_data)

# Convert dictionary to a Person dataclass instance
person_instance = Person(**data_dict)

print(person_instance)
print(type(person_instance.gender))
