# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1741518626.6328797
_enable_loop = True
_template_filename = 'd:/projekte/studlis/studlis/studlis/webui/pages/project_overview.html'
_template_uri = 'pages/project_overview.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer('\r\n<template tpl_id="project_overview">\r\n    <div class="project-overview">\r\n        <h2>Project Übersicht</h2>\r\n    </div>\r\n</template>\r\n<script>\r\n    page_project_overview = {};\r\n    page_project_overview.show = function () {\r\n        node = $("#main-view-content").tpl("project_overview");\r\n    }\r\n</script>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "d:/projekte/studlis/studlis/studlis/webui/pages/project_overview.html", "uri": "pages/project_overview.html", "source_encoding": "utf-8", "line_map": {"16": 0, "21": 1, "27": 21}}
__M_END_METADATA
"""
