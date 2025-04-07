# encoding: utf-8
import logging
import queue

import pymysql

if pymysql.version_info >= (1, ):
    from pymysql.converters import escape_string
else:
    from pymysql import escape_string


logger = logging.getLogger('sql_gen')


class GenSqlManager:

    @classmethod
    def get_real_table_name(cls, table_name, schema_name=None):
        return f'`{schema_name}`.`{table_name}`' if schema_name else f'`{table_name}`'

    @classmethod
    def gen_insert_head(cls, table_name, field_list, schema_name=None, insert_type='INSERT INTO'):
        return "%s %s (%s) VALUES \n" % (
            insert_type,
            cls.get_real_table_name(table_name, schema_name),
            ",".join(["`%s`" % field for field in field_list])
        )

    @classmethod
    def gen_insert_head_tail(
        cls, table_name, field_list, schema_name=None, insert_type='INSERT INTO', on_duplicate_key_update_fields=()
    ):
        sql_tail_list = []
        new_data_flag = '__new_data__'
        if on_duplicate_key_update_fields:
            for on_duplicate_key_update_field in on_duplicate_key_update_fields:
                if not isinstance(on_duplicate_key_update_field, (list, tuple)):
                    from_field = on_duplicate_key_update_field
                    to_field = from_field
                else:
                    assert len(on_duplicate_key_update_field) == 2
                    from_field, to_field = on_duplicate_key_update_field
                if from_field in field_list:
                    from_field = f"`{from_field}`"
                if not isinstance(to_field, (list, tuple)):
                    to_field = (to_field, )
                to_fields = list()
                for field in to_field:
                    if field in field_list:
                        field = f'{new_data_flag}.`{field}`'
                    to_fields.append(field)
                sql_tail_list.append(f"{from_field}={' '.join(to_fields)}")
        sql_tail = ''
        if sql_tail_list:
            sql_tail = f'\nAS {new_data_flag} ON DUPLICATE KEY UPDATE {",".join(sql_tail_list)}'
        sql_head = cls.gen_insert_head(
            table_name=table_name, field_list=field_list, schema_name=schema_name, insert_type=insert_type
        )
        return sql_head, sql_tail

    @classmethod
    def escape_string(cls, value):
        if value is None:
            return "NULL"
        elif isinstance(value, int):
            return str(value)
        else:
            return "'%s'" % escape_string(str(value))

    @classmethod
    def gen_item_sql(cls, item, field_list, field_default):
        return "(%s)" % ",".join([
            cls.get_item_value(item, field, field_default, escape=True)
            for field in field_list
        ])

    @classmethod
    def get_item_value(cls, item, field, field_default, escape, default_value=None):
        data = item.get(field, field_default.get(field, default_value))
        if escape:
            data = cls.escape_string(data)
        return data

    @classmethod
    def gen_items_sql(
        cls,
        items,
        *,
        table_name,
        field_list,
        field_default,
        max_sql_size=None,
        schema_name=None,
        insert_type='INSERT INTO',
        on_duplicate_key_update_fields=()
    ):
        sql_head, sql_tail = cls.gen_insert_head_tail(
            table_name,
            field_list,
            schema_name=schema_name,
            insert_type=insert_type,
            on_duplicate_key_update_fields=on_duplicate_key_update_fields
        )
        sql = ""
        for item in items:
            add_sql = GenSqlManager.gen_item_sql(item, field_list, field_default)
            if max_sql_size is not None and len(sql) + len(add_sql) > max_sql_size:
                sql += " " + sql_tail
                yield sql
                sql = ""
            if sql:
                sql += ",\n"
            else:
                sql = sql_head
            sql += add_sql
        if sql:
            sql += " " + sql_tail
            yield sql


class GenSqlBase(GenSqlManager):
    SCHEMA_NAME = None
    TABLE_NAME = None
    FIELD_LIST = ()
    FIELD_DEFAULT = {}
    MT_MPSC = False

    def __init__(self):
        self.items = queue.Queue()

    def add_item(self, **item):
        self.items.put_nowait(item)
        return item

    def finish(self):
        self.items.put_nowait(None)

    def items_iter(self):
        while True:
            item = self.items.get()
            if item is None:
                break
            yield item

    def gen_sql(self, max_sql_size=1024 * 1024, insert_type='INSERT INTO', on_duplicate_key_update_fields=()):
        if not self.MT_MPSC:
            self.finish()
        return self.gen_items_sql(
            self.items_iter(),
            table_name=self.TABLE_NAME,
            field_list=self.FIELD_LIST,
            field_default=self.FIELD_DEFAULT,
            max_sql_size=max_sql_size,
            schema_name=self.SCHEMA_NAME,
            insert_type=insert_type,
            on_duplicate_key_update_fields=on_duplicate_key_update_fields
        )


class GenSqlUniqueCheck(GenSqlBase):
    UNIQUE_FIELDS = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unique_indexes = {}
        for key in self.get_unique_fields():
            key = self.gen_keys(key)
            assert key not in self.unique_indexes
            for k in key:
                assert k in self.FIELD_LIST
            self.unique_indexes[key] = dict()

    @classmethod
    def gen_keys(cls, keys):
        if not isinstance(keys, (tuple, list)):
            keys = [keys]
        return tuple(keys)

    def on_dup(self, item, dup_items):
        pass

    def find_by_unique(self, key, detail_key):
        key = self.gen_keys(key)
        detail_key = self.gen_keys(detail_key)
        assert key in self.get_unique_fields()
        return self.unique_indexes[key].get(detail_key)

    @classmethod
    def get_unique_fields(cls):
        return cls.UNIQUE_FIELDS

    def add_item(self, **item):
        dup_items = dict()
        dup_keys = dict()
        for key in self.get_unique_fields():
            key = self.gen_keys(key)
            detail_key = self.gen_keys([self.get_item_value(item, k, self.FIELD_DEFAULT, False) for k in key])
            dup_keys[key] = detail_key
            if detail_key in self.unique_indexes[key]:
                dup_items[key] = self.unique_indexes[key][detail_key]
        if dup_items:
            return self.on_dup(item, dup_items)
        ret = super().add_item(**item)
        for key, detail_key in dup_keys.items():
            self.unique_indexes[key][detail_key] = ret
        return ret


class GenSqlAutoId(GenSqlUniqueCheck):
    PK_FILED = 'id'
    UNIQUE_FIELDS = ('id', )
    GEN_ID_KEY = '__GEN_ID__'

    def __init__(self, next_id=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_id = next_id
        assert self.PK_FILED in self.FIELD_LIST

    def get_unique_fields(self):
        if self.PK_FILED not in self.UNIQUE_FIELDS:
            return self.UNIQUE_FIELDS + (self.PK_FILED, )
        return self.UNIQUE_FIELDS

    def get_by_pk(self, pk):
        return self.find_by_unique(self.PK_FILED, pk)

    def on_dup(self, item, dup_items):
        if item.get(self.GEN_ID_KEY):
            self.next_id -= 1

    def add_item(self, **item):
        if self.PK_FILED not in item:
            item[self.PK_FILED] = self.next_id
            self.next_id += 1
            item[self.GEN_ID_KEY] = True
        ret = super().add_item(**item)
        ret.pop(self.GEN_ID_KEY, None)
        return ret
