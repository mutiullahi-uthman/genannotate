# Dataset import format

Uploads may be CSV, XLSX, or JSON. Headers are case-insensitive; surrounding
whitespace is ignored.

Required fields:

| Field | Description |
| --- | --- |
| `record_id` | Unique within the dataset version |
| `language` | Configured project language |
| `instrument` | Instrument identifier |
| `item_id` | Question or item identifier |
| `verified_transcript` | Transcript shown to annotators |

`transcript` is also accepted as an alias for `verified_transcript`. The
optional `item_text` and `audio_link` fields are preserved when supplied.
Other columns are ignored by the current record importer.

- **CSV:** UTF-8 (with or without a BOM); the first row contains headers.
- **XLSX:** The active worksheet's first row contains headers.
- **JSON:** A UTF-8 array of objects, with field names matching the headers.

Rows with missing required values or duplicate `record_id` values are rejected
with row-specific validation messages. JSON validation messages identify the
record's 1-based position in the array.
