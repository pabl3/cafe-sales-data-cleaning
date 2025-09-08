import pandas as pd
import json
import argparse
from pathlib import Path


def generate_reports(input_file, md_out, json_out):
    # === 1. Cargar dataset ===
    df = pd.read_csv(input_file)

    # === 2. Información básica ===
    n_rows, n_cols = df.shape
    basic_info = {
        "rows": n_rows,
        "columns": n_cols,
        "column_names": df.columns.tolist()
    }

    # === 3. Valores nulos ===
    missing = df.isna().sum().to_dict()

    # === 4. Duplicados ===
    duplicates = int(df.duplicated().sum())

    # === 5. Tipos de datos detectados ===
    dtypes = df.dtypes.astype(str).to_dict()

    # === 6. Valores únicos (para ver cardinalidad) ===
    unique_counts = df.nunique().to_dict()

    # === 7. Posibles problemas de contenido ===
    issues = {}
    for col in df.columns:
        # Ejemplo: valores no numéricos en columnas que parecen numéricas
        if col in ["Quantity", "Price Per Unit", "Total Spent"]:
            non_numeric = df[~df[col].astype(str).str.replace(".", "", 1).str.isnumeric()][col].unique()
            issues[col] = {"non_numeric_values": non_numeric.tolist()}

        # Ejemplo: valores desconocidos
        if df[col].astype(str).str.upper().str.contains("UNKNOWN").any():
            issues[col] = issues.get(col, {})
            issues[col]["contains_UNKNOWN"] = True

    # === 8. Guardar reporte en JSON ===
    report = {
        "basic_info": basic_info,
        "missing_values": missing,
        "duplicates": duplicates,
        "dtypes": dtypes,
        "unique_counts": unique_counts,
        "issues_found": issues
    }

    Path(json_out).write_text(json.dumps(report, indent=4))

    # === 9. Guardar reporte en Markdown ===
    md_lines = []
    md_lines.append(f"# Exploration Report – {Path(input_file).name}\n")
    md_lines.append("## Dataset Overview")
    md_lines.append(f"- Rows: {n_rows}")
    md_lines.append(f"- Columns: {n_cols}\n")

    md_lines.append("## Missing Values")
    for k, v in missing.items():
        md_lines.append(f"- {k}: {v}")
    md_lines.append("")

    md_lines.append(f"## Duplicates\n- Total duplicates: {duplicates}\n")

    md_lines.append("## Data Types")
    for k, v in dtypes.items():
        md_lines.append(f"- {k}: {v}")
    md_lines.append("")

    md_lines.append("## Unique Values (Cardinality)")
    for k, v in unique_counts.items():
        md_lines.append(f"- {k}: {v}")
    md_lines.append("")

    md_lines.append("## Issues Found")
    for col, info in issues.items():
        md_lines.append(f"- {col}: {info}")
    md_lines.append("")

    Path(md_out).write_text("\n".join(md_lines))

    print(f"✅ Reports generated:\n- {md_out}\n- {json_out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exploration of Cafe Sales dataset")
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--md-out", required=True, help="Path to Markdown output file")
    parser.add_argument("--json-out", required=True, help="Path to JSON output file")
    args = parser.parse_args()

    generate_reports(args.input, args.md_out, args.json_out)
