from dataclasses import dataclass, field


@dataclass
class Header:
    """Заголовок"""
    name_header: str = ""   # название
    column_header: int = 0  # номер колонки


@dataclass
class HeaderOption:
    """ Заголовок таблицы параметров """
    column_header_option: int = 0                               # первая колонка заголовка параметров
    name_header_option: str = ""                                # название таблицы параметров
    option_headers: list[Header] = field(default_factory=list)  # список заголовков параметров


@dataclass
class TableItem:
    """ Таблица """
    cod_table: str = ""                                                 # код таблицы
    number_table: str = ""                                              # номер из названия
    name_table: str = ""                                                # название
    row_table: int = 0                                                  # номер строки
    catalog: list[str] = field(default_factory=list)                    # ссылки на каталог
    attribute_headers: list[Header] = field(default_factory=list)       # список заголовков атрибутов
    options_headers: list[HeaderOption] = field(default_factory=list)   # список заголовков параметров


@dataclass
class Attribute:
    name_attribute: str = ""
    value_attribute: str = ""


tables: dict[str, TableItem] = dict()
