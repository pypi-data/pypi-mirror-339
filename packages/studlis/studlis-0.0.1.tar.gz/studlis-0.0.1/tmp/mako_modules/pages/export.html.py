# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1707919528.9872432
_enable_loop = True
_template_filename = '/home/niklas/projects/mvicon/mvicon/webui/pages/export.html'
_template_uri = 'pages/export.html'
_source_encoding = 'utf-8'
_exports = []



import platform


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer('<template tpl_id="page_export">\n    <div>\n        <h2>Export</h2>\n        Download all icons as a zip file.\n        \n\n        <button type="button" class="btn btn-primary" onclick="export_icons();return false;">Download</button>\n        ')
        __M_writer('\n\n')
        if platform.system() == 'Windows':
            __M_writer('            <p><span style="color:red">Server is running on Windows platform, this is currently not supported</span></p>\n')
        __M_writer('    </div>\n</template>\n<script>\n    var page_export = {};\n    page_export.show = function(){\n        node=$("#main-view-content").tpl("page_export");\n    }\n    var export_icons = function(){\n        DoDownload("download_icons",{},"icons.zip");\n    }\n</script>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "/home/niklas/projects/mvicon/mvicon/webui/pages/export.html", "uri": "pages/export.html", "source_encoding": "utf-8", "line_map": {"16": 8, "17": 9, "18": 10, "19": 11, "20": 0, "25": 1, "26": 10, "27": 12, "28": 13, "29": 15, "35": 29}}
__M_END_METADATA
"""
