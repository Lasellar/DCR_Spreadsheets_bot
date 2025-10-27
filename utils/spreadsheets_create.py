from aiogoogle import Aiogoogle

from .utils import generate_three_sheets


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        date: str,
        event_title: str,
        rows_count: int
) -> str:
    date_f = date.split('.')
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': f'DCR: {date_f[2]}-{date_f[1]}-{date_f[0]} [{event_title}]',
            'locale': 'ru_RU'
        },
        'sheets': [
            await generate_three_sheets(rows_count)
        ]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response.get('spreadsheetId')
    return spreadsheetid
