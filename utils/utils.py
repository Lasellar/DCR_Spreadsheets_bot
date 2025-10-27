from aiogoogle import Aiogoogle

from settings import COLORS


def get_working_hours(start_time: str, end_time: str) -> list:
    """
    Принимает строки со временем начала и конца мероприятия и возвращает
    список часов, когда формируется отчет.
    :param start_time: Строка вида 18:30
    :param end_time: Строка вида 04:30
    :return: Список часов. Например: ['01:00', '02:00', '02:30']
    """
    result = list()
    start_hour, start_minute = map(int, start_time.split(':'))
    end_hour, end_minute = map(int, end_time.split(':'))
    start_total_minutes = start_hour * 60 + start_minute
    end_total_minutes = end_hour * 60 + end_minute
    if end_total_minutes <= start_total_minutes:
        end_total_minutes += 24 * 60
    current_minutes = (start_total_minutes // 60 + 1) * 60
    while current_minutes < end_total_minutes:
        current_hour = (current_minutes // 60) % 24
        current_minute = current_minutes % 60
        result.append(f'{current_hour:02d}:{current_minute:02d}')
        current_minutes += 60
    if end_total_minutes % 60 != 0 or current_minutes > end_total_minutes:
        final_hour = (end_total_minutes // 60) % 24
        final_minute = end_total_minutes % 60
        result.append(f'{final_hour:02d}:{final_minute:02d}')
    else:
        result.append(end_time)
    return result


async def set_user_permissions(
    spreadsheetid: str, wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'anyone', 'role': 'writer', 'allowFileDiscovery': False
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid, json=permissions_body, fields='id'
        )
    )


async def generate_three_sheets(rows_count):
    return {
        'properties': {
            'sheetType': 'GRID', 'sheetId': 0,
            'title': 'РЕЗУЛЬТАТ',
            'gridProperties': {
                'rowCount': rows_count, 'columnCount': 8
            }, 'tabColor': COLORS.get('r')
        }
    }





