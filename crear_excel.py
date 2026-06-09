import pandas as pd

# Matriz con todos los datos exactos de tu Tabla Maestra
datos_retenciones = [
    # BARRANQUILLA
    ["Barranquilla", "ICA Barranquilla Ventas 8 x mil", 0.008],
    ["Barranquilla", "ICA Barranquilla Ventas 12.5 x mil", 0.0125],
    ["Barranquilla", "ICA Barranquilla Ventas 12.5 x mil Sin Base", 0.0125],
    ["Barranquilla", "ICA Barranquilla Servicios 11.6 x mil", 0.0116],
    ["Barranquilla", "ICA Barranquilla Compras 4.5 x mil", 0.0045],
    
    # BOGOTÁ
    ["Bogota", "ICA Bogotá Ventas 11.04 x mil", 0.01104],
    ["Bogota", "ICA Bogotá Ventas Sin Base 11.04 x mil", 0.01104],
    ["Bogota", "ICA Bogotá Servicios 9.66 x mil", 0.00966],
    
    # MEDELLÍN
    ["Medellin", "ICA Medellín Ventas 2 x mil", 0.002],
    ["Medellin", "ICA Medellín Servicios 2 x mil", 0.002],
    ["Medellin", "ICA Medellín Compras 2 x mil", 0.002],
    
    # BUCARAMANGA
    ["Bucaramanga", "ICA Bucaramanga Ventas 4.8 x mil", 0.0048],
    ["Bucaramanga", "ICA Bucaramanga Servicios 2.2 x mil", 0.0022],
    ["Bucaramanga", "ICA Bucaramanga Compras 4.8 x mil", 0.0048],
    ["Bucaramanga", "ICA Bucaramanga Sobretasa Bomberil 10%", 0.10],
    ["Bucaramanga", "ICA Bucaramanga Avisos y Tableros 15%", 0.15],
    
    # SANTA MARTA
    ["Santa Marta", "ICA Santa Marta Ventas 7 x mil", 0.007],
    ["Santa Marta", "ICA Santa Marta Servicios 7 x mil", 0.007],
    
    # VALLE DEL CAUCA - CALI
    ["Cali", "ICA Cali Ventas 7.7 x mil", 0.0077],
    ["Cali", "ICA Cali Ventas 10 x mil", 0.01],
    ["Cali", "ICA Cali Servicios 9 x mil", 0.009],
    
    # VALLE DEL CAUCA - YUMBO
    ["Yumbo", "ICA Yumbo Ventas 7 x mil", 0.007],
    ["Yumbo", "ICA Yumbo Ventas 10 x mil", 0.01],
    ["Yumbo", "ICA Yumbo Servicios 7 x mil", 0.007],
    ["Yumbo", "ICA Yumbo Servicios 10 x mil", 0.01],
    
    # VALLE DEL CAUCA - PALMIRA
    ["Palmira", "ICA Palmira Ventas 6.9 x mil", 0.0069],
    ["Palmira", "ICA Palmira Ventas 9.6 x mil", 0.0096],
    ["Palmira", "ICA Palmira Servicios 6.9 x mil", 0.0069],
    ["Palmira", "ICA Palmira Servicios 9.6 x mil", 0.0096],
    
    # VALLE DEL CAUCA - BUGA
    ["Buga", "ICA Buga Ventas 5.1 x mil", 0.0051],
    ["Buga", "ICA Buga Servicios 5.1 x mil", 0.0051],
    
    # VALLE DEL CAUCA - TULUÁ
    ["Tulua", "ICA Tuluá Ventas 7 x mil", 0.007],
    ["Tulua", "ICA Tuluá Ventas 9 x mil", 0.009],
    ["Tulua", "ICA Tuluá Servicios 7 x mil", 0.007],
    ["Tulua", "ICA Tuluá Servicios 9 x mil", 0.009],
    
    # VALLE DEL CAUCA - CARTAGO
    ["Cartago", "ICA Cartago Ventas 7 x mil", 0.007],
    ["Cartago", "ICA Cartago Ventas 9 x mil", 0.009],
    ["Cartago", "ICA Cartago Servicios 7 x mil", 0.007],
    ["Cartago", "ICA Cartago Servicios 9 x mil", 0.009],
    
    # SABANA DE BOGOTÁ
    ["Tocancipa", "ICA Tocancipá Ventas 6 x mil", 0.006],
    ["Tocancipa", "ICA Tocancipá Servicios 6 x mil", 0.006],
    ["Sesquile", "ICA Sesquilé Ventas 5 x mil", 0.005],
    ["Sesquile", "ICA Sesquilé Ventas 5.5 x mil", 0.0055],
    ["Sesquile", "ICA Sesquilé Servicios 5 x mil", 0.005],
    ["Malambo", "ICA Malambo Ventas 7 x mil", 0.007],
    ["Malambo", "ICA Malambo Ventas 7.5 x mil", 0.0075],
    ["Malambo", "ICA Malambo Servicios 7 x mil", 0.007],
    ["Cota", "ICA Cota Ventas 6 x mil", 0.006],
    ["Cota", "ICA Cota Servicios 6 x mil", 0.006],
    ["Funza", "ICA Funza Ventas 7 x mil", 0.007],
    ["Funza", "ICA Funza Ventas 9 x mil", 0.009],
    ["Funza", "ICA Funza Servicios 7 x mil", 0.007],
    ["Funza", "ICA Funza Servicios 9 x mil", 0.009],
    ["Mosquera", "ICA Mosquera Ventas 7 x mil", 0.007],
    ["Mosquera", "ICA Mosquera Ventas 9 x mil", 0.009],
    ["Mosquera", "ICA Mosquera Servicios 7 x mil", 0.007],
    ["Mosquera", "ICA Mosquera Servicios 9 x mil", 0.009],
    ["Zipaquira", "ICA Zipaquirá Ventas 7 x mil", 0.007],
    ["Zipaquira", "ICA Zipaquirá Ventas 10 x mil", 0.01],
    ["Zipaquira", "ICA Zipaquirá Servicios 7 x mil", 0.007],
    ["Zipaquira", "ICA Zipaquirá Servicios 10 x mil", 0.01],
    ["Chia", "ICA Chía Ventas 7 x mil", 0.007],
    ["Chia", "ICA Chía Ventas 10 x mil", 0.01],
    ["Chia", "ICA Chía Servicios 7 x mil", 0.007],
    ["Chia", "ICA Chía Servicios 10 x mil", 0.01],
    ["Cajica", "ICA Cajicá Ventas 6 x mil", 0.006],
    ["Cajica", "ICA Cajicá Ventas 8 x mil", 0.008],
    ["Cajica", "ICA Cajicá Servicios 6 x mil", 0.006],
    ["Cajica", "ICA Cajicá Servicios 8 x mil", 0.008],
    
    # CESAR
    ["La Jagua de Ibirico", "ICA La Jagua de Ibirico Ventas 10 x mil", 0.01],
    ["Agustin Codazzi", "ICA Agustín Codazzi Ventas 10 x mil", 0.01],
    
    # RETEFUENTE
    ["Retefuente Nacional", "Retefuente Servicios 1%", 0.01],
    ["Retefuente Nacional", "Retefuente Servicios 2%", 0.02],
    ["Retefuente Nacional", "Retefuente Servicios 3.5%", 0.035],
    ["Retefuente Nacional", "Retefuente Servicios 4%", 0.04],
    ["Retefuente Nacional", "Retefuente Servicios 6%", 0.06],
    ["Retefuente Nacional", "Retefuente Ventas 2.5%", 0.025]
]

# Estructurar en un DataFrame de Pandas
columnas = ["Ciudad", "Concepto", "Tarifa"]
df = pd.DataFrame(datos_retenciones, columns=columnas)

# Exportar de forma automática a Excel en la misma carpeta
df.to_excel("retenciones_colombia.xlsx", index=False)
print("¡Éxito! El archivo 'retenciones_colombia.xlsx' ha sido creado en tu carpeta.")