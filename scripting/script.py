import pandas as pd

# Leer fichero de participantes
data = pd.read_excel("flisol.xlsx")

print("FLISoL 2025 Registration")

# Obtener alumnos UTEC
UTECs = data[
    data["Código Alumno / DNI"].apply(lambda s: len(str(s)) == 9) |
    data["Nombre de Instituto educativo"].str.contains("utec", case=False, na=False)
]

# Obtener participantes externos (para solicitud de externos)
invites = data[
    data["Código Alumno / DNI"].apply(lambda s: len(str(s)) == 8) &
    (~data["Correo electrónico"].str.contains("utec.edu.pe", na=False)) &
    (~data["Nombre de Instituto educativo"].str.contains("utec", case=False, na=False)) # Por suerte, nadie inscrito con DNI ha puesto UTEC completo
]
# FIXME: Claramente existen más casos, pero qué flojera colocar cada uno

# Obtener registros inválidos (Verifica si la longitud es de un DNI)
# FIXME: verificar si es numerico y aplicar más filtros
erroneous = data[
    data["Código Alumno / DNI"].apply(lambda s: len(str(s)) < 7 or len(str(s)) > 9)
]

print(UTECs)
print(invites)
print(erroneous)

# Not working at all, data can be duplicated on those dataframes (negative diference)
# print("Ignored entries: ", data.size - (erroneous.size + UTECs.size + invites.size))

if len(erroneous) > 0:
    print(f"Saved bad inscriptions to erroneous.xlsx ({erroneous.size} entries)")
    erroneous.to_excel("erroneous.xlsx")
if len(UTECs) > 0:
    print(f"Saved UTEC participants to UTECs.xlsx ({UTECs.size} entries)")
    UTECs.to_excel("UTECs.xlsx")
if len(invites) > 0:
    print(f"Saved non-UTEC participants to invites.xlsx ({invites.size} entries)")
    invites.to_excel("invites.xlsx")
