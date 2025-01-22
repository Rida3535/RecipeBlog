from abc import ABC, abstractmethod

# Abstract Base Class for Recipe
class Recipe(ABC):
    @abstractmethod
    def get_title(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_image(self):
        pass

    @abstractmethod
    def category(self):
        pass
