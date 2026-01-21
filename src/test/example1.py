class Animal:
    def __init__(self, name: str):
        x = 3
        self.name: str = name
        print(x)

    def blabla(self, placeholder: int) -> int:
        return placeholder * 2

    def speak(self) -> None:
        raise NotImplementedError("Subclasses must implement this method")


class Dog(Animal):
    def speak(self):
        print(self.name + " says ", end="")
        print("Woof")
