import csv
import json
from dataclasses import dataclass
from io import BytesIO, StringIO
from pathlib import Path
from zipfile import BadZipFile


class ImportFileError(ValueError):
    pass


@dataclass(frozen=True)
class ParsedImportFile:
    columns: tuple[str, ...]
    rows: list[dict[str, object]]
    row_numbers: tuple[int, ...]


def parse_import_file(
    file_name: str,
    contents: bytes,
) -> ParsedImportFile:
    extension = Path(file_name).suffix.lower()

    if extension == ".csv":
        return _parse_csv(contents)
    if extension == ".json":
        return _parse_json(contents)
    if extension == ".xlsx":
        return _parse_xlsx(contents)

    raise ImportFileError(
        "Unsupported file type. Use CSV, XLSX, or JSON."
    )


class ImportFileService:
    def __init__(self, blob_storage=None):
        self.blob_storage = blob_storage

    def read_job_file(self, job, db) -> ParsedImportFile:
        from app.models.dataset_file import DatasetFile

        dataset_file = (
            db.query(DatasetFile)
            .filter(DatasetFile.id == job.dataset_file_id)
            .first()
        )
        if dataset_file is None:
            raise ImportFileError(
                "The uploaded source file was not found."
            )
        if dataset_file.dataset_id != job.dataset_id:
            raise ImportFileError(
                "The uploaded source file does not belong to this dataset."
            )
        if not dataset_file.upload_complete:
            raise ImportFileError(
                "The uploaded source file has not been completed."
            )

        if self.blob_storage is None:
            from app.services.blob_storage_service import BlobStorageService

            self.blob_storage = BlobStorageService()

        contents = self.blob_storage.download_file(
            dataset_file.object_key
        )
        return parse_import_file(
            dataset_file.file_name,
            contents,
        )


def _parse_csv(contents: bytes) -> ParsedImportFile:
    try:
        text = contents.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ImportFileError(
            "CSV files must use UTF-8 encoding."
        ) from exc

    reader = csv.DictReader(StringIO(text, newline=""))
    if not reader.fieldnames:
        raise ImportFileError(
            "CSV file must contain a header row."
        )

    columns = _normalize_columns(reader.fieldnames)
    rows = []
    row_numbers = []

    try:
        for row in reader:
            if None in row:
                raise ImportFileError(
                    f"Row {reader.line_num} has more values than the header."
                )

            rows.append(
                _normalize_row(row)
            )
            row_numbers.append(reader.line_num)
    except csv.Error as exc:
        raise ImportFileError(
            f"CSV file could not be parsed: {exc}"
        ) from exc

    return ParsedImportFile(
        columns=columns,
        rows=rows,
        row_numbers=tuple(row_numbers),
    )


def _parse_json(contents: bytes) -> ParsedImportFile:
    try:
        data = json.loads(contents.decode("utf-8-sig"))
    except UnicodeDecodeError as exc:
        raise ImportFileError(
            "JSON files must use UTF-8 encoding."
        ) from exc
    except json.JSONDecodeError as exc:
        raise ImportFileError(
            f"Invalid JSON at line {exc.lineno}, column {exc.colno}."
        ) from exc

    if not isinstance(data, list) or not all(
        isinstance(row, dict)
        for row in data
    ):
        raise ImportFileError(
            "JSON files must contain an array of record objects."
        )

    rows = [
        _normalize_row(row)
        for row in data
    ]
    columns = tuple(
        dict.fromkeys(
            column
            for row in rows
            for column in row
        )
    )

    return ParsedImportFile(
        columns=columns,
        rows=rows,
        row_numbers=tuple(
            range(1, len(rows) + 1)
        ),
    )


def _parse_xlsx(contents: bytes) -> ParsedImportFile:
    try:
        from openpyxl import load_workbook
        from openpyxl.utils.exceptions import InvalidFileException
    except ImportError as exc:
        raise ImportFileError(
            "XLSX support is unavailable; install the openpyxl dependency."
        ) from exc

    try:
        workbook = load_workbook(
            BytesIO(contents),
            read_only=True,
            data_only=True,
        )
    except (BadZipFile, InvalidFileException, OSError, ValueError) as exc:
        raise ImportFileError(
            "XLSX file could not be parsed."
        ) from exc

    try:
        worksheet = workbook.active
        rows_iterator = worksheet.iter_rows(values_only=True)
        header = next(rows_iterator, None)
        if header is None:
            raise ImportFileError(
                "XLSX file must contain a header row."
            )

        header_values = list(header)
        while header_values and _is_blank(header_values[-1]):
            header_values.pop()
        if not header_values:
            raise ImportFileError(
                "XLSX file must contain a header row."
            )

        columns = _normalize_columns(header_values)
        rows = []
        row_numbers = []

        for row_number, values in enumerate(
            rows_iterator,
            start=2,
        ):
            if all(_is_blank(value) for value in values):
                continue

            if any(
                not _is_blank(value)
                for value in values[len(columns):]
            ):
                raise ImportFileError(
                    f"Row {row_number} has more values than the header."
                )

            rows.append(
                _normalize_row(
                    dict(zip(columns, values[:len(columns)]))
                )
            )
            row_numbers.append(row_number)

        return ParsedImportFile(
            columns=columns,
            rows=rows,
            row_numbers=tuple(row_numbers),
        )
    finally:
        workbook.close()


def _normalize_columns(values) -> tuple[str, ...]:
    columns = tuple(
        _normalize_column(value)
        for value in values
    )
    if any(not column for column in columns):
        raise ImportFileError(
            "File contains a blank column name."
        )
    if len(set(columns)) != len(columns):
        raise ImportFileError(
            "File contains duplicate column names."
        )
    return columns


def _normalize_row(row: dict) -> dict[str, object]:
    normalized = {}
    for column, value in row.items():
        if column is None:
            continue

        normalized_column = _normalize_column(column)
        if not normalized_column:
            raise ImportFileError(
                "File contains a blank column name."
            )
        if normalized_column in normalized:
            raise ImportFileError(
                "File contains duplicate column names."
            )

        normalized[normalized_column] = value

    return normalized


def _normalize_column(value) -> str:
    if value is None:
        return ""
    column = str(value).strip().lower()
    if column == "verified_transcript":
        return "transcript"
    return column


def _is_blank(value) -> bool:
    return value is None or (
        isinstance(value, str)
        and not value.strip()
    )
