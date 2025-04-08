# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1741516279.947263
_enable_loop = True
_template_filename = 'd:/projekte/studlis/studlis/studlis/webui/pages/select_study.html'
_template_uri = 'pages/select_study.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer('<template tpl_id="select_study">\r\n    <div>\r\n        <h2>Wähle Studie</h2>\r\n        <div class="study_list">\r\n            <div class="row">\r\n                <div class="col-12">\r\n                    <table class="study-table table-modern">\r\n                        <thead>\r\n                            <tr class="d-none">\r\n                                <td>Name</td>\r\n                                <td>Detail</td>\r\n                                <td>Optionen</td>\r\n                            </tr>\r\n                        </thead>\r\n                        <tbody class="study-content"></tbody>\r\n                    </table>\r\n                </div>\r\n                <div class="col-4">\r\n                </div>\r\n\r\n            </div>\r\n        </div>\r\n\r\n\r\n    </div>\r\n</template>\r\n<template tpl_id="study_item">\r\n    <tr class="" style="font-size:12pt;">\r\n        <td class="study-name"></td>\r\n        <td class="study-desc"></td>\r\n        <td class="study-options">\r\n\r\n        </td>\r\n\r\n    </tr>\r\n\r\n</template>\r\n<script>\r\n    page_select_study = {};\r\n    page_select_study.show = function () {\r\n        node = $("#main-view-content").tpl("select_study");\r\n        DoRequest("get_study_list", {"token":session_token}, function (data) {\r\n            if (data.value) {\r\n                for (var i = 0; i < data.value.length; i++) {\r\n                    var study = data.value[i];\r\n                    var node = $(".study-content").tpl("study_item");\r\n                    node.find(".study-name").text(study.name);\r\n                    node.find(".study-desc").text(study.description);\r\n                    node.find(".study-options").append(\'<button class="btn btn-outline-secondary btn-sm" onclick="page_select_study.select_study(\' + study.id + \')">Auswählen</button>\');\r\n                \r\n                    //$(".main-view-sidenav").removeClass("d-none");\r\n                \r\n                }\r\n            }\r\n        });\r\n    }\r\n\r\n\r\n\r\n</script>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "d:/projekte/studlis/studlis/studlis/webui/pages/select_study.html", "uri": "pages/select_study.html", "source_encoding": "utf-8", "line_map": {"16": 0, "21": 1, "27": 21}}
__M_END_METADATA
"""
