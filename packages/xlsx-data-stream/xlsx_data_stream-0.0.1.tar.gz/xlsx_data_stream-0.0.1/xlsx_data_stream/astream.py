import io
import zipfile
from collections.abc import AsyncIterable
from copy import deepcopy
from datetime import timezone
from typing import Optional, cast
from xml.etree import ElementTree as ETree

import asynczipstream

from .common import (
    ColumnsDescription,
    DocumentsStreamAsync,
    ModifyWorkbookCallable,
    ModifyWorksheetCallable,
    fill_data_row,
    generate_template,
)


async def _generate_xlsx_sheet_async(
    columns: ColumnsDescription,
    display_timezone: timezone,
    documents: DocumentsStreamAsync,
    template_worksheet_content: str,
) -> AsyncIterable[bytes]:
    data_prefix = template_worksheet_content.split("<sheetData>")[0] + "<sheetData>"
    yield data_prefix.encode("utf-8")

    data = template_worksheet_content.split("<sheetData>")[1].split("</sheetData>")[0]
    data_postfix = "</sheetData>" + template_worksheet_content.split("</sheetData>")[1]

    data_root = ETree.fromstring(f"<sheetData>{data}</sheetData>")

    header_row = data_root[0]
    yield ETree.tostring(header_row)

    template_row = data_root[1]

    row_number = 2

    async for document in documents:
        data_row = deepcopy(template_row)

        data_row.attrib["r"] = str(row_number)

        fill_data_row(
            data_row,
            columns,
            display_timezone,
            document,
            row_number,
        )

        yield ETree.tostring(data_row)

        row_number += 1

    yield data_postfix.encode("utf-8")


def _generate_xlsx_zip_async(
    columns: ColumnsDescription,
    display_timezone: timezone,
    documents: DocumentsStreamAsync,
    template_zfzf: zipfile.ZipFile,
    output_zszf: asynczipstream.ZipFile,
    active_worksheet_filename: str,
):
    for filename in template_zfzf.namelist():
        if filename == active_worksheet_filename:
            continue

        output_zszf.writestr(
            arcname=filename,
            data=template_zfzf.read(filename),
            compress_type=asynczipstream.ZIP_DEFLATED,
        )

    template_worksheet_content_bytes = template_zfzf.read(active_worksheet_filename)
    template_worksheet_content = template_worksheet_content_bytes.decode("utf-8")

    output_zszf.write_iter(
        arcname=active_worksheet_filename,
        iterable=_generate_xlsx_sheet_async(
            columns,
            display_timezone,
            documents,
            template_worksheet_content,
        ),
        compress_type=asynczipstream.ZIP_DEFLATED,
    )


async def get_xlsx_file_stream_async(
    columns: ColumnsDescription,
    documents: DocumentsStreamAsync,
    *,
    freeze_panes: Optional[str] = "A2",
    display_timezone: timezone = timezone.utc,
    modify_template_worksheet: Optional[ModifyWorksheetCallable] = None,
    modify_template_workbook: Optional[ModifyWorkbookCallable] = None,
) -> AsyncIterable[bytes]:
    """
    Generates an asynchronous stream of bytes representing an Excel file with data read
    from the `documents` iterable.

    :param columns: a list of ColumnDescription objects
    :param documents: an asynchronous iterable of dictionaries representing the data to
        be inserted
    :param freeze_panes: the value for the freeze_panes attribute of the worksheet
    :param display_timezone: the timezone for which date and time values should be
        displayed
    :param modify_template_worksheet: a callable that modifies the template worksheet
        object before it is used
    :param modify_template_workbook: a callable that modifies the template workbook
        object before it is used

    :return: an asynchronous iterable of bytes representing the Excel file
    """
    template_bytes, active_worksheet_index = generate_template(
        columns,
        freeze_panes,
        modify_template_worksheet,
        modify_template_workbook,
    )

    with io.BytesIO(template_bytes) as fh, zipfile.ZipFile(fh, mode="r") as zff:
        azszf = asynczipstream.ZipFile(compression=asynczipstream.ZIP_DEFLATED)

        _generate_xlsx_zip_async(
            columns,
            display_timezone,
            documents,
            zff,
            azszf,
            f"xl/worksheets/sheet{active_worksheet_index + 1}.xml",
        )

        async for chunk in azszf:
            yield cast(bytes, chunk)
