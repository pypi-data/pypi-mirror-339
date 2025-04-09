# -*- coding: utf-8 -*-
import json
import bottle
from typing import List

from pip_services4_commons.convert import TypeCode
from pip_services4_components.refer import Descriptor, IReferences
from pip_services4_data.validate import ObjectSchema
from pip_services4_http.controller import RestOperations, RestController
from pip_services4_components.context import Context

from eic_aichat_users.roles.logic.IRolesService import IRolesService
from eic_aichat_users.roles.data import UserRolesV1


class RolesOperations(RestOperations):
    def __init__(self):
        super().__init__()
        self._roles_service: IRolesService = None
        self._dependency_resolver.put("roles-service", Descriptor('aichatusers-roles', 'service', '*', '*', '1.0'))

    def configure(self, config):
        super().configure(config)

    def set_references(self, references: IReferences):
        super().set_references(references)
        self._roles_service = self._dependency_resolver.get_one_required("roles-service")

    def get_roles_by_filter(self):
        context = Context.from_trace_id(self._get_trace_id())
        filter_params = self._get_filter_params()
        paging_params = self._get_paging_params()
        try:
            res = self._roles_service.get_roles_by_filter(context, filter_params, paging_params)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def get_roles_by_id(self, user_id):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            res = self._roles_service.get_roles_by_id(context, user_id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def set_roles(self, user_id):
        context = Context.from_trace_id(self._get_trace_id())
        data = bottle.request.json or []
        try:
            res = self._roles_service.set_roles(context, user_id, data)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def grant_roles(self, user_id):
        context = Context.from_trace_id(self._get_trace_id())
        data = bottle.request.json or []
        try:
            res = self._roles_service.grant_roles(context, user_id, data)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def revoke_roles(self, user_id):
        context = Context.from_trace_id(self._get_trace_id())
        data = bottle.request.json or []
        try:
            res = self._roles_service.revoke_roles(context, user_id, data)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def authorize(self, user_id):
        context = Context.from_trace_id(self._get_trace_id())
        data = bottle.request.json or []
        try:
            res = self._roles_service.authorize(context, user_id, data)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def register_routes(self, controller: RestController):
        controller.register_route('get', '/roles', None, self.get_roles_by_filter)

        controller.register_route('get', '/roles/<user_id>', ObjectSchema(True)
                                  .with_required_property("user_id", TypeCode.String),
                                  self.get_roles_by_id)

        controller.register_route('post', '/roles/<user_id>/set', ObjectSchema(True)
                                  .with_required_property("user_id", TypeCode.String)
                                  .with_required_property("body", TypeCode.Array),
                                  self.set_roles)

        controller.register_route('post', '/roles/<user_id>/grant', ObjectSchema(True)
                                  .with_required_property("user_id", TypeCode.String)
                                  .with_required_property("body", TypeCode.Array),
                                  self.grant_roles)

        controller.register_route('post', '/roles/<user_id>/revoke', ObjectSchema(True)
                                  .with_required_property("user_id", TypeCode.String)
                                  .with_required_property("body", TypeCode.Array),
                                  self.revoke_roles)

        controller.register_route('post', '/roles/<user_id>/authorize', ObjectSchema(True)
                                  .with_required_property("user_id", TypeCode.String)
                                  .with_required_property("body", TypeCode.Array),
                                  self.authorize)
