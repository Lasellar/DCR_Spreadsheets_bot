from time import sleep
from aiogoogle import Aiogoogle


async def copy_sheet_from_template(
        target_spreadsheet_id: str,
        source_spreadsheet_url: str,
        wrapper_services: Aiogoogle,
) -> int:
    """Копирует лист из шаблона и возвращает ID скопированного листа"""
    service = await wrapper_services.discover('sheets', 'v4')
    source_spreadsheet_id = source_spreadsheet_url.split('/d/')[1].split('/')[0]
    source_spreadsheet = await wrapper_services.as_service_account(
        service.spreadsheets.get(spreadsheetId=source_spreadsheet_id)
    )
    source_sheet_id = None
    for sheet in source_spreadsheet.get('sheets'):
        if sheet['properties']['title'] == 'РАССЧЕТ':
            source_sheet_id = sheet['properties']['sheetId']
            break
    if not source_sheet_id:
        raise Exception("Лист 'РАССЧЕТ' не найден в исходном документе")
    copy_response = await wrapper_services.as_service_account(
        service.spreadsheets.sheets.copyTo(
            spreadsheetId=source_spreadsheet_id,
            sheetId=source_sheet_id,
            json={'destinationSpreadsheetId': target_spreadsheet_id}
        )
    )
    return copy_response['sheetId']


async def update_third_sheet(
        spreadsheetid: str,
        wrapper_services: Aiogoogle,
        use_template: bool = False,
        template_url: str = None
) -> None:
    if use_template and template_url:
        copied_sheet_id = await copy_sheet_from_template(
            spreadsheetid, template_url, wrapper_services
        )
        service = await wrapper_services.discover('sheets', 'v4')
        sleep(1)
        requests = [{'updateSheetProperties': {
            'properties': {
                'sheetId': copied_sheet_id, 'title': 'РАССЧЕТ'
            }, 'fields': 'title'}}]
        await wrapper_services.as_service_account(
            service.spreadsheets.batchUpdate(
                spreadsheetId=spreadsheetid,
                json={'requests': requests}
            )
        )