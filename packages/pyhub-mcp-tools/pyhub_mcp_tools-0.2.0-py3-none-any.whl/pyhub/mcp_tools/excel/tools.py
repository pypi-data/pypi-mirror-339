"""
Excel automation
"""

import json
from typing import Optional, Any

import xlwings as xw

from .types import ExcelRange
from .. import mcp


#
# macOS 보안정책에 창의 가시성을 조절하거나, 워크북 수를 세는 명령은 자동화 권한을 허용한 앱에서만 가능
# Claude 앱에서는 Excel에 대해 자동화 권한을 부여하지 않았음.
#
# Claude 앱내에서 STDIN 방식의 직접 실행 방식이기에 CLAUDE 앱의 실행권한이 영향을 받음.
# MCP Server를 별도 서버로 띄우고, SSE 방식으로 접근한다면 이를 해결할 수도 있겠음.
# 장기적으로 별도 애플리케이션으로 띄울 수 있어야, 다양한 기능 구현이 가능하겠음.
#
#  - https://github.com/xlwings/xlwings/issues/1262
#  - https://github.com/xlwings/xlwings/issues/1851
#  - https://github.com/xlwings/xlwings/issues/1966
#
# Claude 밖에서 별도 프로세스로 SSE 서버를 띄운 다음 pyhub.mcp_tools.excel run sse --port 9999
# Claude 에서는 uvx mcp-proxy http://localhost:9999/sse 명령으로 접속 가능
#


@mcp.tool()
def get_opened_workbooks() -> dict:
    """현재 열려진 엑셀 워크북 목록을 반환"""

    try:
        return {
            "books": [
                {
                    "name": book.name,
                    "fullname": book.fullname,
                    "sheets": [
                        {
                            "name": sheet.name,
                            "index": sheet.index,
                            "range": sheet.used_range.get_address(),  # "$A$1:$E$665"
                            "count": sheet.used_range.count,  # 3325 (셀의 총 개수)
                            "shape": sheet.used_range.shape,  # (655, 5)
                            "active": sheet == xw.sheets.active,
                        }
                        for sheet in book.sheets
                    ],
                    "active": book == xw.books.active,
                }
                for book in xw.books
            ]
        }
    except Exception as e:
        import traceback

        with open("/Users/allieus/Work/pyhub-mcp-tools/debug.txt", "wt") as f:
            f.write(traceback.format_exc())
        raise e


@mcp.tool()
def get_values_from_active_sheet(sheet_range: Optional[ExcelRange] = None) -> str:
    """활성화된 시트의 지정 범위의 값을 반환합니다. 범위가 생략되면 시트의 전체 데이터를 JSON 배열로 반환"""

    if sheet_range is None:
        data = xw.sheets.active.used_range.value
    else:
        data = xw.Range(sheet_range).value

    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
def get_values_from_sheet(book_name: str, sheet_name: str, sheet_range: Optional[ExcelRange] = None) -> str:
    """지정 시트의 지정 범위로부터"""

    sheet: xw.Sheet = xw.books[book_name].sheets[sheet_name]

    if sheet_range is None:
        data = sheet.used_range.value
    else:
        data = sheet.range(sheet_range).value

    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
def set_values_to_active_sheet(sheet_range: ExcelRange, values) -> None:
    """

    Ex:
        sheet_range="E1" values='[["a", "b"], ["c", "d"]]'
    """
    if sheet_range is None:
        range_ = xw.sheets.active.used_range
    else:
        range_ = xw.Range(sheet_range)

    range_.value = values


@mcp.tool()
def set_values_to_sheet(book_name: str, sheet_name: str, sheet_range: ExcelRange, values) -> None:
    sheet: xw.Sheet = xw.books[book_name].sheets[sheet_name]

    if sheet_range is None:
        range_ = sheet.used_range.value
    else:
        range_ = sheet.range(sheet_range).value

    range_.value = values