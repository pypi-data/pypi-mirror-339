# -*- coding: utf-8 -*-
import json
import bottle

from typing import Optional, Any
from pip_services4_components.refer import Descriptor, IReferences
from pip_services4_http.controller import RestOperations, RestController
from pip_services4_components.context import Context
from pip_services4_commons.convert import TypeCode
from pip_services4_data.validate import ObjectSchema

from eic_aichat_users.sessions.data import SessionV1
from eic_aichat_users.sessions.data.SessionV1Schema import SessionV1Schema
from eic_aichat_users.sessions.logic.ISessionsService import ISessionsService


class SessionsOperations(RestOperations):
    def __init__(self):
        super().__init__()
        self._service: ISessionsService = None
        self._dependency_resolver.put("sessions-service", Descriptor("aichatusers-sessions", "service", "*", "*", "1.0"))

    def configure(self, config):
        super().configure(config)

    def set_references(self, references: IReferences):
        super().set_references(references)
        self._service = self._dependency_resolver.get_one_required("sessions-service")

    def get_sessions(self):
        context = Context.from_trace_id(self._get_trace_id())
        filter_params = self._get_filter_params()
        paging_params = self._get_paging_params()
        try:
            res = self._service.get_sessions(context, filter_params, paging_params)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def get_session_by_id(self, session_id):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            res = self._service.get_session_by_id(context, session_id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def open_session(self):
        context = Context.from_trace_id(self._get_trace_id())
        data = bottle.request.json or {}
        try:
            res = self._service.open_session(
                context,
                data.get("user_id"),
                data.get("user_name"),
                data.get("address"),
                data.get("client"),
                data.get("user"),
                data.get("data"),
            )
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def store_session_data(self, session_id):
        context = Context.from_trace_id(self._get_trace_id())
        data = bottle.request.json or {}
        try:
            res = self._service.store_session_data(context, session_id, data)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def update_session_user(self, session_id):
        context = Context.from_trace_id(self._get_trace_id())
        data = bottle.request.json or {}
        try:
            res = self._service.update_session_user(context, session_id, data)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def close_session(self, session_id):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            res = self._service.close_session(context, session_id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def delete_session_by_id(self, session_id):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            res = self._service.delete_session_by_id(context, session_id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def close_expired_sessions(self):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            self._service.close_expired_sessions(context)
            return self._send_empty_result()
        except Exception as err:
            return self._send_error(err)

    def register_routes(self, controller: RestController):
        controller.register_route("get", "/sessions", None, self.get_sessions)

        controller.register_route("get", "/sessions/<session_id>", ObjectSchema(True)
                                  .with_required_property("session_id", TypeCode.String),
                                  self.get_session_by_id)

        controller.register_route("post", "/sessions/open", ObjectSchema(True)
                                  .with_required_property("user_id", TypeCode.String)
                                  .with_required_property("user_name", TypeCode.String),
                                  self.open_session)

        controller.register_route("post", "/sessions/<session_id>/data", ObjectSchema(True)
                                  .with_required_property("session_id", TypeCode.String),
                                  self.store_session_data)

        controller.register_route("post", "/sessions/<session_id>/user", ObjectSchema(True)
                                  .with_required_property("session_id", TypeCode.String),
                                  self.update_session_user)

        controller.register_route("post", "/sessions/<session_id>/close", ObjectSchema(True)
                                  .with_required_property("session_id", TypeCode.String),
                                  self.close_session)

        controller.register_route("delete", "/sessions/<session_id>", ObjectSchema(True)
                                  .with_required_property("session_id", TypeCode.String),
                                  self.delete_session_by_id)

        controller.register_route("post", "/sessions/cleanup", None, self.close_expired_sessions)
