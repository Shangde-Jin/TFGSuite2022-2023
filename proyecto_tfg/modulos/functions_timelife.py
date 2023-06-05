# En este script están todas las funciones para calcular el tiempo de recombinación.
import math
import numpy as np
from .movilidad import sinton_mode
from .movilidad import dorkel_mode
from .movilidad import klaassen_mode
from .movilidad import schindler_mode
###########
# DEF CTE #
###########
VPER_SUN = 0.008 #Unidades : [V/sun]
A = 0
B = 0.034
OFFSET= 0.038
DARK_VOLTAGE = 0 # primero se usa este valor, posteriormente habrá que volver a definirlo
AIR_VOLTAGE = 1 # quitarlo o no?
OPTICAL_FACTOR = 0.70
C = OFFSET
Q = 1.6e-19 #[Coulomb]
K = DARK_VOLTAGE - OFFSET
W= 0.0300 #Unidades : [cm]

# Variables para el calculo del tiempo intrínseco
N0EEHN0 = 3.3e+17 # unidades [cm^-3]
N0EEHP0 = 7.0e+17 # unidades [cm^-3]
BLOW = 4.73e-15 # unidades[cm^3/s]
BREL = 1
NDOP=1e+17 #unidades [cm^-3]
# NI = 1e+10 #unidades [cm^-3]
NC = 3e+19 #unidades [cm^-3]
NV = 1e+19 #unidades [cm^-3]
NA = 1e+19 #unidades [cm^-3] FALTA COMPROBAR!
EG = 1.1242 #Energy Bandgap unidades [eV]
K = 8.617333262145e-5 #cte Boltzmann unidades [eV/K]

# Se pasa como parámetro Vref y se calcula la tasa de generación.
def generacion(Vref):
    generacion = (Vref/VPER_SUN)*0.038*(OPTICAL_FACTOR/Q)
    return generacion
# Se pasa como parámetro Vph y se calcula la fotoconductividad.
def fotoconductividad(Vph):
    fotoconductividad = ((Vph + K) * ((Vph + K)*A + B)) -K*(K*A + B)
    return fotoconductividad

# Se pasan como parámetros la fotoconductividad, movilidad inicial, la elección del usuario
# del tipo de movilidad y la temperatura
# Se calcula la densidad de portadores iterando 2 veces para conseguir un valor más preciso.
# El usuario puede elegir entre los distintos tipos de movilidad (Sinton, Dorkel, Klaassen y Schindler).
def densidad_portadores(fotoconductividad, movilidad_inicial, choice, temperatura):
    lista_densidad_portadores0 = []
    lista_densidad_portadores1 = []
    lista_densidad_portadores2 = []
    funciones_modos = {
        "Sinton": sinton_mode.sinton_mode,
        "Dorkel": dorkel_mode.dorkel_mode,
        "Klaassen": klaassen_mode.klaassen_mode,
        "Schindler": schindler_mode.schindler_mode,
        "Sinton-Intrinseco": sinton_mode.sinton_mode,
        "Dorkel-Intrinseco": dorkel_mode.dorkel_mode,
        "Klaassen-Intrinseco": klaassen_mode.klaassen_mode,
        "Schindler-Intrinseco": schindler_mode.schindler_mode
    }
    funcion_modo = funciones_modos.get(choice)
    if not funcion_modo:
        raise ValueError("Opción de choice inválida.")
    for fotoconduc in fotoconductividad:
        densidad_portadores0 = fotoconduc / (Q * W * movilidad_inicial)
        lista_densidad_portadores0.append(densidad_portadores0)
        movilidad_primeraIteracion = funcion_modo(temperatura, lista_densidad_portadores0)
        densidad_portadores1 = (densidad_portadores0 * movilidad_inicial) / movilidad_primeraIteracion[-1]
        lista_densidad_portadores1.append(densidad_portadores1)
        movilidad_segundaIteracion = funcion_modo(temperatura, lista_densidad_portadores1)
        densidad_portadores2 = (densidad_portadores1 * movilidad_primeraIteracion[-1]) / movilidad_segundaIteracion[-1]
        lista_densidad_portadores2.append(densidad_portadores2)
    return lista_densidad_portadores2

def densidad_portadores_sinton(fotoconductividad, movilidad_inicial, choice, temperatura):
    lista_densidad_portadores0 = []
    lista_densidad_portadores1 = []
    lista_densidad_portadores2 = []
    for fotoconduc in fotoconductividad:
        densidad_portadores0 = fotoconduc / (Q * W * movilidad_inicial)
        lista_densidad_portadores0.append(densidad_portadores0)
        movilidad_primeraIteracion = sinton_mode.sinton_mode(temperatura, lista_densidad_portadores0)
        densidad_portadores1 = (densidad_portadores0 * movilidad_inicial) / movilidad_primeraIteracion[-1]
        lista_densidad_portadores1.append(densidad_portadores1)
        movilidad_segundaIteracion = sinton_mode.sinton_mode(temperatura, lista_densidad_portadores1)
        densidad_portadores2 = (densidad_portadores1 * movilidad_primeraIteracion[-1]) / movilidad_segundaIteracion[-1]
        lista_densidad_portadores2.append(densidad_portadores2)
    return lista_densidad_portadores2

def densidad_portadores_dorkel(fotoconductividad, movilidad_inicial, choice, temperatura):
    lista_densidad_portadores0 = []
    lista_densidad_portadores1 = []
    lista_densidad_portadores2 = []
    for fotoconduc in fotoconductividad:
        densidad_portadores0 = fotoconduc / (Q * W * movilidad_inicial)
        lista_densidad_portadores0.append(densidad_portadores0)
        movilidad_primeraIteracion = dorkel_mode.dorkel_mode(temperatura, lista_densidad_portadores0)
        densidad_portadores1 = (densidad_portadores0 * movilidad_inicial) / movilidad_primeraIteracion[-1]
        lista_densidad_portadores1.append(densidad_portadores1)
        movilidad_segundaIteracion = dorkel_mode.dorkel_mode(temperatura, lista_densidad_portadores1)
        densidad_portadores2 = (densidad_portadores1 * movilidad_primeraIteracion[-1]) / movilidad_segundaIteracion[-1]
        lista_densidad_portadores2.append(densidad_portadores2)
    return lista_densidad_portadores2

def densidad_portadores_klaassen(fotoconductividad, movilidad_inicial, choice, temperatura):
    lista_densidad_portadores0 = []
    lista_densidad_portadores1 = []
    lista_densidad_portadores2 = []
    for fotoconduc in fotoconductividad:
        densidad_portadores0 = fotoconduc / (Q * W * movilidad_inicial)
        lista_densidad_portadores0.append(densidad_portadores0)
        movilidad_primeraIteracion = klaassen_mode.klaassen_mode(temperatura, lista_densidad_portadores0)
        densidad_portadores1 = (densidad_portadores0 * movilidad_inicial) / movilidad_primeraIteracion[-1]
        lista_densidad_portadores1.append(densidad_portadores1)
        movilidad_segundaIteracion = klaassen_mode.klaassen_mode(temperatura, lista_densidad_portadores1)
        densidad_portadores2 = (densidad_portadores1 * movilidad_primeraIteracion[-1]) / movilidad_segundaIteracion[-1]
        lista_densidad_portadores2.append(densidad_portadores2)
    return lista_densidad_portadores2

def densidad_portadores_schindler(fotoconductividad, movilidad_inicial, choice, temperatura):
    lista_densidad_portadores0 = []
    lista_densidad_portadores1 = []
    lista_densidad_portadores2 = []
    for fotoconduc in fotoconductividad:
        densidad_portadores0 = fotoconduc / (Q * W * movilidad_inicial)
        lista_densidad_portadores0.append(densidad_portadores0)
        movilidad_primeraIteracion = schindler_mode.schindler_mode(temperatura, lista_densidad_portadores0)
        densidad_portadores1 = (densidad_portadores0 * movilidad_inicial) / movilidad_primeraIteracion[-1]
        lista_densidad_portadores1.append(densidad_portadores1)
        movilidad_segundaIteracion = schindler_mode.schindler_mode(temperatura, lista_densidad_portadores1)
        densidad_portadores2 = (densidad_portadores1 * movilidad_primeraIteracion[-1]) / movilidad_segundaIteracion[-1]
        lista_densidad_portadores2.append(densidad_portadores2)
    return lista_densidad_portadores2
    
# Se calcula el tiempo de recombinación a partir de los parámetros densidad_portadores
# generación y el tiempo
def tiempo_recombinacion(densidad_portadores, generacion, t):
    derivada = np.gradient(np.array(densidad_portadores),np.array(t))
    lista_recombinacion = []
    for indice_densidad_portadores, indice_generacion, indice_derivada in zip (densidad_portadores,generacion,derivada):
        indice_recombinacion = indice_densidad_portadores/ ((indice_generacion/W)-indice_derivada)
        lista_recombinacion.append(indice_recombinacion)
    return lista_recombinacion

# Se calcula el tiempo de vida intrínseco que incluye auger y radiactiva
def tiempo_intrinseco(densidad_portadores, temperatura):
    # Se definen las variables que se van a usar
    lista_intrinseco = []
    NI = (math.sqrt(NC*NV)) * ((math.e)**((-EG)/(2*K*temperatura)))
    p0 = NDOP
    n0 = math.pow(NI,2)/NDOP
    geehn0 = (1) + (13)*(1 - math.tanh(math.pow(n0/N0EEHN0, 0.66)))
    geehp0 = (1) + (7.5)*(1 - math.tanh(math.pow(p0/N0EEHP0, 0.63)))
    beta = 1/(K*temperatura)
    nieff = (NI)*((math.e)**(beta*EG/2))
    for i in range(len(densidad_portadores)):
        p = (p0) + densidad_portadores[i]
        n = (n0) + densidad_portadores[i]
        # Se va a definir la función a trozos
        intriseco_numerador = densidad_portadores[i]
        intrinseco_denominador1 = (n*p) - (NI**2)
        intrinseco_denominador2 = (2.5e-31*geehn0) + (8.5e-32*geehp0) + ((3.0e-29)*math.pow(densidad_portadores[i],0.92)) + (BREL*BLOW)
        intrinseco_denominador = (intrinseco_denominador1) * (intrinseco_denominador2)
        intrinseco = (intriseco_numerador)/(intrinseco_denominador)
        lista_intrinseco.append(intrinseco)
    return lista_intrinseco

# Se calcula 1/tiempo eff - 1/tiempo intrinseco
def tiempo_srh(tiempo_intrinseco, tiempo_recombinacion):
    lista_diferencia_tiempo = []
    for i in range(len(tiempo_intrinseco)):
        indice = 1/tiempo_recombinacion[i] - 1/tiempo_intrinseco[i]
        lista_diferencia_tiempo.append(1/indice)
    return lista_diferencia_tiempo
    
        

    


        