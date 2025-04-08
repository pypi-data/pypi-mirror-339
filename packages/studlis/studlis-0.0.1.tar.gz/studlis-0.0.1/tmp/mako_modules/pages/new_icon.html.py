# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1707912181.535857
_enable_loop = True
_template_filename = '/home/niklas/projects/mvicon/mvicon/webui/pages/new_icon.html'
_template_uri = 'pages/new_icon.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer('\n<template tpl_id="page_new_icon">\n    <div>\n        <h3> New Icon</h3>\n        \n        <div class="mb-3">\n            <label for="exampleFormControlInput1" class="form-label">Icon Name</label>\n            <input type="text" class="form-control" id="exampleFormControlInput1" placeholder="...icon name...">\n        </div>\n        <div class="mb-3">\n            <label for="iconcat" class="form-label">Category</label>\n            <select class="form-select" id="iconcat" aria-label="Icon Category">\n                <option selected>loading...</option>\n            </select>\n        </div>\n        <div class="mb-3">\n            <label for="iconlic" class="form-label">License</label>\n            <select class="form-select" id="iconlic" aria-label="Icon Category">\n                <option selected>loading...</option>\n            </select>\n        </div>   \n    \n        <div class="mb-3">\n            <label for="iconlic" class="form-label">Icon SVG</label>\n            <div class="mb-3">\n                Please drop the .svg file here!\n    \n            </div>\n\n            <div id="svg_target">\n\n            </div>\n        </div>   \n        <button type="button" class="btn btn-primary" onclick="new_icon.save();return false;">\n            <i class="fas fa-save"></i> Save\n         </button>\n\n\n    </div>\n</template>\n\n\n\n<script>\n    var new_icon={};\n    new_icon.show=function(){\n        node=$("#main-view-content").tpl("page_new_icon");\n        set_svg_drop($("#main-view-content"),$("#svg_target"),function(file){\n            if($("#exampleFormControlInput1").val().length==0){\n                $("#exampleFormControlInput1").val(formatFileName(file.name));\n            }\n        });\n\n\n        DoRequest("categories_and_licences",{},function(data){\n            $("#iconlic").empty();\n            $.each(data.value.licenses,function(index,item){\n                var node = document.createElement("option");\n                node.innerHTML=item.name;\n                node.setAttribute("item_id",item.id);\n                $("#iconlic").append(node);\n            });\n            $("#iconcat").empty();\n            $.each(data.value.categories,function(index,item){\n                var node = document.createElement("option");\n                node.innerHTML=item.name;\n                node.setAttribute("item_id",item.id);\n                $("#iconcat").append(node);\n            });\n\n        });\n\n    }\n    new_icon.save = function(){\n        data={}\n        data.data = $("#svg_target").find("svg")[0].outerHTML;\n        data.name=$("#exampleFormControlInput1").val();\n        data.license_id=$("#iconlic option:selected").attr("item_id");\n        data.category_id=$("#iconcat option:selected").attr("item_id");\n        DoRequest("create_icon",data,function(data){\n            $("#exampleFormControlInput1").val("");\n            $("#svg_target").empty();\n        });\n\n\n    }\n\n\n\n\n    function formatFileName(fileName) {\n        // Remove the file extension\n        const nameWithoutExtension = fileName.substring(0, fileName.lastIndexOf(\'.\')) || fileName;\n        // Capitalize the first letter\n        const capitalized = nameWithoutExtension.charAt(0).toUpperCase() + nameWithoutExtension.slice(1);\n        return capitalized;\n    }\n</script>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "/home/niklas/projects/mvicon/mvicon/webui/pages/new_icon.html", "uri": "pages/new_icon.html", "source_encoding": "utf-8", "line_map": {"16": 0, "21": 1, "27": 21}}
__M_END_METADATA
"""
