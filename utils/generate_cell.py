from settings import COLORS


def generate_cell(
        str_value: str | int, color: dict = COLORS.get('w'), h_a: str = 'CENTER', is_bold: bool = False,
        font_size: int = 10, value_type: str = 'string', borders: dict = None, font_family: str = 'Arial',
):
    cell_format = {
        'horizontalAlignment': h_a,
        'verticalAlignment': 'MIDDLE',
        'textFormat': {'bold': is_bold, 'fontSize': font_size},
        'backgroundColor': color
    }
    if borders:
        cell_format['borders'] = borders
    return {
        'userEnteredValue': {f'{value_type}Value': str_value},
        'userEnteredFormat': cell_format
    }

