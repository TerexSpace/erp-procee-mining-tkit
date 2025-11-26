# Sample Logs

This directory is intended to hold sample ERP data exports in CSV format.
These files can be used to test the functionality of the `erp-processminer`
toolkit and to run the example scripts.

## Expected Data Format

The example scripts are designed to work with CSV files representing
different documents in a procure-to-pay (P2P) process. The expected files
and their columns are:

### `purchase_orders.csv`

A file containing purchase order header data.

| Column          | Type      | Description                               |
|-----------------|-----------|-------------------------------------------|
| `PO_NUMBER`     | string    | Unique identifier for the purchase order. |
| `CREATION_DATE` | datetime  | Timestamp when the PO was created.        |
| `VENDOR`        | string    | Identifier for the supplier.              |
| `CREATED_BY`    | string    | User who created the PO.                  |

### `goods_receipts.csv`

A file containing goods receipt information, linking back to a purchase order.

| Column         | Type      | Description                               |
|----------------|-----------|-------------------------------------------|
| `GR_NUMBER`    | string    | Unique identifier for the goods receipt.  |
| `PO_NUMBER`    | string    | The PO this receipt is for.               |
| `RECEIPT_DATE` | datetime  | Timestamp when the goods were received.   |
| `QUANTITY`     | float     | The quantity of goods received.           |
| `ITEM_NUMBER`  | integer   | The line item number from the PO.         |

### `invoices.csv`

A file containing invoice information.

| Column           | Type      | Description                               |
|------------------|-----------|-------------------------------------------|
| `INVOICE_NUMBER` | string    | Unique identifier for the invoice.        |
| `PO_NUMBER`      | string    | The PO this invoice is for.               |
| `INVOICE_DATE`   | datetime  | Timestamp when the invoice was received.  |
| `AMOUNT`         | float     | The total amount of the invoice.          |
| `STATUS`         | string    | The status of the invoice (e.g., "Paid"). |
| `CLEARING_DATE`  | datetime  | Timestamp when the invoice was paid.      |

You can create synthetic CSV files with these columns to run the examples.