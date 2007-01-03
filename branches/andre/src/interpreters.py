'''
interpreters.py

code execution and simplification of error messages

HTTPrepl:
    Class which provide a Python interpreter embedded in a browser.
    Adapted from Robert (fumanchu) Brewer's code.
    repl: read-eval-print loop.

CrunchyInterpreter:
    Class which provides a Python interpreter used to run code from
    an "editor" or from a "doctest".
    
exec_external:
    Function used to run code as a separate external process.
    This is most useful for running GUI based programs.
    
exec_graphics:
    Function used to process graphics (draw or plot) scripts.
    Could probably be rewritten to use CrunchyInterpreter.
'''
# Python standard library modules
import codeop
import inspect
import os
import re
import sys
import threading
from doctest import DocTestRunner, DocTestParser
from StringIO import StringIO
from popen2 import popen2
from subprocess import Popen
from xml.sax.saxutils import escape as _escape
# crunchy modules
import errors
import crunchyfier
import graphics
import sound
import utilities
from translation import _

interpreters = {}
success = False

interps = {}

class Singleton(object):
    """From the 2nd edition of the Python cookbook.
       Ensures that only one instance is created per running script"""
    def __new__(cls, *args, **kwargs):
        if '_inst' not in vars(cls):
            cls._inst = object.__new__(cls, *args, **kwargs)
        return cls._inst

class HTTPrepl(Singleton):
   
    def __init__(self):
        self.locals = {}
        self.buffer = []
   
    def push(self, line):
        """Push 'line' and return exec results (None if more input needed)."""
        if line == "help":
            return _("Type help(object) for help about object.")
        if line == "help()":
            return _("You cannot call help() without an argument.")
        self.buffer.append(line)
        source = "\n".join(self.buffer)
        try:
            code = codeop.compile_command(source, "<Crunchy :-)>", 'single')
        except (OverflowError, SyntaxError, ValueError):
            self.buffer = []
            return errors.get_syntax_error(line)
        if code is None:
            # More lines needed.
            return None
        self.buffer = []
        res = self.execute(code)
        if not res:
            return ''
        else: 
            return res
   
    def execute(self, code):
        """Execute the given code in self.locals and return any stdout/sterr."""
        out = StringIO()
        oldout = sys.stdout
        olderr = sys.stderr
        sys.stdout = sys.stderr = out
        try:
            try:
                exec code in self.locals
            except:
                result = errors.get_traceback(" ")
            else:
                result = out.getvalue()
        finally:
            sys.stdout = oldout
            sys.stderr = olderr
        out.close()
        return result
   
    def dir(self, line):
        """Examine a partial line and provide attr list of final expr."""
        line = re.split(r"\s", line)[-1].strip()
        # Support lines like "thing.attr" as "thing.", because the browser
        # may not finish calculating the partial line until after the user
        # has clicked on a few more keys.
        line = ".".join(line.split(".")[:-1])
        try:
            result = eval("dir(%s)" % line, {}, self.locals)
        except:
            return []
        return result
   
    def doc(self, line):
        """Examine a partial line and provide sig+doc of final expr."""
        line = re.split(r"\s", line)[-1].strip()
        # Support lines like "func(text" as "func(", because the browser
        # may not finish calculating the partial line until after the user
        # has clicked on a few more keys.
        line = "(".join(line.split("(")[:-1])
        try:
            result = eval(line, {}, self.locals)
            try:
                if isinstance(result, type):
                    func = result.__init__
                else:
                    func = result
                args, varargs, varkw, defaults = inspect.getargspec(func)
            except TypeError:
                if callable(result):
                    doc = getattr(result, "__doc__", "") or ""
                    return "%s\n\n%s" % (line, doc)
                return None
        except:
            return _('%s is not defined yet')%line
       
        if args and args[0] == 'self':
            args.pop(0)
        missing = object()
        defaults = defaults or []
        defaults = ([missing] * (len(args) - len(defaults))) + list(defaults)
        arglist = []
        for a, d in zip(args, defaults):
            if d is missing:
                arglist.append(a)
            else:
                arglist.append("%s=%s" % (a, d))
        if varargs:
            arglist.append("*%s" % varargs)
        if varkw:
            arglist.append("**%s" % varkw)
        doc = getattr(result, "__doc__", "") or ""
        return "%s(%s)\n%s" % (line, ", ".join(arglist), doc)


def escape(data):
    """make a string suitable for embedding in HTML"""
    data =  _escape(data)
    data = data.replace('\n', '<br/>')
    return data

    
class CrunchyInterpreter(threading.Thread):
    """Run python source asynchronously and parse the standard 
        python error output to make it friendlier.  Also, helps 
        with the isolation of sessions.
    """
    def __init__(self, code, name, symbols = {}, doctest=False):
        threading.Thread.__init__(self)
        self.code = code
        interpreters[name] = self
        self.name = name
        self.symbols = dict(symbols, **sound.all_sounds)
        self._doctest = doctest
        
    def run(self):
        """run the code, redirecting stdout and returning the string representing the output
        """
        sys.stdout.register_thread(id = self.name)
        sys.stderr.register_thread(self.name)
        self.code = utilities.fixLineEnding(self.code)
        try:
            self.ccode = compile(self.code, "crunchy_exec", 'exec')
        except:
            sys.stderr.write(errors.get_syntax_error(self.code))
            return
        if not self.ccode:    #code does nothing
            return
        try:
            exec self.ccode in self.symbols
        except:
            sys.stderr.write(errors.get_traceback(self.code))
            
    def get(self):
        global success
        str1 = sys.stdout.get_by_id(self.name)
        str2 = sys.stderr.get_by_id(self.name)
        info = ''
        if self._doctest and str1: # str1 should mean that doctest was executed
            str1 = '<span class="error_info">' + escape(str1) + "</span>"
            if not success:
                str2, exception_found = self.simplify_doctest_error_message(str2)
                if exception_found:
                    info = '<br/><span class="error_info">' + \
                       '<a href="/docs/reference/errors.html">' + \
                       '%s</a></span>'%_("Follow this link if you want to know more about exceptions.")
        elif self._doctest:  # should be: a syntax error prevented execution
            lines = str2.split('\n')
            if lines[0].strip().startswith("File"): # remove meaningless line
                lines = lines[1:]
            # Python indicates the approximative location of a syntax error by
            # a caret (^) preceded by a number of whitespaces.  The whitespaces
            # are essentially removed by html; so we replace them by something
            # visible so that the caret is located where Python indicated.
            for n, line in enumerate(lines):
                nb_spaces = 0
                for character in line:
                    if character == " ":
                        nb_spaces += 1
                    else:
                        break
                if nb_spaces >= 4:
                    nb_spaces -= 4
                    lines[n] = "~"*nb_spaces + lines[n][nb_spaces:]
            str2 = '\n'.join(lines)
        else:
            str1 = '<span class="stdout">' + escape(str1) + "</span>"
        str2 = '<span class="stderr">' + escape(str2) + "</span>" + info
        return str1 + str2

    def simplify_doctest_error_message(self, msg):
        stars = "*"*70
        failures = msg.split(stars)
        new_mesg = ["="*70]
        exception_found = False
        for fail in failures:
            if fail: # ignore empty lines
                lines = fail.split('\n')
                for line in lines[2:-2]:
                    if line.startswith("Failed example:"):
                        new_mesg.append(_("The following example failed:"))
                    elif line.startswith("Expected:"):
                        new_mesg.append(_("The expected result was:"))
                    elif line.startswith("Got:"):
                        new_mesg.append(_("The result obtained was:"))
                    elif line.startswith("Exception raised:"):
                        new_mesg.append(_("An exception was raised:"))
                        exception_found = True
                        break
                    else:
                        new_mesg.append(line)
                new_mesg.append(lines[-2])
                new_mesg.append("-"*70)
        return '\n'.join(new_mesg), exception_found

def run_doctest(code, doctestname):
    '''Executes some Python code treated as a module accompanied by some
       doctests to be tested by the doctest module from the standard
       library.
    '''
    doctest = utilities.fixLineEnding('\n"""\n' + 
                                 crunchyfier.DOCTESTS[doctestname] + '\n"""\n')
    code += '''
import sys
__t=sys.stdout
sys.stdout = sys.stderr
__test = __parser.get_doctest(__teststring, globals(),"Crunchy Doctest", "<crunchy>", 0)
_x= __runner.run(__test)
sys.stdout=__t
print analyse(_x)
'''
    runner = DocTestRunner()
    parser = DocTestParser()
    symbols = {'__parser': parser, 
                '__runner': runner, 
                '__teststring': doctest,
                'analyse': analyse_doctest_result}

    i = CrunchyInterpreter(code, doctestname, symbols, True)
    i.start()
    return
    
def analyse_doctest_result(x):
    """Determines the message to give based on the number of failures."""
    global success
    failures, total = x
    if failures:
        success = False
    else:
        success = True
    if total == 0:
        return _("There was no test to satisfy.")
    elif total == 1:
        if failures == 0:
            return _("Congratulation, your code passed the test!")
        else:
            return _("You code failed the test.")
    else:
        if failures == 0:
            return _("Congratulation, your code passed all %d tests!")%total
        elif failures == total:
            return _("Your code failed all %d tests.")%total
        else:
            return _("Your code failed %s out of %s tests.")%(failures, total)




def exec_external(code, console=False, path=None):
    """execute code in an external process
    currently works under: 
        * Windows NT (tested)
        * GNOME (tested)  [January 2nd change untested]
    This also needs to be implemented for OS X, KDE 
    and some form of linux fallback (xterm?)
    """
    if path is None:
        path = os.path.join("temp", "temp.py")
        if os.name == 'nt':
            current_dir = os.getcwd()
            target_dir = current_dir
            fname = path
    elif os.name == 'nt':
        target_dir, fname = os.path.split(path)
        current_dir = os.getcwd() 
                                  
    filename = open(path, 'w')
    filename.write(code)
    filename.close()
        
    if os.name == 'nt':
        os.chdir(target_dir) # change dir so as to deal with paths that
                             # include spaces
        if console:
            Popen(["cmd.exe", ('/c start python %s'%fname)])
        else:
            Popen(["cmd.exe", ('/c python %s'%fname)])
        os.chdir(current_dir)
    elif os.name == 'posix':
        try:
            os.spawnlp(os.P_NOWAIT, 'gnome-terminal', 'gnome-terminal', 
                                '-x', 'python', '%s'%path)
        except:
            raise NotImplementedError
    else:
        raise NotImplementedError

# The following is adapted from "Python Standard Library", by Fredrik Lundh
##def win_run(program, *args):
##    for path in os.environ["PATH"].split(os.pathsep):
##        filename = os.path.join(path, program) + ".exe"
##        try:
##            return Popen([filename, args])
##        except:
##            pass
##    raise os.error, "cannot find executable"

#---- The following is for graphics
_js_init = """
var canvas, ctx;
canvas = document.getElementById("%s");
ctx = canvas.getContext("2d");
%s
"""

def exec_graphics(id, code):
    if not code:
        return _js_init%(id, '')
    else:
        code = utilities.fixLineEnding(code)
    if 'canvas' in id:
        res = re.search(r'canvas([0-9]+?)_([0-9]+?)code', id)
        width = int(res.groups()[0])
        height = int(res.groups()[1])
    if 'plot' in id:
        res = re.search(r'plot([0-9]+?)_([0-9]+?)code', id)
        width = int(res.groups()[0])
        height = int(res.groups()[1])
    else:
        width, height = 400, 400
    
    if 'plot' in id:
        __g = graphics.Plot(width, height)
        __dict =  { _('set_line_color'): __g.set_line_colour, # for those used
                _('set_line_colour'): __g.set_line_colour,   # to canvas commands
                _('color'): __g.set_line_colour,   # simpler
                _('colour'): __g.set_line_colour,
                _('x_range'): __g.set_xrange,
                _('y_range'): __g.set_yrange, 
                _('x_axis'): __g.x_axis,
                _('y_axis'): __g.y_axis,
                _('prepare_graph'): __g.prepare_graph,
                _('plot_function'): __g.plot_function
                }
    else:
        __g = graphics.Graphics(width, height)
        __dict =  {_('circle'): __g.circle,
                _('filled_circle'): __g.filled_circle,
                _('filled_rectangle'): __g.filled_rectangle,
                _('filled_triangle'): __g.filled_triangle,
                _('line'): __g.line,
                _('rectangle'): __g.rectangle,
                _('set_line_color'): __g.set_line_colour,
                _('set_line_colour'): __g.set_line_colour,
                _('set_fill_color'): __g.set_fill_colour,
                _('set_fill_colour'): __g.set_fill_colour,
                _('triangle'): __g.triangle,
                _('point'): __g.point}
    graph_dict = dict(__dict, **sound.all_sounds)
    try:
        exec code in graph_dict
    except errors.ColourNameError, info:
        raise
    except Exception, info:
        raise
    result = ''.join(__g.js_code)
    return _js_init%(id, result)


