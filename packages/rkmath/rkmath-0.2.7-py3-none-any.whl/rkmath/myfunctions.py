import math
import numpy as np

def neliöjuuri(x):
    return math.sqrt(x)

def kuutiojuuri(x):
     return math.copysign(abs(x) ** (1/3), x) 
 

def summa(x,y):
     return x+y
 
def erotus(x,y):
     return x-y
 
def potenssi(x,y):
     return x**y
 
def suurinYhteinenTekijä(x,y):
     return math.gcd(x,y)
  
def keskiarvo(array):
    sum = 0
    for i in range(len(array)):
        sum += array[i]
    
    return sum/len(array)
         
def mediaani(array):
    return np.median(array)

def varianssi(array):
    return np.var(array)

def pythagoraanLause(a,b):
    return (math.sqrt(a**2 + b**2))

def hypotenuusa(a,b):
    return math.hypot(a,b)

def toisen_asteen_lause(a, b, c):
    d = b**2 - 4*a*c  
    if d > 0:
        vastaus1 = (-b + math.sqrt(d)) / (2*a)
        vastaus2 = (-b - math.sqrt(d)) / (2*a)
        return vastaus1, vastaus2
    elif d == 0:
        vastaus3 = -b / (2*a)
        return vastaus3,
    else:
        return "Ei reaalijuuria"
    

def etäisyys(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def elementtiensumma(array):
    sum = 0
    for i in range(len(array)):
        sum += array[i]
    
    return sum

def RKMathIsTheBestLibraryIHaveEverUsed():
    """
    This function helps to remind people that RKMATH is the best library ever.
    """
    return "RKMATH is the best library I have ever used!!!"
    
    
    