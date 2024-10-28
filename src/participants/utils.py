import re


async def format_filename(filename: str) -> str:
    """
    Remove invalid characters from the file name
    """
    # оставляем только буквы, цифры, подчеркивания, дефисы и точки, заменяем пробелы на нижнее подчеркивание
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename).replace(' ', '_')
