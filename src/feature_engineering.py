import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class FeatureEngineer:
    """
    A class to perform feature engineering on sales data.
    """

    def __init__(
        self,
        input_path="../data_clean/ventas_clean.csv",
        output_path="../data_clean/data_fe.csv",
    ):
        """
        Initialize the FeatureEngineer with input and output paths.

        Args:
            input_path (str): Path to the cleaned sales data
            output_path (str): Path to save the engineered features
        """
        self.input_path = input_path
        self.output_path = output_path
        self.df = None

    def load_data(self):
        """Load the data from the input path."""
        self.df = pd.read_csv(self.input_path)
        self.df["Fecha"] = pd.to_datetime(self.df["Fecha"])
        return self

    def create_temporal_features(self):
        """Create temporal features: week, month, day of week."""
        self.df["semana"] = self.df["Fecha"].dt.isocalendar().week
        self.df["mes"] = self.df["Fecha"].dt.month
        self.df["dia_semana"] = self.df["Fecha"].dt.dayofweek
        return self

    def create_lag_features(self):
        """Create lag features for time series analysis."""
        self.df["ventas_categoria_lag_1"] = self.df.groupby(["Categoria"])[
            "Cantidad"
        ].shift(1)
        self.df["ventas_region_lag_1"] = self.df.groupby(["Region"])["Cantidad"].shift(
            1
        )
        self.df["cantidad_lag_1"] = self.df.groupby(["Categoria", "Region"])[
            "Cantidad"
        ].shift(1)
        return self

    def create_rolling_features(self):
        """Create rolling mean and std features for different time windows."""
        windows = [3, 7, 14, 30]

        for window in windows:
            # Rolling means
            self.df[f"ventas_categoria_rolling_mean_{window}"] = self.df.groupby(
                ["Categoria"]
            )["Cantidad"].transform(lambda x: x.shift(1).rolling(window=window).mean())
            self.df[f"ventas_region_rolling_mean_{window}"] = self.df.groupby(
                ["Region"]
            )["Cantidad"].transform(lambda x: x.shift(1).rolling(window=window).mean())

            # Rolling stds
            self.df[f"ventas_categoria_rolling_std_{window}"] = self.df.groupby(
                ["Categoria"]
            )["Cantidad"].transform(lambda x: x.shift(1).rolling(window=window).std())
            self.df[f"ventas_region_rolling_std_{window}"] = self.df.groupby(
                ["Region"]
            )["Cantidad"].transform(lambda x: x.shift(1).rolling(window=window).std())

        # 2, 3, 4, 5, 6 week rolling means for Categoria and Region
        for w in range(2, 7):
            self.df[f"ventas_categoria_rolling_mean_{w}_weeks"] = self.df.groupby(
                ["Categoria"]
            )["Cantidad"].transform(lambda x: x.shift(1).rolling(window=w * 7).mean())
            self.df[f"ventas_region_rolling_mean_{w}_weeks"] = self.df.groupby(
                ["Region"]
            )["Cantidad"].transform(lambda x: x.shift(1).rolling(window=w * 7).mean())

        return self

    def create_interaction_features(self):
        """Create interaction features between different variables."""
        # Precio x Cantidad
        self.df["precio_x_cantidad"] = (
            self.df["Precio_Unitario"] * self.df["cantidad_lag_1"]
        )

        # Cantidad / Rolling Mean and Std by Categoria and Region
        for w in (3, 7, 14, 30):
            # means
            denom_cat_mean = self.df[f"ventas_categoria_rolling_mean_{w}"]
            denom_reg_mean = self.df[f"ventas_region_rolling_mean_{w}"]
            self.df[f"cantidad_/_ventas_categoria_rmean_{w}"] = np.where(
                (denom_cat_mean == 0) | denom_cat_mean.isna(),
                np.nan,
                self.df["cantidad_lag_1"] / denom_cat_mean,
            )
            self.df[f"cantidad_/_ventas_region_rmean_{w}"] = np.where(
                (denom_reg_mean == 0) | denom_reg_mean.isna(),
                np.nan,
                self.df["cantidad_lag_1"] / denom_reg_mean,
            )

            # stds
            denom_cat_std = self.df[f"ventas_categoria_rolling_std_{w}"]
            denom_reg_std = self.df[f"ventas_region_rolling_std_{w}"]
            self.df[f"cantidad_/_ventas_categoria_rstd_{w}"] = np.where(
                (denom_cat_std == 0) | denom_cat_std.isna(),
                np.nan,
                self.df["cantidad_lag_1"] / denom_cat_std,
            )
            self.df[f"cantidad_/_ventas_region_rstd_{w}"] = np.where(
                (denom_reg_std == 0) | denom_reg_std.isna(),
                np.nan,
                self.df["cantidad_lag_1"] / denom_reg_std,
            )

        # ventas_categoria_rolling_mean_7 / ventas_categoria_rolling_mean_14
        self.df["ventas_categoria_rmean_7_/_14"] = (
            self.df["ventas_categoria_rolling_mean_7"]
            / self.df["ventas_categoria_rolling_mean_14"]
        )

        # ventas_region_rolling_mean_7 / ventas_region_rolling_mean_14
        self.df["ventas_region_rmean_7_/_14"] = (
            self.df["ventas_region_rolling_mean_7"]
            / self.df["ventas_region_rolling_mean_14"]
        )

        # rolling_mean + rolling_std
        self.df["ventas_categoria_rmean_+_rstd_7"] = (
            self.df["ventas_categoria_rolling_mean_7"]
            + self.df["ventas_categoria_rolling_std_7"]
        )
        self.df["ventas_region_rmean_+_rstd_7"] = (
            self.df["ventas_region_rolling_mean_7"]
            + self.df["ventas_region_rolling_std_7"]
        )

        # rolling_mean * rolling_std
        self.df["ventas_categoria_rmean_*_rstd_7"] = (
            self.df["ventas_categoria_rolling_mean_7"]
            * self.df["ventas_categoria_rolling_std_7"]
        )
        self.df["ventas_region_rmean_*_rstd_7"] = (
            self.df["ventas_region_rolling_mean_7"]
            * self.df["ventas_region_rolling_std_7"]
        )

        return self

    def create_categorical_encoding(self):
        """Encode categorical variables."""
        self.df["ID_Region"] = self.df["Region"].astype("category").cat.codes
        return self

    def sort_data(self):
        """Sort the dataframe by Categoria, Region, and Fecha."""
        self.df = self.df.sort_values(by=["Categoria", "Region", "Fecha"])
        return self

    def save_data(self):
        """Save the engineered dataframe to the output path."""
        self.df.to_csv(self.output_path, index=False)
        print(f"Feature Engineering completado. Datos guardados en: {self.output_path}")
        return self

    def engineer(self):
        """
        Execute the complete feature engineering pipeline.

        Returns:
            pd.DataFrame: The engineered dataframe
        """
        print("Iniciando Feature Engineering...")
        (
            self.load_data()
            .sort_data()
            .create_temporal_features()
            .create_lag_features()
            .create_rolling_features()
            .create_interaction_features()
            .create_categorical_encoding()
            .save_data()
        )

        print(f"Features creadas: {self.df.shape[1]} columnas")
        return self.df


if __name__ == "__main__":
    # Create the feature engineer and execute the pipeline
    fe = FeatureEngineer()
    df_engineered = fe.engineer()
