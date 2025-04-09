# Archivo con tus funciones
import datetime
import numpy as np


# CREAR ARRAY DE FECHAS EN FORMATO DATETIME
def createTspan(fecha_inicio,fecha_final,deltaT_min):
    """ Esta funcion crea un array de timestamps que incian en f0 y terminan en fE con un avance de tiempo del detalT minutos.
    f0 y fE son fechas en formato datetime. I.e., datetime(2025, 1, 1, 0, 0, 0) 
    deltaT = Tiempo entre medidiciones, e.g., 10 minutos
    **********
    Example of use:
    The measurement is made every ten mins, starting time [2025,1,1,0,0,0] ending time [2025,1,1,1,0,0]
    fecha_inicio = datetime(2025,1,1,0,0,0)
    fecha_final = datetime(2025,1,1,1,0,0)
    deltaT = 10 (10 minutes each measurement)
    # Resultado esperado
    tspan = [datetime.datetime(2025, 1, 1, 0, 0), datetime.datetime(2025, 1, 1, 0, 10), datetime.datetime(2025, 1, 1, 0, 20), datetime.datetime(2025, 1, 1, 0, 30), datetime.datetime(2025, 1, 1, 0, 40), datetime.datetime(2025, 1, 1, 0, 50), datetime.datetime(2025, 1, 1, 1, 0)]
    ***********
    by BelloDev
    agregado 2025/04/06
    ultima revision 2025/04/07
    ***********
    """
    vector_fechas = []
    actual = fecha_inicio
    while actual <= fecha_final:
        vector_fechas.append(actual)
        actual += datetime.timedelta(minutes=deltaT_min)
    return vector_fechas

# FECHAS DE MATLAB A PYTHON en formato datetime
def datenum_to_datetime(datenum):
    """Lee un array en formato datenum de matlab (numeros de orden 7XXXXX) y los cambia al formato datetime de python.
    Por lo general los datos datenum vienen desde un archivo netCDF generado por matlab por lo que pueden venir como un Masked Array.
    Esta Funcion utiliza las librerías datetime y numpy para hacer la conversión de fechas.
    ***********
    by BelloDev
    agregado 2025/04/06
    ultima revision 2025/04/06
    ***********
    """
    # Primero convierte el maskedArray en un array normal de python
    if isinstance(datenum, np.ma.MaskedArray):
        fechas = np.array(datenum.filled(np.nan))
    else:
        fechas = np.array(datenum)

    # Lista para almacenar las fechas convertidas
    fechas_convertidas = []
    
    for idatenum in fechas.flatten():
         # Conversion de idatenum a un valor escalar
        idatenum = float(idatenum)

        # Convierte un número datenum de MATLAB a datetime de Python
        fecha = datetime.datetime.fromordinal(int(idatenum)) + datetime.timedelta(days=idatenum % 1) - datetime.timedelta(days=366)
        #fechas_convertidas.append(fecha)

        # Redondear al minuto más cercano
        fecha = fecha.replace(microsecond=0)
        if fecha.second >= 30:
            fecha += datetime.timedelta(minutes=1)
        
        fecha.replace(second=0)
        fechas_convertidas.append(fecha)

    # Retorna las fechas convertidas como un array de numpy
    return np.array(fechas_convertidas)

# FECHAS DE MATLAB A PYTHON EN FORMATO STRING
def datenum_to_datetimeStr(datenum,format="%Y/%m/%d %H:%M"):
    """Lee un array en formato datenum de matlab (numeros de orden 7XXXXX) y los cambia al formato string elegido por el usuario.
    Por defecto el formato es 'YYYY/mm/dd HH:MM'
    Por lo general los datos datenum vienen desde un archivo netCDF generado por matlab por lo que pueden venir como un Masked Array.
    Esta Funcion utiliza las librerías datetime y numpy para hacer la conversión de fechas.
    ***********
    by BelloDev
    agregado 2025/04/06
    ultima revision 2025/04/06
    ***********
    """
    tspan = datenum_to_datetime(datenum)
    tspan_str = [t.strftime(format) for idx, t in enumerate(tspan)]
    return tspan_str

# FECHAS DE PYTHON A FORMATO STRING
def datetimeStr(tspan,format="%Y/%m/%d %H:%M"):
    """Recibe un array datetime de python y lo cambia al formato string elegido por el usuario. 
    Por defecto el formato es 'YYYY/mm/dd HH:MM'
    Esta Funcion utiliza las librerías datetime hacer la conversión de fechas.
    ***********
    by BelloDev
    agregado 2025/04/06
    ultima revision 2025/04/06
    ***********
    """
    tspan_str = [t.strftime(format) for idx, t in enumerate(tspan)]
    return tspan_str