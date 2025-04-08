# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1741518766.7967715
_enable_loop = True
_template_filename = 'd:/projekte/studlis/studlis/studlis/webui/_layout.html'
_template_uri = '_layout.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>MV</title>\n    <link href="static/bootstrap5.3/css/bootstrap.min.css" rel="stylesheet"crossorigin="anonymous">\n    <link href="static/fontawesome/css/all.min.css" rel="stylesheet">\n    <link href="static/main.css" rel="stylesheet">\n    <link href="static/ui.css" rel="stylesheet">\n    <link rel="stylesheet" href="static/toastui/toastui-editor.min.css" />\n    <link rel="stylesheet" href="static/select2/select2.min.css" />\n    <link rel="stylesheet" href="static/jstree/themes/default/style.min.css" />\n</head>\n<body>\n    <div class="main-view main-view-outer" id="main_view" explorer=\'hidden\'>\n        <div class="main-view-sidenav d-none" collapsed="false">\n            <ul>\n                <li onclick="page_search.show();">\n                    \n                    <i class="fa-solid fa-icons"></i>\n                    <span>Projekt Übersicht</span>\n                </li>\n                <li onclick="page_study_browser.show()">\n                    <i class="fa-solid fa-list"></i>\n                    <span>Studien</span>\n                </li>\n                <li onclick="wiki_edit.show()">\n                    <i class="fa-solid fa-list"></i>\n                    <span>Quick Info</span>\n                </li>\n                <li onclick="page_variants.show()">\n                  <i class="fa-solid fa-palette"></i>\n                  <span>Variants</span>\n              </li>\n\n\n                \n                <li>\n                    <i class="fa-solid fa-newspaper"></i>\n                    <span>Licenses</span>\n                </li>               \n                <li onclick="page_export.show();">\n                    <i class="fa-solid fa-file-export"></i>\n                    <span>Export</span>\n                </li>    \n                <li onclick="do_logout();">\n                    <i class="fa-solid fa-cloud-arrow-down" "></i>\n                    <span>Logout</span>\n                </li>                               \n            </ul>\n        </div>\n\n        <script src="static/bootstrap5.3/js/bootstrap.bundle.min.js"></script>\n        <script src="static/jquery/jquery-3.7.1.min.js"></script>\n        <script src="static/lang.js"></script>\n        <script src="static/ui.js"></script>\n        <script src="static/engine.js"></script>\n        <script src="static/editor.js"></script>\n\n        ')
        __M_writer(str(self.body()))
        __M_writer('\n        <script src="static/toastui/toastui-editor-all.min.js"></script>\n        <script src="static/select2/select2.min.js"></script>\n        <script src="static/jstree/jstree.min.js"></script>\n    </div>\n\n  \n    <div class="modal fade" id="error_modal" tabindex="-1" aria-labelledby="modalLabel" aria-hidden="true">\n        <div class="modal-dialog">\n          <div class="modal-content">\n            <div class="modal-header">\n              <h5 class="modal-title" id="modalLabel">Error Details</h5>\n              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\n            </div>\n            <div class="modal-body">\n              <p id="error_text">Error text will be displayed here.</p>\n              <p id="error_detail">Error details will be displayed here.</p>\n              <!--<p id="error_log">Error log will be displayed here.</p>-->\n            </div>\n            <div class="modal-footer">\n              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>\n            </div>\n          </div>\n        </div>\n      </div>\n\n</body>\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "d:/projekte/studlis/studlis/studlis/webui/_layout.html", "uri": "_layout.html", "source_encoding": "utf-8", "line_map": {"16": 0, "22": 1, "23": 61, "24": 61, "30": 24}}
__M_END_METADATA
"""
