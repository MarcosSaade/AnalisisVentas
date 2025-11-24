import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("../data_clean/ventas_clean.csv")

# Semana, mes, día de la semana
df["Fecha"] = pd.to_datetime(df["Fecha"])

df["semana"] = df["Fecha"].dt.isocalendar().week
df["mes"] = df["Fecha"].dt.month
df["dia_semana"] = df["Fecha"].dt.dayofweek

# Agregamos columnas de autocorrelación por categoria y region

# Lag 1 (ventas del periodo anterior)
df["ventas_categoria_lag_1"] = df.groupby(["Categoria"])["Cantidad"].shift(1)
df["ventas_region_lag_1"] = df.groupby(["Region"])["Cantidad"].shift(1)

# Rolling Mean, Std 3, 7, 14, 30 días

# 3 días
df["ventas_categoria_rolling_mean_3"] = df.groupby(["Categoria"])["Cantidad"].transform(
    lambda x: x.rolling(window=3).mean()
)
df["ventas_region_rolling_mean_3"] = df.groupby(["Region"])["Cantidad"].transform(
    lambda x: x.rolling(window=3).mean()
)

df["ventas_categoria_rolling_std_3"] = df.groupby(["Categoria"])["Cantidad"].transform(
    lambda x: x.rolling(window=3).std()
)
df["ventas_region_rolling_std_3"] = df.groupby(["Region"])["Cantidad"].transform(
    lambda x: x.rolling(window=3).std()
)

# 7 días
df["ventas_categoria_rolling_mean_7"] = df.groupby(["Categoria"])["Cantidad"].transform(
    lambda x: x.rolling(window=7).mean()
)
df["ventas_region_rolling_mean_7"] = df.groupby(["Region"])["Cantidad"].transform(
    lambda x: x.rolling(window=7).mean()
)

df["ventas_categoria_rolling_std_7"] = df.groupby(["Categoria"])["Cantidad"].transform(
    lambda x: x.rolling(window=7).std()
)
df["ventas_region_rolling_std_7"] = df.groupby(["Region"])["Cantidad"].transform(
    lambda x: x.rolling(window=7).std()
)

# 14 días
df["ventas_categoria_rolling_mean_14"] = df.groupby(["Categoria"])[
    "Cantidad"
].transform(lambda x: x.rolling(window=14).mean())
df["ventas_region_rolling_mean_14"] = df.groupby(["Region"])["Cantidad"].transform(
    lambda x: x.rolling(window=14).mean()
)

df["ventas_categoria_rolling_std_14"] = df.groupby(["Categoria"])["Cantidad"].transform(
    lambda x: x.rolling(window=14).std()
)
df["ventas_region_rolling_std_14"] = df.groupby(["Region"])["Cantidad"].transform(
    lambda x: x.rolling(window=14).std()
)

# 30 días
df["ventas_categoria_rolling_mean_30"] = df.groupby(["Categoria"])[
    "Cantidad"
].transform(lambda x: x.rolling(window=30).mean())
df["ventas_region_rolling_mean_30"] = df.groupby(["Region"])["Cantidad"].transform(
    lambda x: x.rolling(window=30).mean()
)

df["ventas_categoria_rolling_std_30"] = df.groupby(["Categoria"])["Cantidad"].transform(
    lambda x: x.rolling(window=30).std()
)
df["ventas_region_rolling_std_30"] = df.groupby(["Region"])["Cantidad"].transform(
    lambda x: x.rolling(window=30).std()
)

# Ordenamos
df = df.sort_values(by=["Categoria", "Region", "Fecha"])
# No rellenamos NaN porque planeamos usar modelos que los soporten

# Categorical encoding
df["ID_Region"] = df["Region"].astype("category").cat.codes

df.to_csv("../data_clean/data_fe.csv", index=False)
print("Feature Engineering completado")
