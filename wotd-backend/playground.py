from flask import jsonify


class TestClass:

    def __init__(self):
        self.intTest: int = 32
        self.textTest: str = 'test'


inst = jsonify(TestClass())
print("inst: ", inst)
