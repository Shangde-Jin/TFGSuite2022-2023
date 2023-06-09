# Script donde se toma los valores del archivo excel, se tratan llamando a functions_timelife y se pinta 
# la curva de vida
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from .. import functions_timelife
from .. import functions_curvefit

class LifetimeGraphic:
    def __init__(self, path):
        self.path = path
        #definimos las columnas iniciales
        num_cols = 3
        if path.endswith('.xlsx'):
            # Se lee el archivo excel y se toma las columnas necesarias
            self.datos = pd.read_excel(path, usecols=range(num_cols))
            # Tomamos 2 valores posteriores al máximo de la columna de Photovoltage
            self.datos = self.datos.loc[self.datos.iloc[:,1] >=0]
            max_index = self.datos.iloc[:, 1].idxmax() +2
            self.lista_nueva = self.datos.loc[max_index:]
        else:
            self.datos = pd.read_csv(path, header = 0, delimiter='\t', usecols=range(num_cols)) 
            # Se toman los valores de la segunda columna
            columnas_numericas = [0, 1, 2]
            # Se toman los valores de la segunda columna
            self.datos.iloc[:, columnas_numericas] = self.datos.iloc[:, columnas_numericas].apply(lambda x: x.str.replace(',', '.').astype(float))
            self.datos = self.datos.loc[self.datos.iloc[:,1] >=0] 
            max_index = np.argmax(self.datos.iloc[:,1])
            self.lista_nueva = self.datos.loc[max_index:]
            

    # Se calcula y se devuelve la lista de tasa de generación.
    def generacionList(self): 
        Vref = self.lista_nueva.iloc[:, 2].values.tolist()
        Vref = np.where(np.array(Vref) < 0, 0, Vref)
        lista_generacion = []
        for vref in Vref:
            indice_generacion= functions_timelife.generacion(vref)
            lista_generacion.append(indice_generacion)
        return lista_generacion
    
    # Se calcula y se devuelve la lista de valores de fotoconductividad.
    def fotoconductividadList(self):
        Vph = self.lista_nueva.iloc[:, 1].values.tolist()
        lista_fotoconductividad = []
        for vph in Vph:
            indice_fotoconductividad = functions_timelife.fotoconductividad(vph)
            lista_fotoconductividad.append(indice_fotoconductividad)
        return lista_fotoconductividad
    
    # Se toma como parámetros la elección del usuario y la temperatura para tomar los valores de la
    # densidad de portadores
    def densidad_portadoresList(self, choice, temperatura):
        lista_fotoconductividad = self.fotoconductividadList()
        lista_densidadPortadores = functions_timelife.densidad_portadores(lista_fotoconductividad, 1700, choice, temperatura)
        return lista_densidadPortadores    
    def densidad_portadoresSintonList(self, choice, temperatura):
        lista_fotoconductividad = self.fotoconductividadList()
        lista_densidadPortadores = functions_timelife.densidad_portadores_sinton(lista_fotoconductividad, 1700, choice, temperatura)
        return lista_densidadPortadores
    def densidad_portadoresDorkelList(self, choice, temperatura):
        lista_fotoconductividad = self.fotoconductividadList()
        lista_densidadPortadores = functions_timelife.densidad_portadores_dorkel(lista_fotoconductividad, 1700, choice, temperatura)
        return lista_densidadPortadores
    def densidad_portadoresKlaassenList(self, choice, temperatura):
        lista_fotoconductividad = self.fotoconductividadList()
        lista_densidadPortadores = functions_timelife.densidad_portadores_klaassen(lista_fotoconductividad, 1700, choice, temperatura)
        return lista_densidadPortadores
    def densidad_portadoresSchindlerList(self, choice, temperatura):
        lista_fotoconductividad = self.fotoconductividadList()
        lista_densidadPortadores = functions_timelife.densidad_portadores_schindler(lista_fotoconductividad, 1700, choice, temperatura)
        return lista_densidadPortadores

    # Se toma como parámetros la elección del usuario y la temperatura para tomar los valores del
    # tiempo de recombinación
    def tiempo_recombinacionList(self, choice, temperatura):
        lista_tiempo = self.lista_nueva.iloc[:, 0].values.tolist()
        lista_densidadPortadores = self.densidad_portadoresList(choice, temperatura)
        lista_generacion = self.generacionList()
        lista_tiempo_recombinacion = functions_timelife.tiempo_recombinacion(lista_densidadPortadores, lista_generacion, lista_tiempo)
        return lista_tiempo_recombinacion
    def tiempo_recombinacionSintonList(self, choice, temperatura):
        lista_tiempo = self.lista_nueva.iloc[:, 0].values.tolist()
        lista_densidadPortadores = self.densidad_portadoresSintonList(choice, temperatura)
        lista_generacion = self.generacionList()
        lista_tiempo_recombinacion = functions_timelife.tiempo_recombinacion(lista_densidadPortadores, lista_generacion, lista_tiempo)
        return lista_tiempo_recombinacion
    def tiempo_recombinacionDorkelList(self, choice, temperatura):
        lista_tiempo = self.lista_nueva.iloc[:, 0].values.tolist()
        lista_densidadPortadores = self.densidad_portadoresDorkelList(choice, temperatura)
        lista_generacion = self.generacionList()
        lista_tiempo_recombinacion = functions_timelife.tiempo_recombinacion(lista_densidadPortadores, lista_generacion, lista_tiempo)
        return lista_tiempo_recombinacion
    def tiempo_recombinacionKlaassenList(self, choice, temperatura):
        lista_tiempo = self.lista_nueva.iloc[:, 0].values.tolist()
        lista_densidadPortadores = self.densidad_portadoresKlaassenList(choice, temperatura)
        lista_generacion = self.generacionList()
        lista_tiempo_recombinacion = functions_timelife.tiempo_recombinacion(lista_densidadPortadores, lista_generacion, lista_tiempo)
        return lista_tiempo_recombinacion
    def tiempo_recombinacionSchindlerList(self, choice, temperatura):
        lista_tiempo = self.lista_nueva.iloc[:, 0].values.tolist()
        lista_densidadPortadores = self.densidad_portadoresSchindlerList(choice, temperatura)
        lista_generacion = self.generacionList()
        lista_tiempo_recombinacion = functions_timelife.tiempo_recombinacion(lista_densidadPortadores, lista_generacion, lista_tiempo)
        return lista_tiempo_recombinacion
        
    def tiempo_intrinsecoList(self, choice, temperatura):
        lista_densidadPortadores = self.densidad_portadoresList(choice, temperatura)
        lista_densidadPortadores_filtrada = [num for num in lista_densidadPortadores if num >=0]
        lista_tiempo_intrinseco = functions_timelife.tiempo_intrinseco(lista_densidadPortadores_filtrada, temperatura)
        return lista_tiempo_intrinseco
    
    def tiempo_srhList(self, choice, temperatura):
        lista_tiempo_recombinacion = self.tiempo_recombinacionList(choice, temperatura)
        lista_tiempo_intrinseco = self.tiempo_intrinsecoList(choice, temperatura)
        lista_tiemposrh = functions_timelife.tiempo_srh(lista_tiempo_intrinseco,lista_tiempo_recombinacion)
        return lista_tiemposrh
    # Se muestra en una gráfica el tiempo de recombinación respecto a la densidad de portadores
    # en cada instante de tiempo
    def pintar_tiempo_recombinacion(self, choice, temperatura):
        lista_densidadPortadores = self.densidad_portadoresList(choice, temperatura)
        lista_tiempo_recombinacion = self.tiempo_recombinacionList(choice, temperatura)
        lista_tiempo_recombinacion_micros = [t * 1e+6 for t in lista_tiempo_recombinacion]  # Conversión a microsegundos
        # Se crea la figura y los ejes con un tamaño determinado    
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot()
        # Configurar los límites del deslizador
        slider_ax = plt.axes([0.15, 0.0001, 0.7, 0.03])  # Modificar las coordenadas y del deslizador
        slider = Slider(slider_ax, 'Rango de valores', 1, len(lista_densidadPortadores), valinit=len(lista_densidadPortadores), valstep=1, color ="green")
        # Se define n como global para acceder al numero de elementos en las funciones posteriores
        global n
        def update_graph(val,slider):
            global n
            # Obtener el valor actual del deslizador
            n = int(val)
            # Obtener los subconjuntos de datos a mostrar
            lista_densidadPortadores_variable = lista_densidadPortadores[:n]
            lista_tiempo_recombinacion_micros_variable = lista_tiempo_recombinacion_micros[:n]
            data = pd.DataFrame({"Carrier Density (cm^-3)": lista_densidadPortadores_variable, "Lifetime (us)": lista_tiempo_recombinacion_micros_variable})
            # Guardar los datos en un archivo Excel
            data.to_excel("Lifetime_Sinton_Mode.xlsx", index=False)
            # Limpiar la figura y graficar los datos actualizados
            ax.clear()
            ax.semilogx(lista_densidadPortadores_variable, lista_tiempo_recombinacion_micros_variable, marker ='o', markersize=3, label="Lifetime", color ='green')
            ax.set_title(f"Lifetime vs. Carrier Density -{choice} Mode")
            ax.set_xlabel("Carrier Density (cm^-3)")
            ax.set_ylabel("Lifetime (us)")
            ax.set_ylim(0, None)
            ax.yaxis.set_major_formatter('{:.1f}'.format)
            ax.grid(which='both', axis='both', linestyle=':', linewidth=0.5)
            fig.canvas.draw_idle()
            plt.pause(0.0001)
        # Conectar el slider a la función de actualización del gráfico
        slider.on_changed(lambda val: update_graph(val,slider))
        # Graficar los datos iniciales
        update_graph(len(lista_densidadPortadores),slider)
        # Se muestra la gráfica
        plt.ion()
        plt.show(block=False)

    # Se muestra en una gráfica el tiempo de recombinación respecto a la densidad de portadores
    # en cada instante de tiempo. Se toma en cuenta la temperatura seleccionada
    def pintar_tiempo_recombinacion_temperatura(self,choice,temperatura):
        # Para graficar correctamente
        global n
        lista_densidadPortadores = self.densidad_portadoresList(choice, temperatura)
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot()
        ax.grid(which='both', axis='both', linestyle=':', linewidth=0.5)
        # se define una temperatura mínima de 300K y se pintan con un intervalo de 50K
        # las gráficas sucesivas
        while temperatura >= 300:
                lista_densidadPortadores = self.densidad_portadoresList(choice, temperatura)
                lista_tiempo_recombinacion = self.tiempo_recombinacionList(choice, temperatura)
                lista_tiempo_recombinacion_micros = [t * 1e+6 for t in lista_tiempo_recombinacion]  # Conversión a microsegundos
                data = pd.DataFrame({"Carrier Density (cm^-3)": lista_densidadPortadores[:n], "Lifetime (us)": lista_tiempo_recombinacion_micros[:n]})
                # Guardar los datos en un archivo Excel
                data.to_excel(f"Lifetime_{choice}_Mode_{temperatura}K.xlsx", index=False)
                ax.semilogx(lista_densidadPortadores[:n], lista_tiempo_recombinacion_micros[:n], marker ='o', markersize=3, label="Lifetime")
                ax.text(lista_densidadPortadores[0], lista_tiempo_recombinacion_micros[0], f"{temperatura} K", fontsize=8)
                ax.set_title(f"Lifetime vs. Carrier Density -{choice} Mode") 
                ax.set_xlabel("Carrier Density (cm^-3)")
                ax.set_ylabel("Lifetime (us)")
                ax.set_ylim(0, None)
                ax.yaxis.set_major_formatter('{:.1f}'.format)
                temperatura-=50
        plt.show(block=False)

    def pintar_tiempo_intrinseco(self, choice, temperatura):
        lista_densidadPortadores = self.densidad_portadoresList(choice, temperatura)
        lista_densidarPortadores_filtrada = [num for num in lista_densidadPortadores if num >=0]
        lista_tiempo_recombinacion = self.tiempo_recombinacionList(choice, temperatura)
        #lista_tiempo_recombinacion_micros = [t * 1e+6 for t in lista_tiempo_recombinacion]  # Conversión a microsegundos
        lista_tiempo_intrinseco = self.tiempo_intrinsecoList(choice,temperatura)
        #lista_tiempo_intrinseco_micros = [t * 1e+6 for t in lista_tiempo_intrinseco] 
        lista_tiempo_srh = self.tiempo_srhList(choice, temperatura)
        #lista_tiempo_srh_micros = [t * 1e+6 for t in lista_tiempo_srh] 
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot()
        # Configurar los límites del deslizador
        slider_ax1 = plt.axes([0.15, 0.0001, 0.7, 0.03])  # Modificar las coordenadas y del deslizador
        slider1 = Slider(slider_ax1, 'Cota superior',1 , len(lista_densidadPortadores), valinit=len(lista_densidadPortadores),valstep=1, color ="green")
        slider_ax2 = plt.axes([0.15, 0.95, 0.7, 0.03])  # Modificar las coordenadas y del deslizador
        slider2 = Slider(slider_ax2, 'Cota inferior',1 , len(lista_densidadPortadores), valinit=len(lista_densidadPortadores),valstep=1, color ="blue")
        global n
        global s
        def update_graph1(val,slider):
            global n
            global s
            # Obtener el valor actual del deslizador
            n = int(val)
            # Obtener los subconjuntos de datos a mostrar
            lista_densidadPortadores_variable = lista_densidadPortadores[s:n]
            lista_densidarPortadores_filtrada_variable = lista_densidarPortadores_filtrada[s:n]
            lista_tiempo_recombinacion_micros_variable = lista_tiempo_recombinacion[s:n]
            lista_tiempo_intrinseco_micros_variable = lista_tiempo_intrinseco[s:n]
            lista_tiempo_srh_micros_variable = lista_tiempo_srh[s:n]
            # Se define la curva suavizada llamando a función
            lista_tiempo_srh_suave, lista_densidarPortadores_filtrada_suave = functions_curvefit.suavizado_curva(lista_tiempo_srh_micros_variable, lista_densidarPortadores_filtrada_variable)
            #indice = functions_curvefit.ajuste_minimo_curva(lista_tiempo_srh_micros_variable,lista_tiempo_srh_suave)
            # Mediante ajuste de curvas calculamos los valores que mejor se ajustan y se almacenan en un 
            # archivo los valores finales
            SRH, J0E, lista_srh_ajustada = functions_curvefit.custom_gradient(lista_densidadPortadores_variable,lista_tiempo_srh_micros_variable)
            with open("Valores_SRH_J0E.csv", "w") as archivo:
                archivo.write(f"Valor SRH, Valor J0E\n")  # Escribir encabezados si es necesario
                archivo.write(f"{SRH}, {J0E}\n")  # Escribir los valores
            # Almacenar los datos en un dataframe
            data = pd.DataFrame({"Carrier Density (cm^-3) Intrinseco":lista_densidarPortadores_filtrada_variable, "Lifetime (us) Intrinseco":lista_tiempo_intrinseco_micros_variable,"Carrier Density (cm^-3) Ajustada":lista_densidarPortadores_filtrada_suave, "Lifetime (us) Ajustada": lista_srh_ajustada, "Carrier Density (cm^-3) Suave":lista_densidarPortadores_filtrada_suave, "Lifetime (us) Suave": lista_tiempo_srh_suave  })
            # Guardar los datos en un archivo Excel
            data.to_excel(f"Lifetime_Intrinseco.xlsx", index=False)
            #Limpiar la figura y graficar los datos actualizados
            ax.clear()
            ax.loglog(lista_densidarPortadores_filtrada_variable,J0E, color ="green")
            #ax.loglog(lista_densidarPortadores_filtrada_variable, lista_srh_ajustada1, marker ="8", markersize = 6, label ="curve-fit", color ="yellow")
            #ax.semilogx(lista_densidadPortadores_variable, lista_srh_ajustada, marker ="8", markersize = 9, label ="curve-fit", color ="purple")
            #ax.semilogx(lista_densidarPortadores_filtrada_suave,lista_tiempo_srh_suave, marker = "8", markersize = 6, label = "curva-suave", color ="black")
            #ax.loglog(lista_densidadPortadores_variable, lista_tiempo_recombinacion_micros_variable, marker ='*', markersize=6, label="Lifetime", color ="green")
            #ax.loglog(lista_densidarPortadores_filtrada_variable, lista_tiempo_intrinseco_micros_variable, marker ='_', markersize=6, label="Intrinsic Lifetime", color ="blue")
            #ax.semilogx(lista_densidarPortadores_filtrada_variable, lista_tiempo_srh_micros_variable, marker ='s', markersize=4, label="SRH Lifetime", color ="red")
            ax.set_title(f"Lifetime & Intrinsic Lifetime -{choice} Mode") 
            ax.set_xlabel("Carrier Density (cm^-3)")
            ax.set_ylabel("J0 Acm^-2")
            ax.grid(which='both', axis='both', linestyle=':', linewidth=0.5)
            ax.legend()
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            fig.canvas.draw_idle()
            plt.pause(0.1)
        
        s = 0
        def update_graph2(val,slider):
            global n
            global s
            # Obtener el valor actual del deslizador
            s = int(val)
            # Obtener los subconjuntos de datos a mostrar
            lista_densidadPortadores_variable = lista_densidadPortadores[s:n]
            lista_densidarPortadores_filtrada_variable = lista_densidarPortadores_filtrada[s:n]
            lista_tiempo_recombinacion_micros_variable = lista_tiempo_recombinacion[s:n]
            lista_tiempo_intrinseco_micros_variable = lista_tiempo_intrinseco[s:n]
            lista_tiempo_srh_micros_variable = lista_tiempo_srh[s:n]
            # Se define la curva suavizada llamando a función
            lista_tiempo_srh_suave, lista_densidarPortadores_filtrada_suave = functions_curvefit.suavizado_curva(lista_tiempo_srh_micros_variable, lista_densidarPortadores_filtrada_variable)
            #indice = functions_curvefit.ajuste_minimo_curva(lista_tiempo_srh_micros_variable,lista_tiempo_srh_suave)
            # Mediante ajuste de curvas calculamos los valores que mejor se ajustan y se almacenan en un 
            # archivo los valores finales
            SRH, J0E, lista_srh_ajustada = functions_curvefit.custom_gradient(lista_densidadPortadores_variable,lista_tiempo_srh_micros_variable)
            with open("Valores_SRH_J0E.csv", "w") as archivo:
                archivo.write(f"Valor SRH, Valor J0E\n")  # Escribir encabezados si es necesario
                archivo.write(f"{SRH}, {J0E}\n")  # Escribir los valores
            # # Almacenar los datos en un dataframe
            data = pd.DataFrame({"Carrier Density (cm^-3) Intrinseco":lista_densidarPortadores_filtrada_variable, "Lifetime (us) Intrinseco":lista_tiempo_intrinseco_micros_variable,"Carrier Density (cm^-3) Ajustada":lista_densidarPortadores_filtrada_suave, "Lifetime (us) Ajustada": lista_srh_ajustada, "Carrier Density (cm^-3) Suave":lista_densidarPortadores_filtrada_suave, "Lifetime (us) Suave": lista_tiempo_srh_suave  })
            # Guardar los datos en un archivo Excel
            data.to_excel(f"Lifetime_Intrinseco.xlsx", index=False)
            #Limpiar la figura y graficar los datos actualizados
            ax.clear()
            ax.loglog(lista_densidarPortadores_filtrada_variable,J0E, color ="green")
            #ax.loglog(lista_densidarPortadores_filtrada_variable, lista_srh_ajustada1, marker ="8", markersize = 6, label ="curve-fit", color ="yellow")
            #ax.semilogx(lista_densidadPortadores_variable, lista_srh_ajustada, marker ="8", markersize = 9, label ="curve-fit", color ="purple")
            #ax.semilogx(lista_densidarPortadores_filtrada_suave,lista_tiempo_srh_suave, marker = "8", markersize = 6, label = "curva-suave", color ="black")
            #ax.loglog(lista_densidadPortadores_variable, lista_tiempo_recombinacion_micros_variable, marker ='*', markersize=6, label="Lifetime", color ="green")
            #ax.loglog(lista_densidarPortadores_filtrada_variable, lista_tiempo_intrinseco_micros_variable, marker ='_', markersize=6, label="Intrinsic Lifetime", color ="blue")
            #ax.semilogx(lista_densidarPortadores_filtrada_variable, lista_tiempo_srh_micros_variable, marker ='s', markersize=4, label="SRH Lifetime", color ="red")
            ax.set_title(f"Lifetime & Intrinsic Lifetime -{choice} Mode") 
            ax.set_xlabel("Carrier Density (cm^-3)")
            ax.set_ylabel("J0 Acm^-2")
            ax.grid(which='both', axis='both', linestyle=':', linewidth=0.5)
            ax.legend()
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            fig.canvas.draw_idle()
            plt.pause(0.1)
        # Conectar el slider a la función de actualización del gráfico
        slider1.on_changed(lambda val: update_graph1(val,slider1))
        # Conectar el slider a la función de actualización del gráfico
        slider2.on_changed(lambda val: update_graph2(val,slider1))
        # Graficar los datos iniciales
        update_graph1(len(lista_densidadPortadores),slider1)
        # Se muestra la gráfica
        plt.ion()
        plt.show(block=False)
    
    def pintar_todas_movilidades(self, choice, temperatura):
        lista_densidadPortadoresSinton = self.densidad_portadoresSintonList(choice, temperatura)
        lista_tiempo_recombinacionSinton = self.tiempo_recombinacionSintonList(choice, temperatura)
        lista_densidadPortadoresDorkel = self.densidad_portadoresDorkelList(choice, temperatura)
        lista_tiempo_recombinacionDorkel = self.tiempo_recombinacionDorkelList(choice, temperatura)
        lista_densidadPortadoresKlaassen = self.densidad_portadoresKlaassenList(choice, temperatura)
        lista_tiempo_recombinacionKlaassen = self.tiempo_recombinacionKlaassenList(choice, temperatura)
        lista_densidadPortadoresSchindler = self.densidad_portadoresSchindlerList(choice, temperatura)
        lista_tiempo_recombinacionSchindler = self.tiempo_recombinacionSchindlerList(choice, temperatura)
        lista_tiempo_recombinacionSinton_micros = [t * 1e+6 for t in lista_tiempo_recombinacionSinton]  # Conversión a microsegundos
        lista_tiempo_recombinacionDorkel_micros = [t * 1e+6 for t in lista_tiempo_recombinacionDorkel]  # Conversión a microsegundos
        lista_tiempo_recombinacionKlaassen_micros = [t * 1e+6 for t in lista_tiempo_recombinacionKlaassen]  # Conversión a microsegundos
        lista_tiempo_recombinacionSchindler_micros = [t * 1e+6 for t in lista_tiempo_recombinacionSchindler]  # Conversión a microsegundos
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot()
        slider_ax = plt.axes([0.15, 0.0001, 0.7, 0.03])  # Modificar las coordenadas y del deslizador
        slider = Slider(slider_ax, 'Rango de valores', 1, len(lista_densidadPortadoresSinton), valinit=len(lista_densidadPortadoresSinton), valstep=1, color ="green")
        def update_graph(val,slider):
            # Obtener el valor actual del deslizador
            n = int(val)
            # Obtener los subconjuntos de datos a mostrar
            lista_densidadPortadoresSinton_variable = lista_densidadPortadoresSinton[:n]
            lista_tiempo_recombinacionSinton_micros_variabe = lista_tiempo_recombinacionSinton_micros[:n]
            lista_densidadPortadoresDorkel_variable = lista_densidadPortadoresDorkel[:n]
            lista_tiempo_recombinacionDorkel_micros_variabe = lista_tiempo_recombinacionDorkel_micros[:n]
            lista_densidadPortadoresKlaassen_variable = lista_densidadPortadoresKlaassen[:n]
            lista_tiempo_recombinacionKlaassen_micros_variabe = lista_tiempo_recombinacionKlaassen_micros[:n]
            lista_densidadPortadoresSchindler_variable = lista_densidadPortadoresSchindler[:n]
            lista_tiempo_recombinacionSchindler_micros_variabe = lista_tiempo_recombinacionSchindler_micros[:n]
            data = pd.DataFrame({"Carrier Density (cm^-3) Sinton": lista_densidadPortadoresSinton_variable, "Lifetime (us) Sinton": lista_tiempo_recombinacionSinton_micros_variabe, "Carrier Density (cm^-3) Dorkel": lista_densidadPortadoresDorkel_variable,"Lifetime (us) Dorkel" :lista_tiempo_recombinacionDorkel_micros_variabe, "Carrier Density (cm^-3) Klaassen" :lista_densidadPortadoresKlaassen_variable, "Lifetime (us) Klaassen": lista_tiempo_recombinacionKlaassen_micros_variabe, "Carrier Density (cm^-3) Schindler" : lista_densidadPortadoresSchindler_variable, "Lifetime (us) Schindler": lista_tiempo_recombinacionSchindler_micros_variabe  })
            # Guardar los datos en un archivo Excel
            data.to_excel("Lifetime_All_Modes.xlsx", index=False)
            # Limpiar la figura y graficar los datos actualizados
            ax.clear()
            ax.semilogx(lista_densidadPortadoresSinton_variable, lista_tiempo_recombinacionSinton_micros_variabe, marker ='o', markersize=3, label="Sinton")
            ax.semilogx(lista_densidadPortadoresDorkel_variable, lista_tiempo_recombinacionDorkel_micros_variabe, marker ='o', markersize=3, label="Dorkel")
            ax.semilogx(lista_densidadPortadoresKlaassen_variable, lista_tiempo_recombinacionKlaassen_micros_variabe, marker ='o', markersize=3, label="Klaassen")
            ax.semilogx(lista_densidadPortadoresSchindler_variable, lista_tiempo_recombinacionSchindler_micros_variabe, marker ='o', markersize=3, label="Schindler")
            ax.set_title("Lifetime vs. Carrier Density All Modes") 
            ax.grid(which='both', axis='both', linestyle=':', linewidth=0.5)
            ax.set_xlabel("Carrier Density (cm^-3)")
            ax.set_ylabel("Lifetime (us)")
            ax.set_ylim(0, None)
            ax.legend()
            fig.canvas.draw_idle()
            plt.pause(0.0001)
        # Conectar el slider a la función de actualización del gráfico
        slider.on_changed(lambda val: update_graph(val,slider))
        update_graph(len(lista_densidadPortadoresSinton),slider)
        plt.ion()
        plt.show(block = False)




    
        

