import re
import sys
import urllib
import urllib2
import hashlib
import base64
try:
    import cPickle as pickle
except ImportError:
    import pickle
if sys.version_info >= (2, 5):
    import hashlib
    md5_constructor = hashlib.md5
else:
    import md5
    md5_constructor = md5.new



def _get_lines_from_file(filename, lineno, context_lines, loader=None, module_name=None):
    """
    Returns context_lines before and after lineno from file.
    Returns (pre_context_lineno, pre_context, context_line, post_context).
    """
    source = None
    if loader is not None and hasattr(loader, "get_source"):
        source = loader.get_source(module_name)
        if source is not None:
            source = source.splitlines()
    if source is None:
        try:
            f = open(filename)
            try:
                source = f.readlines()
            finally:
                f.close()
        except (OSError, IOError):
            pass
    if source is None:
        return None, [], None, []

    encoding = 'ascii'
    for line in source[:2]:
        # File coding may be specified. Match pattern from PEP-263
        # (http://www.python.org/dev/peps/pep-0263/)
        match = re.search(r'coding[:=]\s*([-\w.]+)', line)
        if match:
            encoding = match.group(1)
            break
    source = [unicode(sline, encoding, 'replace') for sline in source]

    lower_bound = max(0, lineno - context_lines)
    upper_bound = lineno + context_lines

    pre_context = [line.strip('\n') for line in source[lower_bound:lineno]]
    context_line = source[lineno].strip('\n')
    post_context = [line.strip('\n') for line in source[lineno+1:upper_bound]]

    return lower_bound, pre_context, context_line, post_context


def strip_picklabes(vars):
    ret = []
    for name, value in vars:
        try:
            pickle.dumps(value)
        except:
            value = repr(value)
        ret.append((name, value))
    return ret


def get_frames(tb):
    frames = []
    while tb is not None:
        # support for __traceback_hide__ which is used by a few libraries
        # to hide internal frames.
        if tb.tb_frame.f_locals.get('__traceback_hide__'):
            tb = tb.tb_next
            continue
        filename = tb.tb_frame.f_code.co_filename
        function = tb.tb_frame.f_code.co_name
        lineno = tb.tb_lineno - 1
        loader = tb.tb_frame.f_globals.get('__loader__')
        module_name = tb.tb_frame.f_globals.get('__name__')
        pre_context_lineno, pre_context, context_line, post_context = _get_lines_from_file(filename, lineno, 7, loader, module_name)
        if pre_context_lineno is not None:
            frames.append({
        #        'tb': tb,
                'filename': filename,
                'function': function,
                'lineno': lineno + 1,
                'vars': strip_picklabes(tb.tb_frame.f_locals.items()),
                'id': id(tb),
                'pre_context': pre_context,
                'context_line': context_line,
                'post_context': post_context,
                'pre_context_lineno': pre_context_lineno + 1,
            })
        tb = tb.tb_next
    return frames


def urlread(url, get={}, post={}, headers={}, timeout=None):
    req = urllib2.Request(url, urllib.urlencode(get), headers=headers)
    try:
        response = urllib2.urlopen(req, urllib.urlencode(post), timeout).read()
    except:
        response = urllib2.urlopen(req, urllib.urlencode(post)).read()
    return response


def send(url, kwargs, key):
    data = {
        'data': base64.b64encode(pickle.dumps(kwargs).encode('zlib')),
        'key': key,
    }
    urlread(url, post=data, timeout=5)

