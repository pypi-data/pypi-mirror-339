import os
import sqlite3
from typing import Type, Iterable, get_origin, Union, get_args
from jinja2 import Template
from contextlib import contextmanager
from .constants import SQL_TYPES, SQL_TYPE
from .sql_templates import (
    CREATE_TABLE_TEMPLATE,
    DELETE_BY_TEMPLATE,
    INSERT_TEMPLATE,
    FIND_BY_TEMPLATE,
    UPDATE_TEMPLATE,
)

DATABASE_PATH = os.environ.get("DATABASE_PATH", "db.db")

DEBUG = os.environ.get("LITEMODEL_DEBUG", False)
if DEBUG:
    print(f"DATABASE_PATH={DATABASE_PATH}")


class Field:
    def __init__(self, name: str, _type: SQL_TYPE) -> None:
        self.name = name
        self.type = _type

    @property
    def sqlite_type(self) -> str:
        if is_type_optional(self.type):
            for type_ in SQL_TYPES:
                if type_ == self.type_when_not_null:
                    return SQL_TYPES[type_]
        if issubclass(self.type, Model):
            return SQL_TYPES[int]
        return SQL_TYPES[self.type]

    @property
    def type_when_not_null(self) -> Type:
        if not is_type_optional(self.type):
            return self.type
        for arg in get_args(self.type):
            if arg is not type(None):
                return arg

    def get_value(self, value: str) -> SQL_TYPE:
        if issubclass(self.type_when_not_null, Model):
            if value.isdigit():
                # handles case where inserting the foreign key by int instead of
                # an entire model
                return int(value)
            return value.id
        if DEBUG:
            print(f"{self.type=}")
            print(f"{value=}")
        if self.type is bool and value is None:
            return False
        return value

    def __set__(self, instance, value):
        if issubclass(self.type_when_not_null, Model) and isinstance(value, int):
            value = self.type.find(value)
        instance._values[self.name] = value

    def __get__(self, instance, cls):
        if instance:
            return instance._values.get(self.name)
        else:
            return self

    def __str__(self) -> str:
        return f"{self.name}: {self.type}"

    def __repr__(self) -> str:
        return f"{self.name}: {self.type}"


class Model:
    def __init__(self, **kwargs) -> None:
        self._values = {"id": None}
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init_subclass__(cls) -> None:
        cls.set_table_name()
        cls.set_fields()
        cls.set_cls_attributes()

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} %s>" % " ".join(
            f"{name}={getattr(self, name)!r}" for name in self._fields
        )

    @classmethod
    def set_table_name(cls) -> None:
        name = cls.__name__
        cls._name = "".join(
            ["_" + c.lower() if c.isupper() else c for c in name]
        ).lstrip("_")

    @classmethod
    def set_fields(cls) -> None:
        cls._fields = {
            name: Field(name, _type) for name, _type in cls.__annotations__.items()
        }

    @classmethod
    def get_field(cls, name) -> Field | None:
        for name, field in cls._fields.items():
            if field.name == name:
                return field
        return None

    @classmethod
    def set_cls_attributes(cls) -> None:
        for name, field in cls._fields.items():
            setattr(cls, name, field)
        setattr(cls, "id", Field("id", int))

    @classmethod
    def create_table(cls, delete_if_exists: bool = False) -> None:
        if delete_if_exists:
            cls.delete_table()
        template = Template(CREATE_TABLE_TEMPLATE)
        not_null = {}
        for x, y in cls._fields.items():
            not_null[x] = "" if is_type_optional(y.type) else " NOT NULL"
        sql_statement = template.render(
            {"table": cls._name, "fields": cls._fields, "not_null": not_null}
        )
        sql_run(sql_statement)

    @classmethod
    def delete_table(cls) -> None:
        sql_statement = f"DROP TABLE IF EXISTS {cls._name}"
        sql_run(sql_statement)

    @classmethod
    def find_by(cls, field_name: str, value: SQL_TYPE):
        template = Template(FIND_BY_TEMPLATE)
        sql_statement = template.render({"table": cls._name, "field": field_name})
        results = sql_select(sql_statement, (value,))
        return map_objects(cls, results, many=False)

    @classmethod
    def find_many(cls, field_name: str, value: SQL_TYPE):
        template = Template(FIND_BY_TEMPLATE)
        sql_statement = template.render({"table": cls._name, "field": field_name})
        results = sql_select(sql_statement, (value,))
        return map_objects(cls, results, many=True)

    @classmethod
    def find(cls, id: int):
        return cls.find_by("id", id)

    @classmethod
    def delete_by(cls, field_name: str, value: SQL_TYPE):
        template = Template(DELETE_BY_TEMPLATE)
        sql_statement = template.render({"table": cls._name, "field": field_name})
        sql_run(sql_statement, (value,))

    @classmethod
    def all(cls):
        sql_statement = f"SELECT * from {cls._name}"
        rows = sql_select(sql_statement)
        return map_objects(cls, rows, many=True)

    @property
    def fields(self) -> dict:
        return self.__class__._fields

    @property
    def table(self) -> str:
        return self.__class__._name

    def save(self):
        if self.id:
            return self._update()
        return self._insert()

    def delete(self) -> None:
        template = Template(DELETE_BY_TEMPLATE)
        sql_statement = template.render({"table": self.table, "field": "id"})
        sql_run(sql_statement, (self.id,))

    def _insert(self) -> None:
        template = Template(INSERT_TEMPLATE)
        field_keys = self.fields.keys()
        sql_statement = template.render({"table": self.table, "fields": field_keys})
        values = self._get_field_values(field_keys)
        if DEBUG:
            print(f"{sql_statement=}")
            print(f"{values=}")
        self.id = sql_run(sql_statement, values)

    def _update(self) -> None:
        template = Template(UPDATE_TEMPLATE)
        field_keys = self.fields.keys()
        sql_statement = template.render(
            {"table": self.table, "fields": field_keys, "where": "id"}
        )
        values = self._get_field_values(field_keys)
        values.append(self.id)
        sql_run(sql_statement, values)

    def _get_field_values(self, field_keys: Iterable) -> list[SQL_TYPE]:
        values = []
        for key in field_keys:
            field: Field = self.fields[key]
            value = field.get_value(getattr(self, field.name))
            if value is None:
                if field.type is int:
                    value = 0
                if field.type is bool:
                    value = False
            values.append(value)
        return values


@contextmanager
def transaction(conn: sqlite3.Connection):
    # We must issue a "BEGIN" explicitly when running in auto-commit mode.
    conn.execute("BEGIN IMMEDIATE TRANSACTION")
    try:
        # Yield control back to the caller.
        yield
    except:
        conn.rollback()  # Roll back all changes if an exception occurs.
        raise
    else:
        conn.commit()


def get_conn() -> sqlite3.Connection:
    CONNECTION = sqlite3.connect(
        DATABASE_PATH, timeout=5, detect_types=1, isolation_level=None
    )
    # CONNECTION.row_factory = sqlite3.Row
    return CONNECTION


def sql_run(sql_statement: str, values: Iterable | None = None):
    with get_conn() as db:
        db.row_factory = sqlite3.Row
        cursor = db.execute(sql_statement, values)
        db.commit()
    return cursor.lastrowid


def sql_select(sql_statement: str, values: Iterable | None = None):
    print(sql_statement)
    print(values)
    with get_conn() as db:
        print(db)
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute(sql_statement, values or {})
        rows = cur.fetchall()
        print(f"{rows}")
    return rows


def has_foreign_value(field: Field, column: str) -> bool:
    if column == "id":
        return False
    if issubclass(field.type_when_not_null, Model):
        return True
    return False


def map_object(cls, **row):
    """Maps an object to the subclass of model, queries for foreign keys"""
    # This can't be done in __init__ (Model) or __set__ (Field) because
    # if we get a foreign key we need to reach out to db and get it
    # This would be an async call and these methods do not support async
    # So this initializes an instance of Model (subclasses) with foreign keys
    instance = cls()  # __init__ Model with no kwargs
    for column, value in row.items():
        field: Field = cls.get_field(column)
        if has_foreign_value(field, column):
            # field.type: Model
            value = field.type.find(value)  # query foreign model
        setattr(instance, column, value)
    return instance


def map_objects(cls, rows, many: bool = False):
    """Maps objects to the subclass of model, queries for foreign keys"""
    if many:
        objects = []
        for row in rows:
            obj = map_object(cls, **dict(row))
            objects.append(obj)
        return objects
    try:
        row = next(iter(rows))
    except StopIteration:
        return None
    return map_object(cls, **dict(row))


def is_type_optional(type_: Type) -> bool:
    return get_origin(type_) is Union and type(None) in get_args(type_)
