from time import sleep

from aiogoogle import Aiogoogle

from settings import cred, TEMPLATE_URL_SECOND, TEMPLATE_URL_THIRD, COLORS
from .sheet_calculation import update_third_sheet
from .sheet_guestlist import update_second_sheet
from .sheet_result import update_first_sheet
from .spreadsheets_create import spreadsheets_create
from .utils import get_working_hours, set_user_permissions


async def create_spreadsheet(
        date: str,
        event_title: str,
        start_time: str,
        end_time: str,
        presale_init: str,
        cash_init: str,
        card_init: str,
        guest_init: str,
        artist_init: str,
        staff_init: str,
        price_on_doors: str = '0',
        rega_init: str = '0',
        rest_init: str = '0',
        is_rega: bool = False,
        is_rest: bool = False,
):
    async with Aiogoogle(service_account_creds=cred) as wrapper_services:
        working_hours = get_working_hours(start_time, end_time)
        rega = 2 if is_rega else 0
        rest = 2 if is_rest else 0
        rows_count = len(working_hours) * 3 + rega + rest + 17
        spreadsheetid = await spreadsheets_create(
            wrapper_services, date, event_title, rows_count
        )
        rest_color = COLORS.get('l-b-1')
        rega_color = COLORS.get('l-r-1')
        sleep(1)
        await set_user_permissions(spreadsheetid, wrapper_services)
        await update_second_sheet(
            spreadsheetid=spreadsheetid,
            wrapper_services=wrapper_services,
            template_url=TEMPLATE_URL_SECOND
        )
        await update_third_sheet(
            spreadsheetid=spreadsheetid,
            wrapper_services=wrapper_services,
            use_template=True,
            template_url=TEMPLATE_URL_THIRD
        )
        await update_first_sheet(
            spreadsheetid=spreadsheetid,
            wrapper_services=wrapper_services,
            date=date,
            event_title=event_title,
            working_hours=working_hours,
            price_on_doors=price_on_doors,
            presale_init=presale_init,
            cash_init=cash_init,
            card_init=card_init,
            is_rega=is_rega,
            rega_color=rega_color,
            rega_init=rega_init,
            is_rest=is_rest,
            rest_color=rest_color,
            rest_init=rest_init,
            guest_init=guest_init,
            staff_init=staff_init,
            artist_init=artist_init,
        )
        created_spreadsheet_link = f'https://docs.google.com/spreadsheets/d/{spreadsheetid}'
        print(created_spreadsheet_link)
    return created_spreadsheet_link
