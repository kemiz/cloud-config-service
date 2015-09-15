# #######
# Copyright (c) 2015 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.

import time
import os
import json
import sqlite3
from contextlib import contextmanager
from functools import wraps
from collections import namedtuple

from cloud_config_service.storage.base import Storage
from cloud_config_service import exceptions


class SQLiteSchema(object):
    Column = namedtuple('Column', 'name type')

    def __init__(self, primary_key_name, primary_key_type):
        self._primary_key_type = primary_key_type
        self._primary_key_name = primary_key_name
        self._columns = []

    def add_column(self, column_name, column_type):
        self._columns.append(self.Column(column_name, column_type))

    @property
    def primary_key_type(self):
        return self._primary_key_type

    @property
    def primary_key_name(self):
        return self._primary_key_name

    @property
    def wilds(self):
        return ', '.join(map(lambda column: '?', self._columns))

    def create(self):
        columns = ', '.join(
            ['{0} {1}'.format(column.name, column.type)
             for column in self._columns])
        return '({0} {1} PRIMARY KEY, {2})'.format(
            self.primary_key_name, self.primary_key_type, columns)


def blocking(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except sqlite3.OperationalError as e:
                if e.message != 'database is locked':
                    raise exceptions.StorageException(e.message)
                time.sleep(0.1)

    return wrapper


class SQLiteStorage(Storage):
    """
    Storage wrapper for SQLite DB implementing AbstractStorage interface.

    """

    def __init__(self, storage=None):
        if storage is None:
            storage = 'cloud-config-data.sqlite'
        print('Innit new SQLiteStorage with storage: {0}'.format(storage))
        self._filename = os.path.abspath(storage)
        self._create_table('aws')
        self._create_table('openstack')

    @contextmanager
    def connect(self, exclusive=False):
        print('Connecting to SQLite...')
        with sqlite3.connect(self._filename) as conn:
            conn.row_factory = _dict_row_factory
            if exclusive:
                conn.isolation_level = 'EXCLUSIVE'
                conn.execute('BEGIN EXCLUSIVE')
            yield conn.cursor()

    @blocking
    def get_clouds(self, provider, **filters):
        with self.connect() as cursor:
            if not filters:
                cursor.execute('SELECT * FROM {0}'.format(provider))
            else:
                sql_cond = _construct_and_query_sql(filters)
                values = _construct_values_tuple(filters)
                cursor.execute('SELECT * FROM {0} WHERE {1}'
                               .format(provider, sql_cond),
                               values)
            return list(cursor.fetchall())

    def add_cloud(self, cloud, provider):
        with self.connect() as cursor:
            column_names = cloud.keys()
            print(column_names)
            values = _construct_values_tuple(cloud)
            values_wild = get_schema(provider).wilds
            sql = 'INSERT INTO {0} ({1}) VALUES({2})'.format(
                provider,
                ', '.join(column_names),
                values_wild)
            print('Adding cloud config: {0}'.format(sql))
            cursor.execute(sql, values)
            cloud[get_schema(provider).primary_key_name] = cursor.lastrowid

    @blocking
    def update_cloud(self, global_id, new_values, provider, old_values=None):
        if old_values is None:
            old_values = {}
        with self.connect(exclusive=True) as cursor:
            sql_set = _construct_set_values_sql(new_values)
            old_values.update({'global_id': global_id})
            sql_con = _construct_and_query_sql(old_values)
            new = _construct_values_tuple(new_values)
            old = _construct_values_tuple(old_values)
            cursor.execute('UPDATE {0} SET {1} WHERE {2}'.format(
                provider, sql_set, sql_con), new + old)
            changed = cursor.connection.total_changes == 1
            cursor.execute('SELECT * FROM {0} WHERE {1}=?'
                           .format(provider,
                                   get_schema(provider).primary_key_name),
                           (global_id, ))
            return cursor.fetchone(), changed

    def _create_table(self, provider):
        with self.connect() as cursor:
            sql = 'CREATE TABLE IF NOT EXISTS {0} {1}'.format(
                provider, get_schema(provider).create())
            print('Creating table: {0}'.format(sql))
            cursor.execute(sql)


def get_schema(provider):
    print provider
    if provider == 'aws':
        return _get_aws_schema()
    elif provider == 'openstack':
        return _get_openstack_schema()
    else:
        raise exceptions.StorageException('Not a supported schema: {0}'.format(provider))


def _get_aws_schema():
    schema = SQLiteSchema(
        primary_key_name='global_id',
        primary_key_type='integer'
    )
    schema.add_column('name', 'text')
    schema.add_column('type', 'text')
    schema.add_column('aws_access_key_id', 'text')
    schema.add_column('aws_secret_access_key', 'text')
    schema.add_column('ec2_region_name', 'text')
    schema.add_column('use_external_resource', 'text')
    schema.add_column('resource_id', 'text')
    schema.add_column('parameters', 'text')
    print('Creating schema: {0}'.format(schema))
    return schema


def _get_openstack_schema():
    schema = SQLiteSchema(
        primary_key_name='global_id',
        primary_key_type='integer'
    )
    schema.add_column('name', 'text')
    schema.add_column('type', 'text')
    schema.add_column('username', 'text')
    schema.add_column('password', 'text')
    schema.add_column('tenant_name', 'text')
    schema.add_column('auth_url', 'text')
    schema.add_column('region', 'text')
    schema.add_column('nova_url', 'text')
    schema.add_column('neutron_url', 'text')
    print('Creating schema: {0}'.format(schema))
    return schema


def _dict_row_factory(cursor, row):
    def _normalize_port(value):
        try:
            return int(value)
        except ValueError:
            if isinstance(value, unicode):
                return str(value)
            if isinstance(value, str):
                return value
            raise

    custom_parsers = {
        'auth': json.loads,
        'port': _normalize_port,
        'alive': lambda v: v != 0,
        'reserved': lambda v: v != 0
    }

    result = {}
    for idx, col in enumerate(cursor.description):
        name = col[0]
        content = row[idx]
        if name in custom_parsers:
            result[name] = custom_parsers[name](content)
        else:
            result[name] = content
    return result


def _construct_set_values_sql(values):
    return ', '.join('{0}=?'.format(s) for s in values)


def _construct_and_query_sql(filters):
    return ' AND '.join('{0}{1}?'.format(
        f[0], ' is ' if f[1] is None else '=') for f in filters.iteritems())


def _construct_values_tuple(values):
    return tuple([json.dumps(f) if isinstance(f, dict) else f for f in
                  values.values()])
