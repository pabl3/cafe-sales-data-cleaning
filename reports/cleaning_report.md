# Cleaning Report – dirty_cafe_sales.csv

- Initial rows: 10000
- Rows after removing duplicates: 10000 (removed 0)

## Nulls after cleaning

- Transaction ID: 0
- Item: 0
- Quantity: 0
- Price Per Unit: 0
- Total Spent: 0
- Payment Method: 0
- Location: 0
- Transaction Date: 460

## Outliers detected (IQR method)

- Quantity: 0 outliers replaced with median
  Bounds: [-1.00, 7.00]
- Price Per Unit: 0 outliers replaced with median
  Bounds: [-1.00, 7.00]
- Total Spent: 259 outliers replaced with median
  Bounds: [-8.00, 24.00]
