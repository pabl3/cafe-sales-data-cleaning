import pandas as pd
import argparse
from pathlib import Path

def clean_data(input_file, output_file, md_out):
    # Cargar dataset
    df = pd.read_csv(input_file)

    # Eliminar duplicados
    initial_rows = df.shape[0]
    df = df.drop_duplicates()
    removed_duplicates = initial_rows - df.shape[0]

    # Normalizar valores de texto
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.replace("UNKNOWN", pd.NA, regex=False)
    df = df.replace("unknown", pd.NA, regex=False)

    # Conversión de tipos de datos
    # Fechas
    if "Transaction Date" in df.columns:
        df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], errors="coerce")

    # Numéricos
    for col in ["Quantity", "Price Per Unit", "Total Spent"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", ".", regex=False)
                .str.replace(r"[^\d\.]", "", regex=True)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # tratamiento de outliers
    outlier_summary = {}
    for col in ["Quantity", "Price Per Unit", "Total Spent"]:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            # Contar outliers
            mask_outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
            outlier_count = mask_outliers.sum()

            # Guardar resumen
            outlier_summary[col] = {
                "Q1": Q1,
                "Q3": Q3,
                "IQR": IQR,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "outliers_detected": int(outlier_count)
            }

            # Reemplazar outliers por NaN
            df.loc[mask_outliers, col] = pd.NA

    # Manejo de valores nulos
    for col in ["Quantity", "Price Per Unit", "Total Spent"]:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].fillna("Unknown")

    # Guardar dataset limpio
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)

    # Guardar reporte MD
    md_lines = []
    md_lines.append(f"# Cleaning Report – {Path(input_file).name}\n")
    md_lines.append(f"- Initial rows: {initial_rows}")
    md_lines.append(f"- Rows after removing duplicates: {df.shape[0]} (removed {removed_duplicates})\n")

    md_lines.append("## Nulls after cleaning\n")
    for col, val in df.isna().sum().to_dict().items():
        md_lines.append(f"- {col}: {val}")
    md_lines.append("")

    md_lines.append("## Outliers detected (IQR method)\n")
    for col, stats in outlier_summary.items():
        md_lines.append(f"- {col}: {stats['outliers_detected']} outliers replaced with median")
        md_lines.append(f"  Bounds: [{stats['lower_bound']:.2f}, {stats['upper_bound']:.2f}]")
    md_lines.append("")

    Path(md_out).write_text("\n".join(md_lines))

    print(f"Dataset cleaned and saved to: {output_file}")
    print(f"Cleaning report saved to: {md_out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleaning Cafe Sales dataset")
    parser.add_argument("--input", required=True, help="Path to raw CSV file")
    parser.add_argument("--output", required=True, help="Path to save cleaned CSV file")
    parser.add_argument("--md-out", required=True, help="Path to save cleaning report (Markdown)")
    args = parser.parse_args()

    clean_data(args.input, args.output, args.md_out)