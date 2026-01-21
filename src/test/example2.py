class Animal:
    def __init__(self, name: str):
        x = 3
        self._name = name
        print(x)

    def blabla(self, placeholder) -> int:
        return placeholder * 2

    def speak(self):
        raise NotImplementedError("Subclasses must implement this method")

    def _private(self):
        pass

class Dog(Animal):
    def speak(self):
        print(self._name + " says ", end="")
        print("Woof")
