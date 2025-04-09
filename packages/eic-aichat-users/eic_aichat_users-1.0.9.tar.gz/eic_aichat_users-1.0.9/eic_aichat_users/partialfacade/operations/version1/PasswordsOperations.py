# -*- coding: utf-8 -*-
from pip_services4_commons.convert import TypeCode
from pip_services4_components.refer import Descriptor, IReferences
from pip_services4_data.validate import ObjectSchema
from pip_services4_http.controller import RestOperations, RestController
from pip_services4_components.context import Context
import bottle

from eic_aichat_users.passwords.logic.IPasswordsService import IPasswordsService

class PasswordsOperations(RestOperations):
    def __init__(self):
        super().__init__()
        self._passwords_service: IPasswordsService = None
        self._dependency_resolver.put("passwords-service", Descriptor('aichatusers-passwords', 'service', '*', '*', '1.0'))

    def configure(self, config):
        super().configure(config)

    def set_references(self, references: IReferences):
        super().set_references(references)
        self._passwords_service = self._dependency_resolver.get_one_required('passwords-service') 

    def get_password_info(self, user_id: str):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            res = self._passwords_service.get_password_info(context, user_id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)
        
    def validate_password(self, password: str):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            res = self._passwords_service.validate_password(context, password)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def validate_password_for_user(self, user_id: str, password: str):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            res = self._passwords_service.validate_password_for_user(context, user_id, password)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)
        
    def set_password(self, user_id: str, password: str):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            res = self._passwords_service.set_password(context, user_id, password)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)    
        
    def set_temp_password(self, user_id: str):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            res = self._passwords_service.set_temp_password(context, user_id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)    
        
    def delete_password(self, user_id: str):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            res = self._passwords_service.delete_password(context, user_id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)    

    def authenticate(self, user_id: str, password: str):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            res = self._passwords_service.authenticate(context, user_id, password)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)    
        
    def change_password(self, user_id: str):
        context = Context.from_trace_id(self._get_trace_id())
        data = bottle.request.json or {}
        try:
            res = self._passwords_service.change_password(
                context, 
                user_id, 
                data.get("old_password"), 
                data.get("new_password")
                )
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)    
        
    def validate_code(self, user_id: str, code: str):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            res = self._passwords_service.validate_code(context, user_id, code)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)  
        
    def reset_password(self, user_id: str):
        context = Context.from_trace_id(self._get_trace_id())
        data = bottle.request.json or {}
        try:
            res = self._passwords_service.reset_password(
                context, 
                user_id, 
                data.get("code"), 
                data.get("password")
                )
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)  
        
    def recover_password(self, user_id: str):
        context = Context.from_trace_id(self._get_trace_id())
        try:
            res = self._passwords_service.recover_password(context, user_id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)   
        
    def register_routes(self, controller: RestController):

        controller.register_route('put', 'users/<user_id>/passwords', ObjectSchema(True)
                                  .with_required_property("user_id", TypeCode.String)
                                  .with_required_property("body", TypeCode.Map),
                                  self.change_password)

        controller.register_route('post', 'users/<user_id>/passwords/reset', ObjectSchema(True)
                                  .with_required_property("user_id", TypeCode.String)
                                  .with_required_property("body", TypeCode.Map),
                                  self.reset_password)
        
        controller.register_route('get', 'users/<user_id>/passwords/recover', ObjectSchema(True)
                                  .with_required_property("user_id", TypeCode.String),
                                  self.recover_password)


        