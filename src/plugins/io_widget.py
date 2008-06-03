"""The IO widget, handles text and graphical IO
This is just the UI part, the communication code is defined in the core
"""

# All plugins should import the crunchy plugin API via interface.py
from src.interface import config, plugin, translate, SubElement
from editarea import editArea_load_and_save
_ = translate['_']

provides = set(["io_widget"])

def register():
    '''register a service'''
    plugin['register_service']("insert_io_subwidget", insert_io_subwidget)
    # register the function for killing threads:
    plugin['register_http_handler']("/kill_thread%s" % plugin['session_random_id'],
                                    kill_thread_handler)

def kill_thread_handler(request):
    """Kills the thread associated with uid"""
    plugin['kill_thread'](request.args["uid"])

def insert_io_subwidget(page, elem, uid, interp_kind=None, sample_code=''):
    """insert an output widget into elem, usable for editors and interpreters,
    and includes a canvas.
    """
    # When a security mode is set to "display ...", we only parse the
    # page, but no Python execution from is allowed from that page.
    # If that is the case, we won't include javascript either, to make
    # thus making the source easier to read.
    if 'display' not in config['page_security_level'](page.url):

        # for some reason, we must create the link/image and hide it if
        # ctypes is not available, rather than not create it at all;
        # if we attempt to not create it, the io widget does not appear... ?!?
        kill_link = SubElement(elem, "a")
        kill_link.attrib["id"] = "kill_%s" % uid
        kill_link.attrib["onclick"] = "kill_thread('%s')" % uid
        kill_image = SubElement(kill_link, 'img')
        kill_image.attrib["src"] = "/display_big.png"
        kill_image.attrib["alt"] = "Interrupt thread"
        kill_image.attrib["class"] = "kill_thread_image"
        kill_image.attrib["id"] = "kill_image_%s" % uid
        if not config['ctypes_available']:
            kill_image.attrib['style'] = 'display: none;'
            kill_link.attrib['style'] = 'display: none;'

        if not page.includes("io_included"):
            page.add_include("io_included")
            page.add_js_code(io_js)
            page.add_css_code(io_css)

        if interp_kind is not None:
            if not page.includes("push_input_included"):
                page.add_include("push_input_included")
                page.add_js_code(push_input)
            # needed for switching to edit area; not currently working
            if not page.includes("editarea_included"):
                page.add_include("editarea_included")
                page.add_js_code(editArea_load_and_save)
                page.insert_js_file("/edit_area/edit_area_crunchy.js")
        elif config['ctypes_available']:
            kill_image.attrib['style'] = 'display:none;'  # revealed by Execute button

    output = SubElement(elem, "span")
    output.attrib["class"] = "output"
    output.attrib["id"] = "out_" + uid
    output.text = "\n"
    span_input = SubElement(elem, "span")
    inp = SubElement(span_input, "input")
    inp.attrib["id"] = "in_" + uid
    inp.attrib["onkeydown"] = 'return push_keys(event, "%s")' % uid
    if interp_kind is not None:
        editor_link = SubElement(span_input, "a")
        editor_link.attrib["onclick"] = "return convertToEditor(this,'%s')" \
                                      % _("Execute")
        editor_link.attrib["id"] = "ed_link_" + uid
        image = SubElement(editor_link, 'img')
        image.attrib["src"] = "/editor.png"
        image.attrib["alt"] = "copy existing code"
        image.attrib["class"] = "interpreter_image"
        code_sample = SubElement(elem, "textarea")
        code_sample.attrib["id"] = "code_sample_" + uid
        code_sample.attrib["style"] = 'visibility:hidden;overflow:hidden;z-index:-1;position:fixed;top:0;'
        if sample_code:
            code_sample.text = sample_code
        else:
            code_sample.text = '\n'
    if interp_kind == 'borg':
        inp.attrib["onkeypress"] = 'return tooltip_display(event, "%s")' % uid
    inp.attrib["type"] = "text"
    inp.attrib["class"] = "input"

io_js = r"""
function push_keys(event, uid){
    // prevent Esc from breaking the interpreter
    if (event.keyCode == 27) return false;
    if (event.keyCode != 13) return true;
    
    data = $("#in_"+uid).val();
    $("#in_"+uid).val("");
    $.ajax({type : "POST",
            url : "/input%s?uid="+uid, 
            data : data + "\n",
            processData : false
            });
    
    return true;
};

function kill_thread(uid){
    $.get("/kill_thread%s?uid="+uid);
};
""" % (plugin['session_random_id'], plugin['session_random_id'])

push_input = r"""
function push_input(uid){
    data = $("#code_"+uid).val();
    $("#in_"+uid).val("");
    $.ajax({type : "POST",
            url : "/input%s?uid="+uid, 
            data : data + "\n",
            processData : false
            });
    
    convertFromEditor(uid);
    return true;
};
""" % plugin['session_random_id']

# moved most style information to crunchy.css
io_css = r"""
.crunchy_canvas{
    display: none;
}
"""
