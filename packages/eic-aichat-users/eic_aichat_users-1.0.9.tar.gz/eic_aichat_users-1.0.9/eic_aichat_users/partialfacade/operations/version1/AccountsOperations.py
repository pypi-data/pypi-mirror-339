# -*- coding: utf-8 -*-
import json

import bottle
from pip_services4_commons.convert import TypeCode
from pip_services4_components.refer import Descriptor, IReferences
from pip_services4_data.validate import ObjectSchema
from pip_services4_http.controller import RestOperations, RestController
from pip_services4_components.context import Context

from eic_aichat_users.accounts.data import AccountV1, AccountV1Schema
from eic_aichat_users.accounts.logic.IAccountsService import IAccountsService


class AccountsOperations(RestOperations):
    def __init__(self):
        super().__init__()
        self._accounts_service: IAccountsService = None
        self._dependency_resolver.put("accounts-service", Descriptor('aichatusers-accounts', 'service', '*', '*', '1.0'))

    def configure(self, config):
        super().configure(config)

    def set_references(self, references: IReferences):
        super().set_references(references)
        self._accounts_service = self._dependency_resolver.get_one_required('accounts-service')

    def get_accounts(self):
        context = Context.from_trace_id(self._get_trace_id())
        filter_params = self._get_filter_params()
        paging_params = self._get_paging_params()
        try:
            res = self._accounts_service.get_accounts(context, filter_params, paging_params)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def get_account_by_id(self, id):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            res = self._accounts_service.get_account_by_id(context, id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def get_account_by_login(self, login):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            res = self._accounts_service.get_account_by_login(context, login)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def get_account_by_id_or_login(self, id_or_login):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            res = self._accounts_service.get_account_by_id_or_login(context, id_or_login)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def create_account(self):
        context = Context.from_trace_id(self._get_trace_id())
        data = bottle.request.json
        account = data if isinstance(data, dict) else json.loads(data)
        account = None if not account else AccountV1(**account)
        try:
            res = self._accounts_service.create_account(context, account)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def update_account(self):
        context = Context.from_trace_id(self._get_trace_id())
        data = bottle.request.json
        account = data if isinstance(data, dict) else json.loads(data)
        account = None if not account else AccountV1(**account)
        try:
            res = self._accounts_service.update_account(context, account)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def delete_account_by_id(self, id):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            res = self._accounts_service.delete_account_by_id(context, id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def drop_account_by_id(self, id):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            res = self._accounts_service.drop_account_by_id(context, id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def register_routes(self, controller: RestController):
        controller.register_route('get', '/users', None, self.get_accounts)

        controller.register_route('get', '/users/<id>', ObjectSchema(True)
                                  .with_optional_property("id", TypeCode.String),
                                  self.get_account_by_id)

        controller.register_route('get', '/accounts/by_login/<login>', ObjectSchema(True)
                                  .with_optional_property("login", TypeCode.String),
                                  self.get_account_by_login)

        controller.register_route('get', '/accounts/by_id_or_login/<id_or_login>', ObjectSchema(True)
                                  .with_optional_property("id_or_login", TypeCode.String),
                                  self.get_account_by_id_or_login)

        controller.register_route('post', '/users', ObjectSchema(True)
                                  .with_required_property("body", AccountV1Schema()),
                                  self.create_account)

        controller.register_route('put', '/users', ObjectSchema(True)
                                  .with_required_property("body", AccountV1Schema()),
                                  self.update_account)

        controller.register_route('delete', '/users/<id>', ObjectSchema(True)
                                  .with_required_property("id", TypeCode.String),
                                  self.delete_account_by_id)

        controller.register_route('delete', '/users/<id>/drop', ObjectSchema(True)
                                  .with_required_property("id", TypeCode.String),
                                  self.drop_account_by_id)
