# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1707836354.4979966
_enable_loop = True
_template_filename = 'D:/Projekte/MV6/mvicon/mvicon/mvicon/webui/_layout.html'
_template_uri = '_layout.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('<!DOCTYPE html>\r\n<html lang="en">\r\n<head>\r\n    <meta charset="UTF-8">\r\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\r\n    <title>MV</title>\r\n    <link href="static/bootstrap5.3/css/bootstrap.min.css" rel="stylesheet"crossorigin="anonymous">\r\n    <link href="static/fontawesome/css/all.min.css" rel="stylesheet">\r\n    <link href="static/main.css" rel="stylesheet">\r\n    <link href="static/ui.css" rel="stylesheet">\r\n</head>\r\n<body>\r\n    <div class="main-view main-view-outer" id="main_view" explorer=\'hidden\'>\r\n        <div class="main-view-sidenav" collapsed="false">\r\n            <ul>\r\n                <li onclick="page_icons.show();">\r\n                    \r\n                    <i class="fa-solid fa-icons"></i>\r\n                    <span>Icons</span>\r\n                </li>\r\n                <li onclick="new_icon.show();">\r\n                    <i class="fa-solid fa-circle-plus" ></i>\r\n                    <span>New Icon</span>\r\n                </li>\r\n                <li onclick="page_categories.show()">\r\n                    <i class="fa-solid fa-list"></i>\r\n                    <span>Categories</span>\r\n                </li>\r\n                <li onclick="page_variants.show()">\r\n                  <i class="fa-solid fa-palette"></i>\r\n                  <span>Variants</span>\r\n              </li>\r\n\r\n\r\n                \r\n                <li>\r\n                    <i class="fa-solid fa-newspaper"></i>\r\n                    <span>Licenses</span>\r\n                </li>               \r\n                <li onclick="page_export.show();">\r\n                    <i class="fa-solid fa-file-export"></i>\r\n                    <span>Export</span>\r\n                </li>    \r\n                <li>\r\n                    <i class="fa-solid fa-cloud-arrow-down"></i>\r\n                    <span>Update</span>\r\n                </li>                               \r\n            </ul>\r\n        </div>\r\n\r\n        <script src="static/bootstrap5.3/js/bootstrap.bundle.min.js"></script>\r\n        <script src="static/jquery/jquery-3.7.1.min.js"></script>\r\n        <script src="static/lang.js"></script>\r\n        <script src="static/ui.js"></script>\r\n        <script src="static/engine.js"></script>\r\n        <script src="static/editor.js"></script>\r\n        ')
        __M_writer(str(self.body()))
        __M_writer('\r\n       \r\n    </div>\r\n\r\n  \r\n    <div class="modal fade" id="error_modal" tabindex="-1" aria-labelledby="modalLabel" aria-hidden="true">\r\n        <div class="modal-dialog">\r\n          <div class="modal-content">\r\n            <div class="modal-header">\r\n              <h5 class="modal-title" id="modalLabel">Error Details</h5>\r\n              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\r\n            </div>\r\n            <div class="modal-body">\r\n              <p id="error_text">Error text will be displayed here.</p>\r\n              <p id="error_detail">Error details will be displayed here.</p>\r\n              <!--<p id="error_log">Error log will be displayed here.</p>-->\r\n            </div>\r\n            <div class="modal-footer">\r\n              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>\r\n            </div>\r\n          </div>\r\n        </div>\r\n      </div>\r\n\r\n</body>\r\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "D:/Projekte/MV6/mvicon/mvicon/mvicon/webui/_layout.html", "uri": "_layout.html", "source_encoding": "utf-8", "line_map": {"16": 0, "22": 1, "23": 57, "24": 57, "30": 24}}
__M_END_METADATA
"""
