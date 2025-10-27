from aiogoogle import Aiogoogle

from settings import COLORS, VALUES_1SH_3ROW
from .generate_cell import generate_cell


async def update_first_sheet(
    spreadsheetid: str, wrapper_services: Aiogoogle,
    date: str, event_title: str,
    working_hours: list,
    price_on_doors: str,
    presale_init: str,
    cash_init: str,
    card_init: str,
    is_rega: bool,
    is_rest: bool = False,
    rega_init: str = str(700),
    rest_init: str = str(700),
    guest_init: str = str(300),
    artist_init: str = str(200),
    staff_init: str = str(100),
    rega_color: dict = COLORS.get('l-b-1'),
    rest_color: dict = COLORS.get('l-r-1'),
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    requests = list()
    requests.append( # объединение ячеек A1:H2(тайтл отчета)
        {'mergeCells': {
            'range': {
                'sheetId': 0, 'startRowIndex': 0, 'endRowIndex': 2,
                'startColumnIndex': 0, 'endColumnIndex': 8
            },
            'mergeType': 'MERGE_ALL'}}
    )
    requests.append( # запись тайтла отчета
        {'updateCells': {
            'range': {
                'sheetId': 0, 'startRowIndex': 0, 'endRowIndex': 2,
                'startColumnIndex': 0, 'endColumnIndex': 8
            },
            'rows': [
                {'values': [
                    generate_cell(
                        f'{date} {event_title}', COLORS.get('l-g-2'),
                        is_bold=True, font_size=12
                    )]}]
            }
        }
    )
    requests.append( # запись 3 строки(Браслет, Цена, Было...)
        {
            'updateCells': {
                'range': {
                    'sheetId': 0, 'startRowIndex': 2, 'endRowIndex': 3,
                    'startColumnIndex': 0, 'endColumnIndex': 8
                },
                'rows': [
                    {
                        'values': [
                            generate_cell(value, COLORS.get('l-g-2'), is_bold=True)
                            for value in VALUES_1SH_3ROW
                        ]
                    }
                ]
            }
        }
    )
    requests.append( # закрепление первых 3 строк
        {"updateSheetProperties": {"properties": {
            "sheetId": 0, "gridProperties": {"frozenRowCount": 3}
        }, "fields": "gridProperties.frozenRowCount"}}
    )
    len_working_hours = len(working_hours)
    len_of_ticket_category = len_working_hours + 2
    current_row = 4
    presale_start_row = current_row
    presale_end_row = current_row + len_working_hours - 1
    for hour in working_hours:
        if working_hours.index(hour) == 0:
            requests.append( # добавление первого часа для PRESALE
                {
                    'updateCells': {
                        'range': {
                            'sheetId': 0, 'startRowIndex': current_row - 1,
                            'endRowIndex': current_row,
                            'startColumnIndex': 0, 'endColumnIndex': 8
                        },
                        'rows': [
                            {
                                'values': [ # первая строка для PRESALE
                                    generate_cell(
                                        f'A {hour}', COLORS.get('l-y-3'), h_a='LEFT', is_bold=True),
                                    generate_cell(0, COLORS.get('l-y-3'), value_type='number'),
                                    generate_cell(presale_init, COLORS.get('l-y-3'), value_type='number'),
                                    generate_cell(
                                        f'=C{current_row}', COLORS.get('l-y-3'), value_type='formula'),
                                    generate_cell(
                                        f'=C{current_row}-D{current_row}', COLORS.get('l-y-3'),
                                        value_type='formula'),
                                    generate_cell(
                                        f'=B{current_row}*E{current_row}', COLORS.get('l-y-3'),
                                        value_type='formula'),
                                    generate_cell(0, COLORS.get('l-y-3'), value_type='number'),
                                    generate_cell(0, COLORS.get('l-y-3'), value_type='number'),
                                ]
                            }
                        ]
                    }
                }
            )
            requests.append( # добавление первого часа для CASH
                {
                    'updateCells': {
                        'range': {
                            'sheetId': 0,
                            'startRowIndex': current_row - 1 + len_of_ticket_category,
                            'endRowIndex': current_row + len_of_ticket_category,
                            'startColumnIndex': 0, 'endColumnIndex': 8
                        },
                        'rows': [
                            {
                                'values':  [ # первая строка для CASH
                                    generate_cell(f'B {hour}', COLORS.get('l-v-3'), h_a='LEFT', is_bold=True),
                                    generate_cell(price_on_doors, COLORS.get('l-v-3'), value_type='number'),
                                    generate_cell(cash_init, COLORS.get('l-v-3'), value_type='number'),
                                    generate_cell(
                                        f'=C{current_row + len_of_ticket_category}',
                                        COLORS.get('l-v-3'), value_type='formula'
                                    ),
                                    generate_cell(
                                        f'=C{current_row + len_of_ticket_category}-D{current_row + len_of_ticket_category}',
                                        COLORS.get('l-v-3'), value_type='formula'
                                    ),
                                    generate_cell(
                                        f'=B{current_row + len_of_ticket_category}*E{current_row + len_of_ticket_category}',
                                        COLORS.get('l-v-3'), value_type='formula'
                                    ),
                                    generate_cell(0, COLORS.get('l-v-3'), value_type='number'),
                                    generate_cell(0, COLORS.get('l-v-3'), value_type='number'),
                                ]
                            }
                        ]
                    }
                }
            )
            requests.append( # добавление первого часа для CARD
                {
                    'updateCells': {
                        'range': {
                            'sheetId': 0,
                            'startRowIndex': current_row - 1 + len_of_ticket_category * 2,
                            'endRowIndex': current_row + len_of_ticket_category * 2,
                            'startColumnIndex': 0, 'endColumnIndex': 8
                        },
                        'rows': [
                            {
                                'values': [ # первая строка для CARD
                                    generate_cell(f'C {hour}', COLORS.get('l-p-3'), h_a='LEFT', is_bold=True),
                                    generate_cell(price_on_doors, COLORS.get('l-p-3'), value_type='number'),
                                    generate_cell(card_init, COLORS.get('l-p-3'), value_type='number'),
                                    generate_cell(
                                        f'=C{current_row + len_of_ticket_category * 2}',
                                        COLORS.get('l-p-3'), value_type='formula'
                                    ),
                                    generate_cell(
                                        f'=C{current_row + len_of_ticket_category * 2}'
                                        f'-D{current_row + len_of_ticket_category * 2}',
                                        COLORS.get('l-p-3'), value_type='formula'
                                    ),
                                    generate_cell(
                                        f'=B{current_row + len_of_ticket_category * 2}'
                                        f'*E{current_row + len_of_ticket_category * 2}',
                                        COLORS.get('l-p-3'), value_type='formula'
                                    ),
                                    generate_cell(0, COLORS.get('l-p-3'), value_type='number'),
                                    generate_cell(0, COLORS.get('l-p-3'), value_type='number'),
                                ]
                            }
                        ]
                    }
                }
            )
        else:
            requests.append( # добавление часов кроме первого для PRESALE
                {
                    'updateCells': {
                        'range': {
                            'sheetId': 0,
                            'startRowIndex': current_row - 1,
                            'endRowIndex': current_row,
                            'startColumnIndex': 0, 'endColumnIndex': 8
                        },
                        'rows': [
                            {
                                'values': [ # клетки строки кроме первой для PRESALE
                                    generate_cell(f'A {hour}', COLORS.get('l-y-3'), h_a='LEFT', is_bold=True),
                                    generate_cell(0, COLORS.get('l-y-3'), value_type='number'),
                                    generate_cell(f'=D{current_row - 1}', COLORS.get('l-y-3'),
                                                  value_type='formula'),
                                    generate_cell(f'=C{current_row}', COLORS.get('l-y-3'),
                                                  value_type='formula'),
                                    generate_cell(f'=C{current_row}-D{current_row}', COLORS.get('l-y-3'),
                                                  value_type='formula'),
                                    generate_cell(f'=B{current_row}*E{current_row}', COLORS.get('l-y-3'),
                                                  value_type='formula'),
                                    generate_cell(0, COLORS.get('l-y-3'), value_type='number'),
                                    generate_cell(0, COLORS.get('l-y-3'), value_type='number'),
                                ]
                            }
                        ]
                    }
                }
            )
            requests.append( # добавление часов кроме первого для CASH
                {
                    'updateCells': {
                        'range': {
                            'sheetId': 0, 'startRowIndex': current_row - 1 + len_of_ticket_category,
                            'endRowIndex': current_row + len_of_ticket_category,
                            'startColumnIndex': 0, 'endColumnIndex': 8
                        },
                        'rows': [
                            {
                                'values': [ # клетки строки кроме первой для CASH
                                    generate_cell(f'B {hour}', COLORS.get('l-v-3'), h_a='LEFT', is_bold=True),
                                    generate_cell(price_on_doors, COLORS.get('l-v-3'), value_type='number'),
                                    generate_cell(f'=D{current_row - 1 + len_of_ticket_category}',
                                                  COLORS.get('l-v-3'), value_type='formula'),
                                    generate_cell(f'=C{current_row + len_of_ticket_category}',
                                                  COLORS.get('l-v-3'), value_type='formula'),
                                    generate_cell(f'=C{current_row + len_of_ticket_category}-'
                                                  f'D{current_row + len_of_ticket_category}',
                                                  COLORS.get('l-v-3'), value_type='formula'),
                                    generate_cell(f'=B{current_row + len_of_ticket_category}'
                                                  f'*E{current_row + len_of_ticket_category}',
                                                  COLORS.get('l-v-3'), value_type='formula'),
                                    generate_cell(0, COLORS.get('l-v-3'), value_type='number'),
                                    generate_cell(0, COLORS.get('l-v-3'), value_type='number'),
                                ]
                            }
                        ]
                    }
                }
            )
            requests.append(  # добавление часов кроме первого для CARD
                {
                    'updateCells': {
                        'range': {
                            'sheetId': 0, 'startRowIndex': current_row - 1 + len_of_ticket_category * 2,
                            'endRowIndex': current_row + len_of_ticket_category * 2,
                            'startColumnIndex': 0, 'endColumnIndex': 8
                        },
                        'rows': [
                            {
                                'values': [  # клетки строки кроме первой для CARD
                                    generate_cell(f'C {hour}', COLORS.get('l-p-3'), h_a='LEFT', is_bold=True),
                                    generate_cell(price_on_doors, COLORS.get('l-p-3'), value_type='number'),
                                    generate_cell(f'=D{current_row - 1 + len_of_ticket_category * 2}',
                                                  COLORS.get('l-p-3'), value_type='formula'),
                                    generate_cell(f'=C{current_row + len_of_ticket_category * 2}',
                                                  COLORS.get('l-p-3'), value_type='formula'),
                                    generate_cell(f'=C{current_row + len_of_ticket_category * 2}-'
                                                  f'D{current_row + len_of_ticket_category * 2}',
                                                  COLORS.get('l-p-3'), value_type='formula'),
                                    generate_cell(f'=B{current_row + len_of_ticket_category * 2}'
                                                  f'*E{current_row + len_of_ticket_category * 2}',
                                                  COLORS.get('l-p-3'), value_type='formula'),
                                    generate_cell(0, COLORS.get('l-p-3'), value_type='number'),
                                    generate_cell(0, COLORS.get('l-p-3'), value_type='number'),
                                ]
                            }
                        ]
                    }
                }
            )
        current_row += 1
    requests.append( # добавление строки PRESALE TTL
        {
            'updateCells': {
                'range': {
                    'sheetId': 0, 'startRowIndex': current_row - 1,
                    'endRowIndex': current_row,
                    'startColumnIndex': 0, 'endColumnIndex': 8
                },
                'rows': [
                    {
                        'values': [ # строка PRESALE TTL
                            generate_cell('PRESALE TTL', COLORS.get('l-y-2'), h_a='LEFT', is_bold=True),
                            generate_cell('', COLORS.get('l-y-2')),
                            generate_cell('', COLORS.get('l-y-2')),
                            generate_cell('', COLORS.get('l-y-2')),
                            generate_cell(f'=СУММ(E{presale_start_row}:E{presale_end_row})',
                                          COLORS.get('l-y-2'), value_type='formula'),
                            generate_cell(f'=СУММ(F{presale_start_row}:F{presale_end_row})',
                                          COLORS.get('l-y-2'), value_type='formula'),
                            generate_cell(0, COLORS.get('l-y-2'), value_type='number'),
                            generate_cell(0, COLORS.get('l-y-2'), value_type='number'),
                        ]
                    }
                ]
            }
        }
    )
    presale_ttl_row = presale_end_row + 1
    requests.append( # добавление строки B TTL (CASH ON DOORS)
        {
            'updateCells': {
                'range': {
                    'sheetId': 0, 'startRowIndex': current_row - 1 + len_of_ticket_category,
                    'endRowIndex': current_row + len_of_ticket_category,
                    'startColumnIndex': 0, 'endColumnIndex': 8
                },
                'rows': [
                    {
                        'values': [ # строка B TTL (CASH ON DOORS)
                            generate_cell('B TTL (CASH ON DOORS)', COLORS.get('l-v-2'), h_a='LEFT', is_bold=True),
                            generate_cell('', COLORS.get('l-v-2')),
                            generate_cell('', COLORS.get('l-v-2')),
                            generate_cell('', COLORS.get('l-v-2')),
                            generate_cell(
                                f'=СУММ(E{presale_start_row + len_of_ticket_category}'
                                f':E{presale_end_row + len_of_ticket_category})',
                                COLORS.get('l-v-2'), value_type='formula'),
                            generate_cell(
                                f'=СУММ(F{presale_start_row + len_of_ticket_category}'
                                f':F{presale_end_row + len_of_ticket_category})',
                                COLORS.get('l-v-2'), value_type='formula'),
                            generate_cell(0, COLORS.get('l-v-2'), value_type='number'),
                            generate_cell(0, COLORS.get('l-v-2'), value_type='number'),
                        ]
                    }
                ]
            }
        }
    )
    cash_ttl_row = presale_end_row + len_of_ticket_category + 1
    requests.append(  # добавление строки С TTL (CARD ON DOORS)
        {
            'updateCells': {
                'range': {
                    'sheetId': 0, 'startRowIndex': current_row - 1 + len_of_ticket_category * 2,
                    'endRowIndex': current_row + len_of_ticket_category * 2 + 1,
                    'startColumnIndex': 0, 'endColumnIndex': 8
                },
                'rows': [
                    {
                        'values': [  # строка С TTL
                            generate_cell('С TTL (CARD ON DOORS)', COLORS.get('l-p-1'), h_a='LEFT', is_bold=True),
                            generate_cell('', COLORS.get('l-p-1')),
                            generate_cell('', COLORS.get('l-p-1')),
                            generate_cell('', COLORS.get('l-p-1')),
                            generate_cell(
                                f'=СУММ(E{presale_start_row + len_of_ticket_category * 2}'
                                f':E{presale_end_row + len_of_ticket_category * 2})',
                                COLORS.get('l-p-1'), value_type='formula'),
                            generate_cell(
                                f'=СУММ(F{presale_start_row + len_of_ticket_category * 2}'
                                f':F{presale_end_row + len_of_ticket_category * 2})',
                                COLORS.get('l-p-1'), value_type='formula'),
                            generate_cell(0, COLORS.get('l-p-1'), value_type='number'),
                            generate_cell(0, COLORS.get('l-p-1'), value_type='number'),
                        ]
                    },
                    {
                        'values': [  # строка С TTL (После налогов)
                            generate_cell('С TTL (После налогов)', COLORS.get('l-p-1'), h_a='LEFT', is_bold=True),
                            generate_cell('', COLORS.get('l-p-1')),
                            generate_cell('', COLORS.get('l-p-1')),
                            generate_cell('', COLORS.get('l-p-1')),
                            generate_cell('', COLORS.get('l-p-1')),
                            generate_cell(
                                f'=F{presale_end_row + len_of_ticket_category * 2 + 1}*0,9',
                                COLORS.get('l-p-1'), value_type='formula'),
                            generate_cell(0, COLORS.get('l-p-1'), value_type='number'),
                            generate_cell(0, COLORS.get('l-p-1'), value_type='number'),
                        ]
                    }
                ]
            }
        }
    )
    card_ttl_row = presale_end_row + len_of_ticket_category * 2 + 1
    current_row = presale_end_row + len_of_ticket_category * 2 + 3
    rega_rest_rows = []
    rest_ttl_row = None
    rega_ttl_row = None
    # вариант 1: есть рега, но нет рестика
    if is_rega and not is_rest:
        rega_rest_rows.extend([
            {
                'values': [
                    generate_cell('E РЕГА', rega_color, h_a='LEFT', is_bold=True),
                    generate_cell('', rega_color),
                    generate_cell(rega_init, rega_color, value_type='number'),
                    generate_cell(rega_init, rega_color, value_type='number'),
                    generate_cell(f'=C{current_row + 1}-D{current_row + 1}', rega_color, value_type='formula'),
                    generate_cell('', rega_color),
                    generate_cell('', rega_color),
                    generate_cell('', rega_color),
                ]
            }
        ])
        rega_ttl_row = current_row + 1
    # вариант 2: нет реги, но есть рестик
    elif not is_rega and is_rest:
        rega_rest_rows.extend([
            {
                'values': [
                    generate_cell('R РЕСТИК', rest_color, h_a='LEFT', is_bold=True),
                    generate_cell('', rest_color),
                    generate_cell(rest_init, rest_color, value_type='number'),
                    generate_cell(rest_init, rest_color, value_type='number'),
                    generate_cell(f'=C{current_row + 1}-D{current_row + 1}', rest_color, value_type='formula'),
                    generate_cell('', rest_color),
                    generate_cell('', rest_color),
                    generate_cell('', rest_color),
                ]
            }
        ])
        rest_ttl_row = current_row + 1

    # вариант 3: есть рега и есть рестик
    elif is_rega and is_rest:
        rega_rest_rows.extend([
            {
                'values': [
                    generate_cell('E РЕГА', rega_color, h_a='LEFT', is_bold=True),
                    generate_cell('', rega_color),
                    generate_cell(rega_init, rega_color, value_type='number'),
                    generate_cell(rega_init, rega_color, value_type='number'),
                    generate_cell(f'=C{current_row + 1}-D{current_row + 1}', rega_color, value_type='formula'),
                    generate_cell('', rega_color),
                    generate_cell('', rega_color),
                    generate_cell('', rega_color),
                ]
            },
            {'values': []},
            {
                'values': [
                    generate_cell('R РЕСТИК', rest_color, h_a='LEFT', is_bold=True),
                    generate_cell('', rest_color),
                    generate_cell(rest_init, rest_color, value_type='number'),
                    generate_cell(rest_init, rest_color, value_type='number'),
                    generate_cell(f'=C{current_row + 3}-D{current_row + 3}', rest_color, value_type='formula'),
                    generate_cell('', rest_color),
                    generate_cell('', rest_color),
                    generate_cell('', rest_color),
                ]
            }
        ])
        rega_ttl_row = current_row + 1
        rest_ttl_row = current_row + 3
    elif not is_rega and not is_rest:
        current_row -= 1
    # вариант 4: нет реги и нет рестика - ничего не добавляем
    # добавляем блок рега/рестик в requests, если есть что добавлять
    if rega_rest_rows:
        requests.append({
            'updateCells': {
                'range': {
                    'sheetId': 0,
                    'startRowIndex': current_row,
                    'endRowIndex': current_row + len(rega_rest_rows),
                    'startColumnIndex': 0,
                    'endColumnIndex': 8
                },
                'rows': rega_rest_rows
            }
        })
    current_row += len(rega_rest_rows)
    result_value = f'{'E+' if is_rega else ''}{'R+' if is_rest else ''}A+B+C (Полный итог)'
    tickets_ttl_formula = f'=E{presale_ttl_row}+E{cash_ttl_row}+E{card_ttl_row}'
    if all([rest_ttl_row, rega_ttl_row]):
        tickets_ttl_formula += f'+E{rest_ttl_row}+E{rega_ttl_row}'
    elif rest_ttl_row:
        tickets_ttl_formula += f'+E{rest_ttl_row}'
    elif rega_ttl_row:
        tickets_ttl_formula += f'+E{rega_ttl_row}'
    tickets_ttl_money_formula = f'=F{cash_ttl_row}+F{card_ttl_row}'
    full_result_row = current_row + 1
    requests.append(  # добавление строки Полный итог
        {
            'updateCells': {
                'range': {
                    'sheetId': 0, 'startRowIndex': full_result_row,
                    'endRowIndex': full_result_row + 1,
                    'startColumnIndex': 0, 'endColumnIndex': 8
                },
                'rows': [
                    {
                        'values': [  # строка A+B+C (Полный итог)
                            generate_cell(result_value, COLORS.get('g'), h_a='LEFT', is_bold=True),
                            generate_cell('', COLORS.get('g')),
                            generate_cell('', COLORS.get('g')),
                            generate_cell('', COLORS.get('g')),
                            generate_cell(
                                tickets_ttl_formula, COLORS.get('g'), value_type='formula',
                                borders={
                                    'left': {'style': 'SOLID_THICK'},
                                    'bottom': {'style': 'SOLID_THICK'},
                                }
                            ),
                            generate_cell(
                                tickets_ttl_money_formula, COLORS.get('g'), value_type='formula',
                                borders={
                                    'bottom': {'style': 'SOLID_THICK'},
                                    'right': {'style': 'SOLID_THICK'},
                                }
                            ),
                            generate_cell('', COLORS.get('g')),
                            generate_cell('', COLORS.get('g')),
                        ]
                    }
                ]
            }
        }
    )
    requests.append(  # добавление строк со списочных категорий + Итог S+T
        {
            'updateCells': {
                'range': {
                    'sheetId': 0, 'startRowIndex': full_result_row + 1,
                    'endRowIndex': full_result_row + 7,
                    'startColumnIndex': 0, 'endColumnIndex': 8
                },
                'rows': [
                    {
                        'values': [  # строка F (Списки)
                            generate_cell('F (Списки)', COLORS.get('l-gr-3'), h_a='LEFT', is_bold=True),
                            generate_cell('', COLORS.get('l-gr-3')),
                            generate_cell(guest_init, COLORS.get('l-gr-3'), value_type='number'),
                            generate_cell(guest_init, COLORS.get('l-gr-3'), value_type='number'),
                            generate_cell(
                                f'=C{full_result_row + 2}-D{full_result_row + 2}',
                                COLORS.get('l-gr-3'), value_type='formula'),
                            generate_cell('', COLORS.get('l-gr-3')),
                            generate_cell(f"='СПИСКИ'!A2", COLORS.get('l-gr-3'), value_type='formula'),
                            generate_cell(
                                f'=E{full_result_row + 2}-G{full_result_row + 2}',
                                COLORS.get('l-gr-3'), value_type='formula'),
                        ]
                    },
                    {
                        'values': [  # строка S (Артисты)
                            generate_cell('S (Артисты)', COLORS.get('l-gr-3'), h_a='LEFT', is_bold=True),
                            generate_cell('', COLORS.get('l-gr-3')),
                            generate_cell(artist_init, COLORS.get('l-gr-3'), value_type='number'),
                            generate_cell(artist_init, COLORS.get('l-gr-3'), value_type='number'),
                            generate_cell(
                                f'=C{full_result_row + 3}-D{full_result_row + 3}',
                                COLORS.get('l-gr-3'), value_type='formula'),
                            generate_cell('', COLORS.get('l-gr-3')),
                            generate_cell(f"='СПИСКИ'!B2", COLORS.get('l-gr-3'), value_type='formula'),
                            generate_cell(
                                f'=E{full_result_row + 3}-G{full_result_row + 3}',
                                COLORS.get('l-gr-3'), value_type='formula'),
                        ]
                    },
                    {
                        'values': [  # строка T (Техники)
                            generate_cell('T (Техники)', COLORS.get('l-gr-3'), h_a='LEFT', is_bold=True),
                            generate_cell('', COLORS.get('l-gr-3')),
                            generate_cell(staff_init, COLORS.get('l-gr-3'), value_type='number'),
                            generate_cell(staff_init, COLORS.get('l-gr-3'), value_type='number'),
                            generate_cell(
                                f'=C{full_result_row + 4}-D{full_result_row + 4}',
                                COLORS.get('l-gr-3'), value_type='formula'),
                            generate_cell('', COLORS.get('l-gr-3')),
                            generate_cell(f"='СПИСКИ'!C2", COLORS.get('l-gr-3'), value_type='formula'),
                            generate_cell(
                                f'=E{full_result_row + 4}-G{full_result_row + 4}',
                                COLORS.get('l-gr-3'), value_type='formula'),
                        ]
                    },
                    {
                        'values': [  # строка Итого
                            generate_cell('Итого', COLORS.get('l-gr-2'), h_a='LEFT', is_bold=True),
                            generate_cell('', COLORS.get('l-gr-2')),
                            generate_cell('', COLORS.get('l-gr-2')),
                            generate_cell('', COLORS.get('l-gr-2')),
                            generate_cell(
                                f'=E{full_result_row + 3}+E{full_result_row + 4}',
                                COLORS.get('l-gr-2'), value_type='formula'),
                            generate_cell('', COLORS.get('l-gr-2')),
                            generate_cell('', COLORS.get('l-gr-2')),
                            generate_cell('', COLORS.get('l-gr-2')),
                        ]
                    },
                    {
                        'values': [  # строка Все гости
                            generate_cell('Все гости', COLORS.get('p'), h_a='LEFT', is_bold=True),
                            generate_cell('', COLORS.get('p')),
                            generate_cell('', COLORS.get('p')),
                            generate_cell('', COLORS.get('p')),
                            generate_cell(
                                f'=E{full_result_row + 1}+E{full_result_row + 2}',
                                COLORS.get('p'), value_type='formula'),
                            generate_cell('', COLORS.get('p')),
                            generate_cell('', COLORS.get('p')),
                            generate_cell('', COLORS.get('p')),
                        ]
                    },
                    {
                        'values': [  # строка Все гости + персонал
                            generate_cell('Все гости + персонал', COLORS.get('p'), h_a='LEFT', is_bold=True),
                            generate_cell('', COLORS.get('p')),
                            generate_cell('', COLORS.get('p')),
                            generate_cell('', COLORS.get('p')),
                            generate_cell(
                                f'=E{full_result_row + 5}+E{full_result_row + 6}',
                                COLORS.get('p'), value_type='formula'),
                            generate_cell('', COLORS.get('p')),
                            generate_cell('', COLORS.get('p')),
                            generate_cell('', COLORS.get('p')),
                        ]
                    }
                ]
            }
        }
    )
    # добавление ключа fields в словарь updateCells для всех requests, где он есть
    for request in requests:
        updateCells = request.get('updateCells')
        if updateCells:
            updateCells['fields'] = (
                'userEnteredValue,userEnteredFormat(textFormat,horizontalAlignment,'
                'verticalAlignment,backgroundColor,borders)'
            )
    requests.append(
        {'repeatCell': {'range': {
            'sheetId': 0,
            'startColumnIndex': 1, 'endColumnIndex': 2,
            'startRowIndex': 3, 'endRowIndex': full_result_row,
            },
            'cell': {'userEnteredFormat': {
                    'numberFormat': {'type': 'CURRENCY', 'pattern': "#,##0.00\" ₽\""}}},
            'fields': 'userEnteredFormat.numberFormat'
            }
        }
    )
    requests.append(
        {'repeatCell': {'range': {
            'sheetId': 0,
            'startColumnIndex': 6, 'endColumnIndex': 8,
            'startRowIndex': 3, 'endRowIndex': full_result_row,
        },
            'cell': {'userEnteredFormat': {
                'numberFormat': {'type': 'CURRENCY', 'pattern': "#,##0.00\" ₽\""}}},
            'fields': 'userEnteredFormat.numberFormat'
        }
        }
    )
    await wrapper_services.as_service_account(
        service.spreadsheets.batchUpdate(
            spreadsheetId=spreadsheetid, json={'requests': requests}
        )
    )