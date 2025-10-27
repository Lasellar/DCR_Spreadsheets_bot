from aiogoogle import Aiogoogle

from settings import COLORS
from .generate_cell import generate_cell

from time import sleep


async def copy_guestlist_sheet_from_template(
        target_spreadsheet_id: str,
        source_spreadsheet_url: str,
        wrapper_services: Aiogoogle,
) -> int:
    """Копирует лист 'СПИСКИ' из шаблона и возвращает ID скопированного листа"""
    service = await wrapper_services.discover('sheets', 'v4')
    source_spreadsheet_id = source_spreadsheet_url.split('/d/')[1].split('/')[0]
    source_spreadsheet = await wrapper_services.as_service_account(
        service.spreadsheets.get(spreadsheetId=source_spreadsheet_id)
    )
    source_sheet_id = None
    for sheet in source_spreadsheet.get('sheets'):
        if sheet['properties']['title'] == 'СПИСКИ':
            source_sheet_id = sheet['properties']['sheetId']
            break
    if not source_sheet_id:
        raise Exception("Лист 'СПИСКИ' не найден в исходном документе")
    copy_response = await wrapper_services.as_service_account(
        service.spreadsheets.sheets.copyTo(
            spreadsheetId=source_spreadsheet_id,
            sheetId=source_sheet_id,
            json={'destinationSpreadsheetId': target_spreadsheet_id}
        )
    )
    return copy_response['sheetId']


async def update_second_sheet(
    spreadsheetid: str, wrapper_services: Aiogoogle,
    template_url: str
) -> None:
    copied_sheet_id = await copy_guestlist_sheet_from_template(
        spreadsheetid, template_url, wrapper_services
    )
    service = await wrapper_services.discover('sheets', 'v4')
    sleep(1)
    requests = [{'updateSheetProperties': {
        'properties': {
            'sheetId': copied_sheet_id, 'title': 'СПИСКИ'
        }, 'fields': 'title'}}]
    await wrapper_services.as_service_account(
        service.spreadsheets.batchUpdate(
            spreadsheetId=spreadsheetid,
            json={'requests': requests}
        )
    )
    # Используем ID скопированного листа для дальнейших операций
    sheet_id = copied_sheet_id
    service = await wrapper_services.discover('sheets', 'v4')
    requests = list()

    # Добавление постоянного списка
    with open('permanent_list.txt', 'r', encoding='utf-8') as file:
        current_row = 2
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',', )
            name = parts[0]
            pluses = parts[1]
            from_who = parts[2]
            requests.append({
                'updateCells': {
                    'range': {
                        'sheetId': sheet_id, 'startRowIndex': current_row,
                        'endRowIndex': current_row + 1,
                        'startColumnIndex': 3, 'endColumnIndex': 6
                    },
                    'rows': [
                        {
                            'values': [
                                generate_cell(name, h_a='LEFT'),
                                generate_cell(pluses),
                                generate_cell(from_who, h_a='LEFT'),
                            ]
                        }
                    ]
                }
            })
            current_row += 1

    # Добавление ключа fields в словарь updateCells для всех requests
    for request in requests:
        updateCells = request.get('updateCells')
        if updateCells:
            updateCells['fields'] = (
                'userEnteredValue,dataValidation,userEnteredFormat(textFormat,horizontalAlignment,'
                'verticalAlignment,backgroundColor,borders)'
            )

    if requests:  # Выполняем только если есть запросы
        await wrapper_services.as_service_account(
            service.spreadsheets.batchUpdate(
                spreadsheetId=spreadsheetid, json={'requests': requests}
            )
        )

    requests.append(  # запись 1-2 строки
        {
            'updateCells': {
                'range': {
                    'sheetId': sheet_id, 'startRowIndex': 0, 'endRowIndex': 1,
                    'startColumnIndex': 3, 'endColumnIndex': 7
                },
                'rows': [
                    {
                        'values': [
                            generate_cell('', COLORS.get('l-g-2')),
                            generate_cell('=СУММ(E40:E)', COLORS.get('l-g-2'), value_type='formula', is_bold=True),
                            generate_cell('', COLORS.get('l-g-2')),
                            generate_cell('', COLORS.get('l-g-2')),
                        ]
                    }
                ]
            }
        }
    )
    requests.append(  # запись 1-2 строки
        {
            'updateCells': {
                'range': {
                    'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': 2,
                    'startColumnIndex': 0, 'endColumnIndex': 7
                },
                'rows': [
                    {
                        'values': [
                            generate_cell('=СУММ(A3:A)', COLORS.get('l-gr-2'), value_type='formula', is_bold=True),
                            generate_cell('=СУММ(B3:B)', COLORS.get('l-r-2'), value_type='formula', is_bold=True),
                            generate_cell('=СУММ(C3:C)', COLORS.get('l-g-1'), value_type='formula', is_bold=True),
                            generate_cell('Фамилия, Имя', COLORS.get('l-g-2'), is_bold=True, h_a='LEFT'),
                            generate_cell('Плюсы', COLORS.get('l-g-2'), is_bold=True),
                            generate_cell('Внесено от', COLORS.get('l-g-2'), is_bold=True, h_a='LEFT'),
                            generate_cell('Тип браслета', COLORS.get('l-g-2'), is_bold=True, h_a='LEFT'),
                        ]
                    }
                ]
            }
        }
    )
    requests.append(  # закрепление первых 2 строк
        {"updateSheetProperties": {"properties": {
            "sheetId": sheet_id, "gridProperties": {"frozenRowCount": 2}
        }, "fields": "gridProperties.frozenRowCount"}}
    )
    # добавление постоянного списка
    with open('permanent_list.txt', 'r', encoding='utf-8') as file:
        current_row = 2
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',', )
            name = parts[0]
            pluses = parts[1]
            from_who = parts[2]
            requests.append( # добавление постоянного списка
                {
                    'updateCells': {
                        'range': {
                            'sheetId': sheet_id, 'startRowIndex': current_row,
                            'endRowIndex': current_row + 1,
                            'startColumnIndex': 3, 'endColumnIndex': 6
                        },
                        'rows': [
                            {
                                'values': [
                                    generate_cell(name, h_a='LEFT'),
                                    generate_cell(pluses),
                                    generate_cell(from_who, h_a='LEFT'),
                                ]
                            }
                        ]
                    }
                }
            )
            current_row += 1
    # центрирование для столбцов A, B, C, E
    requests.append({ # Столбцы A, B, C
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0, "endRowIndex": 2000,
                "startColumnIndex": 0, "endColumnIndex": 3
            },
            "cell": {
                "userEnteredFormat": {
                    "horizontalAlignment": "CENTER",
                    "verticalAlignment": "MIDDLE"
                }
            },
            "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment)"
        }
    })
    requests.append({ # столбец E
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0, "endRowIndex": 2000,
                "startColumnIndex": 4, "endColumnIndex": 5
            },
            "cell": {
                "userEnteredFormat": {
                    "horizontalAlignment": "CENTER",
                    "verticalAlignment": "MIDDLE"
                }
            },
            "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment)"
        }
    })
    # выравнивание по левому краю для столбцов D и F
    requests.append({ # столбец D
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0, "endRowIndex": 2000,
                "startColumnIndex": 3, "endColumnIndex": 4
            },
            "cell": {
                "userEnteredFormat": {
                    "horizontalAlignment": "LEFT",
                    "verticalAlignment": "MIDDLE"
                }
            },
            "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment)"
        }
    })
    # добавление ключа fields в словарь updateCells для всех requests, где он есть
    for request in requests:
        updateCells = request.get('updateCells')
        if updateCells:
            updateCells['fields'] = (
                'userEnteredValue,dataValidation,userEnteredFormat(textFormat,horizontalAlignment,'
                'verticalAlignment,backgroundColor,borders)'
            )
    await wrapper_services.as_service_account(
        service.spreadsheets.batchUpdate(
            spreadsheetId=spreadsheetid, json={'requests': requests}
        )
    )


