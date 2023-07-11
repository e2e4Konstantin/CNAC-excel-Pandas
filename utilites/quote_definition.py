from dataclasses import dataclass, field, fields


@dataclass
class Header:
    """Заголовок"""
    name_header: str = ""  # название
    column_header: int = 0  # номер колонки


@dataclass
class HeaderOption:
    """ Заголовок таблицы параметров """
    column_header_option: int = 0  # первая колонка заголовка параметров
    name_header_option: str = ""  # название таблицы параметров
    option_headers: list[Header] = field(default_factory=list)  # список заголовков параметров


@dataclass
class TableItem:
    """ Таблица """
    cod_table: str = ""  # код таблицы
    number_table: str = ""  # номер из названия
    name_table: str = ""  # название
    row_table: int = 0  # номер строки
    catalog_table: list[str] = field(default_factory=list)  # ссылки на каталог
    # attribute_headers
    attribute_table: list[Header] = field(default_factory=list)  # список заголовков атрибутов
    # options_headers
    options_table: list[HeaderOption] = field(default_factory=list)  # список заголовков параметров


@dataclass
class Attribute:
    """ Атрибут """
    name_attribute: str = ""
    value_attribute: str = ""


@dataclass
class Option:
    """ Параметр """
    name_option: str = ""
    value_option: list[tuple[str, str]] = field(default_factory=list)  # (название, значение)


@dataclass
class Quote:
    """ Расценка """
    row_quote: int = -1
    table_quote: str = ""
    cod_quote: str = ""
    name_quote: str = ""
    sizer_quote: str = ""
    statistics_quote: int = 0
    parameterized_quote: bool = False
    type_quote: str = ""
    parent_quote: str = ""

    attributes_quote: list[Attribute] = field(default_factory=list)
    options_quote: list[Option] = field(default_factory=list)

    def __str__(self):
        s = '; '.join(f'{x.name}={getattr(self, x.name)!r}' for x in fields(self))
        return f'{type(self).__name__}({s})'

    def short_str(self):
        s = f"{self.cod_quote}; {self.name_quote}; {self.table_quote}; {self.parameterized_quote}; " \
            f"{self.attributes_quote}; {self.options_quote};"
        return s
    # def csv_str(self):
    #     s = ';'.join(f'{getattr(self, x.name)!r}' for x in fields(self))
    #     return s
    def csv_list(self):
        return [getattr(self, x.name) for x in fields(self)]

QUOTE_TYPE: list[str] = ["основная", "дополнительная"]

tables: dict[str, TableItem] = dict()
quotes: list[Quote] = list()
heap: list[Quote] = list()
