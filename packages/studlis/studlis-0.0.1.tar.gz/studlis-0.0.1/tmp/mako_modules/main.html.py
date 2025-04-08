# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1707836354.4520636
_enable_loop = True
_template_filename = 'D:/Projekte/MV6/mvicon/mvicon/mvicon/webui/main.html'
_template_uri = 'main.html'
_source_encoding = 'utf-8'
_exports = []


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, '_layout.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer('\r\n\r\n\r\n<!-- Main content goes here -->\r\n<div class="main-view-content" id="main-view-content">\r\n            \r\n</div>\r\n\r\n<!-- Include subpages --->\r\n')
        runtime._include_file(context, 'pages/icon.html', _template_uri)
        __M_writer('\r\n')
        runtime._include_file(context, 'pages/new_icon.html', _template_uri)
        __M_writer('\r\n')
        runtime._include_file(context, 'pages/export.html', _template_uri)
        __M_writer('\r\n')
        runtime._include_file(context, 'pages/categories.html', _template_uri)
        __M_writer('\r\n')
        runtime._include_file(context, 'pages/variants.html', _template_uri)
        __M_writer('\r\n<script>\r\n  page_icons.show();\r\n\r\n</script>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "D:/Projekte/MV6/mvicon/mvicon/mvicon/webui/main.html", "uri": "main.html", "source_encoding": "utf-8", "line_map": {"27": 0, "32": 1, "33": 10, "34": 10, "35": 11, "36": 11, "37": 12, "38": 12, "39": 13, "40": 13, "41": 14, "42": 14, "48": 42}}
__M_END_METADATA
"""
