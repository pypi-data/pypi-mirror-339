# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1741516804.0291262
_enable_loop = True
_template_filename = 'd:/projekte/studlis/studlis/studlis/webui/pages/login.html'
_template_uri = 'pages/login.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer('\r\n    <style>\r\n        .login-box {\r\n            max-width: 400px;\r\n            margin: 50px auto;\r\n            padding: 30px;\r\n            border: 1px solid #ddd;\r\n            border-radius: 10px;\r\n            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);\r\n        }\r\n        .login-box .form-group {\r\n            position: relative;\r\n        }\r\n        .login-box .form-group .fa {\r\n            position: absolute;\r\n            top: 50%;\r\n            left: 10px;\r\n            transform: translateY(-50%);\r\n        }\r\n        .login-box .form-control {\r\n            padding-left: 30px;\r\n        }\r\n    </style>\r\n<template tpl_id="login_box">\r\n    <div class="login-box">\r\n        <h2 class="text-center">Login</h2>\r\n            <div class="form-group">\r\n                <i class="fa fa-user"></i>\r\n                <input type="text" id="user" class="form-control" placeholder="Username" required>\r\n            </div>\r\n            <div class="form-group mt-1">\r\n                <i class="fa fa-lock"></i>\r\n                <input type="password"  id="pwd" class="form-control" placeholder="Password">\r\n            </div>\r\n            <button class="btn btn-primary btn-block mt-1" onclick="page_login.login();">Login</button>\r\n    </div>\r\n</template>\r\n<script>\r\n    var page_login = {\r\n        show: function() {\r\n            $(\'#main-view-content\').tpl(\'login_box\');\r\n        },\r\n        login: function(){\r\n            var username = $(\'#user\').val();\r\n            var password = $(\'#pwd\').val();\r\n            DoRequest("login",{"username":username,"password":password},function(data){\r\n                if(data.value.username){\r\n                    sessionStorage.setItem("token",data.value.token);\r\n                    sessionStorage.setItem("username",data.value.username);\r\n                    session_token = data.value.token;\r\n                    \r\n                    $("#loginbutton").addClass("d-none");\r\n                    loggedin=true;\r\n                    page_select_project.show();\r\n                }\r\n            });\r\n        }\r\n    }\r\n\r\n    var loggedin=false;\r\n    session_permission_groups="";\r\n    var session_token = sessionStorage.getItem("token");\r\n\r\n    $(function(){\r\n        if (session_token){\r\n            DoRequest("check_login",{"token":session_token},function(data){\r\n                if(data.value.username){\r\n                    \r\n                    $("#loginbutton").addClass("d-none");\r\n                    loggedin=true;\r\n                    page_select_project.show();\r\n                }else{\r\n                    page_login.show();\r\n                }\r\n            });\r\n            \r\n        }else {\r\n            page_login.show();\r\n        }\r\n\r\n    });\r\n\r\n\r\n</script>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "d:/projekte/studlis/studlis/studlis/webui/pages/login.html", "uri": "pages/login.html", "source_encoding": "utf-8", "line_map": {"16": 0, "21": 1, "27": 21}}
__M_END_METADATA
"""
