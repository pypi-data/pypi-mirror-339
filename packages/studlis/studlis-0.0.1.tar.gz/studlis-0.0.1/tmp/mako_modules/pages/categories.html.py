# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1707836354.5400224
_enable_loop = True
_template_filename = 'D:/Projekte/MV6/mvicon/mvicon/mvicon/webui/pages/categories.html'
_template_uri = 'pages/categories.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer('<template tpl_id="page_category_list">\r\n    <div>\r\n        <h2>Kategorien</h2>\r\n        <div class="row">\r\n            <div class="col-8">\r\n                <table class="category-table table-modern">\r\n                    <thead ><tr>\r\n\r\n                        <td>Kategorie</td>\r\n                        <td>Anzahl Icons</td>\r\n                    </tr></thead>\r\n                    <tbody class="category-table-content"></tbody>\r\n                </table>\r\n            </div>\r\n            <div class="col-4">\r\n            </div>\r\n       \r\n    </div>\r\n</template>\r\n<template tpl_id="category_element">\r\n    <tr>\r\n        \r\n        <td class="category-name"></td>\r\n        <td class="category-count"></td>\r\n    </tr>\r\n\r\n</template>\r\n\r\n\r\n\r\n\r\n\r\n<script>\r\n    var page_categories = {};\r\n    page_categories.show = function(){\r\n        node=$("#main-view-content").tpl("page_category_list");\r\n        DoRequest("categories",{filter:""},function(data){\r\n            $(".category-table-content").empty();\r\n\r\n            $.each(data.value,function(index,item){\r\n                var node = $(".category-table-content").appendtpl("category_element");\r\n                node.find(".category-name").html(item.name);\r\n                node.find(".category-count").html(item.icon_count);\r\n                $(".category-table-content").append(node);\r\n            });\r\n        });\r\n    }\r\n</script>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "D:/Projekte/MV6/mvicon/mvicon/mvicon/webui/pages/categories.html", "uri": "pages/categories.html", "source_encoding": "utf-8", "line_map": {"16": 0, "21": 1, "27": 21}}
__M_END_METADATA
"""
