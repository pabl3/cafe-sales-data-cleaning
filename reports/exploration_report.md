# Exploration Report � dirty_cafe_sales.csv

## Dataset Overview
- Rows: 10000
- Columns: 8

## Missing Values
- Transaction ID: 0
- Item: 333
- Quantity: 138
- Price Per Unit: 179
- Total Spent: 173
- Payment Method: 2579
- Location: 3265
- Transaction Date: 159

## Duplicates
- Total duplicates: 0

## Data Types
- Transaction ID: object
- Item: object
- Quantity: object
- Price Per Unit: object
- Total Spent: object
- Payment Method: object
- Location: object
- Transaction Date: object

## Unique Values (Cardinality)
- Transaction ID: 10000
- Item: 10
- Quantity: 7
- Price Per Unit: 8
- Total Spent: 19
- Payment Method: 5
- Location: 4
- Transaction Date: 367

## Issues Found
- Item: {'contains_UNKNOWN': True}
- Quantity: {'non_numeric_values': ['ERROR', 'UNKNOWN', nan], 'contains_UNKNOWN': True}
- Price Per Unit: {'non_numeric_values': [nan, 'ERROR', 'UNKNOWN'], 'contains_UNKNOWN': True}
- Total Spent: {'non_numeric_values': ['ERROR', nan, 'UNKNOWN'], 'contains_UNKNOWN': True}
- Payment Method: {'contains_UNKNOWN': True}
- Location: {'contains_UNKNOWN': True}
- Transaction Date: {'contains_UNKNOWN': True}
