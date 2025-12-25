import pandas as pd
import numpy as np
from datetime import datetime
from number_parser import parse

class CafeSalesPipeline:
    def __init__(self, df):
        """
        Inicializa el pipeline con una copia del dataset original.
        """
        self.data = df.copy()
        self.formatos_fecha = [
            "%d/%m/%Y","%d/%m/%y","%m/%d/%Y","%m/%d/%y","%Y/%m/%d","%y/%m/%d",
            "%d/%b/%Y","%d/%b/%y","%b/%d/%Y","%b/%d/%y","%Y/%b/%d","%y/%b/%d",
            "%d/%B/%Y","%d/%B/%y","%B/%d/%Y","%B/%d/%y","%Y/%B/%d","%y/%B/%d"
        ]

    def _preprocesar_strings(self):
        # Limpieza de Transaction ID
        self.data['Transaction ID'] = self.data['Transaction ID'].astype(str).str.replace(r'[^A-Za-z0-9_]', '', regex=True)
        self.data['Transaction ID'] = self.data['Transaction ID'].str.upper()

        # Estandarización de nulos en columnas
        lista_strings = ["Item", "Payment Method", "Location"]
        for col in lista_strings:
            self.data[col] = self.data[col].replace([r'UNKNOWN', r'ERROR', r'NAN'], np.nan, regex=True)

    def _preprocesar_numericos(self):
        numericos = ["Quantity", "Price Per Unit", "Total Spent"]

        for col in numericos:
            # Convertir texto numérico a valor real
            try:
                self.data[col] = self.data[col].apply(lambda x: parse(str(x)) if pd.notnull(x) else x)
            except:
                pass

            # Eliminar y forzar a numérico
            self.data[col] = self.data[col].replace([r'UNKNOWN', r'ERROR'], np.nan, regex=True)
            self.data[col] = self.data[col].astype(str).str.replace(r'[^0-9.]', '', regex=True)
            self.data[col] = pd.to_numeric(self.data[col], errors='coerce')

    def _preprocesar_fechas(self):
        # Limpieza de texto en fechas
        self.data['Transaction Date'] = self.data['Transaction Date'].astype(str).str.upper()
        self.data['Transaction Date'] = self.data['Transaction Date'].replace([r'UNKNOWN', r'ERROR', r'NAN'], np.nan, regex=True)
        self.data['Transaction Date'] = self.data['Transaction Date'].str.replace(r'[^A-Za-z0-9._/\-]', "", regex=True)
        self.data['Transaction Date'] = self.data['Transaction Date'].replace(r'[^A-Za-z0-9/]', "/", regex=True)

        def intentar_parsear(x):
            if pd.isna(x) or x == 'None': return np.nan
            for fmt in self.formatos_fecha:
                try:
                    return datetime.strptime(x, fmt)
                except:
                    continue
            return np.nan

        self.data['Transaction Date'] = self.data['Transaction Date'].apply(intentar_parsear)

    def _eliminar_filas_criticas(self):
        # Eliminación según criterios de pérdida de información grave
        # 1. Sin Item, Cantidad ni Fecha
        critico_item_qty_date = self.data[["Item", "Quantity", "Transaction Date"]].isna().all(axis=1)
        self.data = self.data.drop(self.data[critico_item_qty_date].index)

        # 2. Sin Item, Cantidad ni Precio
        nan_item_qty_price = self.data[["Item", "Quantity", "Price Per Unit"]].isna().all(axis=1)
        self.data = self.data.drop(self.data[nan_item_qty_price].index)

    def _imputacion_iterativa(self, max_iter=11):
        # seguridad para Price Per Unit
        self.data["Price Per Unit"] = self.data["Price Per Unit"].fillna(
            self.data.groupby("Item")["Price Per Unit"].transform(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan)
        )

        for i in range(max_iter):
            nulos_antes = self.data.isnull().sum().sum()

            # Imputación basada en relaciones matemáticas de las categorías
            self.data['Price Per Unit'] = self.data['Price Per Unit'].fillna(self.data['Total Spent'] / self.data['Quantity'])
            self.data['Quantity'] = self.data['Quantity'].fillna(self.data["Total Spent"] / self.data["Price Per Unit"])
            self.data["Total Spent"] = self.data["Total Spent"].fillna(self.data["Quantity"] * self.data["Price Per Unit"])

            # Imputación basada en modas de grupos relacionados
            self.data['Payment Method'] = self.data['Payment Method'].fillna(
                self.data.groupby(["Quantity", "Location"])['Payment Method'].transform(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan)
            )
            self.data['Transaction Date'] = self.data["Transaction Date"].fillna(
                self.data.groupby(["Item", "Quantity"])['Transaction Date'].transform(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan)
            )
            self.data['Location'] = self.data['Location'].fillna(
                self.data.groupby(["Item", "Quantity"])['Location'].transform(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan)
            )
            self.data['Item'] = self.data['Item'].fillna(
                self.data.groupby(["Price Per Unit", "Quantity"])['Item'].transform(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan)
            )

            if self.data.isnull().sum().sum() == nulos_antes:
                break

    def _limpieza_final(self):
        # Eliminar registros que quedaron nulos en Total Spent
        self.data = self.data.dropna(subset=["Total Spent", "Item"])

        # Asegurando formato de columnas
        self.data["Quantity"] = self.data["Quantity"].astype(int)
        self.data["Price Per Unit"] = self.data["Price Per Unit"].astype(float)
        self.data["Total Spent"] = self.data["Total Spent"].astype(float)
        self.data['Item'] = self.data['Item'].astype(str)
        self.data['Payment Method'] = self.data['Payment Method'].astype(str)
        self.data['Location'] = self.data['Location'].astype(str)

    def run_pipeline(self):
        """Ejecuta todos los pasos de limpieza secuencialmente."""
        self._preprocesar_strings()
        self._preprocesar_numericos()
        self._preprocesar_fechas()
        self._eliminar_filas_criticas()
        self._imputacion_iterativa()
        self._limpieza_final()
        return self.data

  # 1. Cargar datos
raw_data = pd.read_csv('dirty_cafe_sales.csv')

# 2. Ejecutar
pipeline = CafeSalesPipeline(raw_data)
data_limpia = pipeline.run_pipeline()

# 3. Resumen de resultados
print(f"Dataset original: {raw_data.shape[0]} filas")
print(f"Dataset final: {data_limpia.shape[0]} filas")
print(f"Valores nulos totales: {data_limpia.isna().sum().sum()}")

clean_data= data_limpia.copy()
clean_data.to_csv('clean_data.csv', index=False)
