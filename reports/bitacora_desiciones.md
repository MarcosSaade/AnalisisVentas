- Agregamos al dataset ventas las regiones de acuerdo a el ID de cliente, las categorias de acuerdo al ID de producto

- Renombramos columnas para eliminar acentos

- Eliminamos outliers en ventas por categoria usando IQR

- Agregamos columna monto de venta = cantidad * precio unitario

- Eliminamos Enero por empezar en el 31

- Creamos columnas de lag, medias moviles, y rolling volatility para cantidad de ventas por region y categoria

- No rellenamos los NaNs generados por las medias moviles y lag ya que los modelos que usaremos no los requieren