# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1741518626.6298807
_enable_loop = True
_template_filename = 'd:/projekte/studlis/studlis/studlis/webui/pages/select_project.html'
_template_uri = 'pages/select_project.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer('<template tpl_id="select_project">\r\n    <div>\r\n        <h2>Wähle Studie</h2>\r\n        <div class="project_list">\r\n            <div class="row">\r\n                <div class="col-12">\r\n                    <table class="project-table table-modern">\r\n                        <thead>\r\n                            <tr class="">\r\n                                <td>Name</td>\r\n                                <td>Beschreibung</td>\r\n                                <td>Studienzahl</td>\r\n\r\n                            </tr>\r\n                        </thead>\r\n                        <tbody class="project-content"></tbody>\r\n                    </table>\r\n                </div>\r\n                <div class="col-4">\r\n                </div>\r\n\r\n            </div>\r\n        </div>\r\n\r\n\r\n    </div>\r\n</template>\r\n<template tpl_id="project_item">\r\n    <tr class="" style="font-size:12pt;">\r\n        <td class="project-name"></td>\r\n        <td class="project-desc"></td>\r\n        <td class="project-count">\r\n\r\n        </td>\r\n\r\n    </tr>\r\n\r\n</template>\r\n<script>\r\n    var selected_project="";\r\n    page_select_project = {};\r\n    page_select_project.show = function () {\r\n        node = $("#main-view-content").tpl("select_project");\r\n        DoRequest("get_project_list", {"token":session_token}, function (data) {\r\n            if (data.value) {\r\n                for (var i = 0; i < data.value.length; i++) {\r\n                    var project = data.value[i];\r\n                    var node = $(".project-content").tpl("project_item");\r\n                    node.find(".project-name").text(project.name);\r\n                    node.find(".project-desc").text(project.description);\r\n                    node.find(".project-count").text(project.study_count);\r\n                    node.click(function () {\r\n                        page_select_project.select_project(project.name);\r\n                    });\r\n                    //$(".main-view-sidenav").removeClass("d-none");\r\n                \r\n                }\r\n            }\r\n        });\r\n    }\r\n    page_select_project.select_project = function (project_name) {\r\n        selected_project = project_name;\r\n        $(".main-view-sidenav").removeClass("d-none");\r\n        page_project_overview.show();\r\n    }\r\n\r\n\r\n\r\n</script>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "d:/projekte/studlis/studlis/studlis/webui/pages/select_project.html", "uri": "pages/select_project.html", "source_encoding": "utf-8", "line_map": {"16": 0, "21": 1, "27": 21}}
__M_END_METADATA
"""
