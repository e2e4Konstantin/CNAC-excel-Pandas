import os
import sys
import re
import pandas

STRONG_MATCH = True
SOFT_MATCH = False

pattern_rulls = {
    "B": (re.compile(r"\d+"), STRONG_MATCH),  # 3
    "C": (re.compile(r"\d+\.\d+"), STRONG_MATCH),  # 3.6
    "D": (re.compile(r"\d+\.\d+(-\d+){1}"), STRONG_MATCH),  # 3.6-1
    "E": (re.compile(r"\d+\.\d+(-\d+){2}"), STRONG_MATCH),  # 3.6-1-1
    "F": (re.compile(r"\d+\.\d+(-\d+){4}"), STRONG_MATCH),  # 3.6-1-1-0-1
    "G": (re.compile(r"^\s*$"), STRONG_MATCH),  # пустая строка
    "H": (re.compile(r"Таблица \d+\.\d+-\d+\."), SOFT_MATCH),
    "L": (re.compile(r"Дополнительные расценки"), STRONG_MATCH),
    "O": (re.compile(r"Атрибуты"), STRONG_MATCH),
}


class Stuff:
    def __init__(self, *args, **kwargs):
        self.test_points = pattern_rulls
        self.column_number = {}
        self.column_number_generate()

    def column_number_generate(self):
        alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        alphabet.extend([alphabet[0] + v for v in alphabet])
        lc_alphabet = list('abcdefghijklmnopqrstuvwxyz')
        lc_alphabet.extend([lc_alphabet[0] + v for v in lc_alphabet])
        self.column_number = {v: i for i, v in enumerate(alphabet)}
        self.column_number.update({v: i for i, v in enumerate(lc_alphabet)})

    def get_column_number(self, column_name: str) -> int | None:
        """Возвращает номер столбца по букве"""
        return self.column_number.get(column_name, None)


class SourceData(Stuff):
    def __init__(self, file_name, file_path, sheet_name):
        super().__init__()
        self.file_name = file_name
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.full_path = None
        self.df: pandas.DataFrame()

        self.row_max = 0
        self.column_max = 0
        self.get_full_name()
        self.get_data()

    def get_full_name(self):
        fullpath = os.path.abspath(os.path.join(self.file_path, self.file_name, ))
        self.full_path = fullpath if os.path.exists(fullpath) else None
        if not self.full_path:
            print(f"--> Не найден фйл: '{self.file_name}' в папке: '{self.file_path}'")
            sys.exit()

    def get_data(self):
        try:
            if self.full_path:
                self.df = pandas.read_excel(self.full_path, sheet_name=self.sheet_name, header=None, dtype="object")
                if not self.df.empty:
                    self.row_max = self.df.shape[0]
                    self.column_max = self.df.shape[1]
                else:
                    raise TypeError(self.__class__)
        except Exception as err:
            print(f"\tget_data --> {err}")
            sys.exit()

    def __str__(self):
        return f"файл: {self.full_path}\nтаблица: {self.sheet_name}', строк: {self.row_max + 1}, столбцов: {self.column_max + 1}\n" \
               f"pandas.version: {pandas.__version__} \n{self.df}"  #

    def get_cell_str_value(self, row, column) -> str:
        # value: str = "" if pd.isnull(tmp_val) else tmp_val
        if row >= 0 and column >= 0:
            src_value = self.df.iat[row, column]
            if pandas.isna(src_value):
                return ""
            match src_value:
                case int() | float():
                    return str(src_value)
                case str():
                    return " ".join(src_value.split())
                case _:
                    return str(src_value or "").strip()
        return ""
