# Document Classification Dataset

This dataset is used for training the CNN-based document classifier.

## Structure

```
datasets/doc_classification/
 ├── train/
 │   ├── invoice/
 │   ├── receipt/
 │   ├── form/
 │   └── note/
 └── val/
     ├── invoice/
     ├── receipt/
     ├── form/
     └── note/
```

## Classes

- **invoice**: Commercial invoices, bills.
- **receipt**: Payment receipts, POS slips.
- **form**: Structured forms, applications, surveys.
- **note**: Handwritten notes, memos, unstructured text.

## Usage

Place images (jpg, png) into the respective class folders.
Ensure validation set has a representative distribution.
