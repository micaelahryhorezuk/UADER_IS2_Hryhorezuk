#Implemente una clase bajo el patrón iterator que almacene una cadena de caracteres 
#y permita recorrerla en sentido directo y reverso.

from dataclasses import dataclass
from typing import Iterator

@dataclass
class StringIterator:  #implementa el patrón iterator para una cadena de caracteres
    string: str
    reverse: bool = False

    def __iter__(self):
        if self.reverse:
            return reversed(self.string)
        return iter(self.string)

if __name__ == "__main__": #Ejemplo de uso de la clase StringIterator
    my_string = "Hello, World!"
    
    print("Iterando en sentido directo:")  #Itera a través de los caracteres de la cadena en sentido directo
    for char in StringIterator(my_string):
        print(char)

    print("\nIterando en sentido reverso:") #Itera a través de los caracteres de la cadena en sentido reverso
    for char in StringIterator(my_string, reverse=True):
        print(char)