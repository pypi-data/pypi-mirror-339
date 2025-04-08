# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1741859010.3896227
_enable_loop = True
_template_filename = 'd:/projekte/studlis/studlis/studlis/webui/main.html'
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
        global_variants = context.get('global_variants', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\r\n\r\n\r\n<!-- Main content goes here -->\r\n<div class="main-view-content d-flex flex-colum" id="main-view-content">\r\n            \r\n</div>\r\n\r\n\r\n<script>\r\n  var global_variants = ')
        __M_writer(str(global_variants))
        __M_writer(";\r\n  var studlib={};\r\n  studlib.dirty=false; // flag to indicate if the document has been modified\r\n  studlib.on_save_event=undefined; // callback function to be called when save event is triggered\r\n  window.addEventListener('beforeunload', function (e) {\r\n        if (!studlib.dirty) {\r\n            return; // Do nothing if no changes were made\r\n        }\r\n   \r\n        var confirmationMessage = 'Eingaben wurden verändert, wirklich verlassen?';\r\n        e.returnValue = confirmationMessage; \r\n        return confirmationMessage; \r\n       \r\n    });\r\n\r\n    document.addEventListener('keydown', function (e) {\r\n      if (e.ctrlKey && e.key === 's') {\r\n        e.preventDefault(); // Prevent the default save action\r\n        if (typeof studlib.on_save_event === 'function') {\r\n          studlib.on_save_event(); // Call the save event callback\r\n        }\r\n      }\r\n    },true);\r\n\r\n\r\n</script>\r\n\r\n\r\n<!-- Include subpages --->\r\n\r\n")
        runtime._include_file(context, 'pages/login.html', _template_uri)
        __M_writer('\r\n')
        runtime._include_file(context, 'pages/select_project.html', _template_uri)
        __M_writer('\r\n')
        runtime._include_file(context, 'pages/project_overview.html', _template_uri)
        __M_writer('\r\n')
        runtime._include_file(context, 'pages/study_browser.html', _template_uri)
        __M_writer('\r\n')
        runtime._include_file(context, 'pages/study_viewer.html', _template_uri)
        __M_writer('\r\n<script>\r\n\r\n\r\n  \r\n</script>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "d:/projekte/studlis/studlis/studlis/webui/main.html", "uri": "main.html", "source_encoding": "utf-8", "line_map": {"27": 0, "33": 1, "34": 11, "35": 11, "36": 41, "37": 41, "38": 42, "39": 42, "40": 43, "41": 43, "42": 44, "43": 44, "44": 45, "45": 45, "51": 45}}
__M_END_METADATA
"""
