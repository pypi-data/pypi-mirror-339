import os
import shutil
import sys
import tempfile
import getpass
from functools import reduce
from itertools import chain
from pathlib import Path
from dektools.file import sure_dir, write_file, read_text, remove_path, sure_parent_dir, normal_path, \
    format_path_desc, read_file, split_ext, path_ext, clear_dir, copy_recurse_ignore, \
    split_file, combine_split_files, remove_split_files, meta_split_file, tree, iglob, \
    where, where_list, which, which_list
from dektools.hash import hash_file
from dektools.zip import compress_files, decompress_files
from dektools.output import pprint, obj2str
from dektools.net import get_available_port
from dektools.func import FuncAnyArgs
from dektools.fetch import download_file
from dektools.download import download_from_http
from dektools.ps.process import process_detail, process_kill, process_list_all
from dektools.time import now
from dektools.str import shlex_split, shlex_quote
from dektools.shell import shell_wrapper, is_user_admin
from dektools.match import GeneralMatcher, glob2re, glob_compile, glob_match
from dektools.git import git_clean_dir, git_apply, git_parse_modules, git_fetch_min, git_list_remotes
from ...utils.beep import sound_notify
from ..markers.base.core import MarkerBase, get_inner_vars
from ..markers.invoke import InvokeMarker, GotoMarker
from ..redirect import search_bin_by_path_tree


def _is_true(x):
    if isinstance(x, str):
        x = x.lower()
    return x not in {'false', '0', 'none', 'null', '', ' ', False, 0, None, b'', b'\0'}


def _parent_dir(path, num=1):
    cursor = path
    for i in range(int(num)):
        cursor = os.path.dirname(cursor)
    return cursor


def _list_dir_one(path, file):
    path = normal_path(path)
    for item in os.listdir(path):
        result = os.path.join(path, item)
        if file is None:
            return result
        elif file:
            if os.path.isfile(result):
                return result
        else:
            if os.path.isdir(result):
                return result


def _iter_dir(path, file):
    path = normal_path(path)
    for item in os.listdir(path):
        result = os.path.join(path, item)
        if file is None:
            yield result
        elif file:
            if os.path.isfile(result):
                yield result
        else:
            if os.path.isdir(result):
                yield result


def _tree(*args):
    if len(args) == 1:
        if isinstance(args[0], int):
            tree(None, *args)
        else:
            tree(*args)
    else:
        tree(*args)
    return ''


def _sure_and_clear(path):
    path = normal_path(path)
    sure_dir(path)
    clear_dir(path)


def _remove_path(path):
    if isinstance(path, (str, os.PathLike)):
        remove_path(path)
    else:
        for item in path:
            _remove_path(item)


_xeval_default = object()


def _xeval(expression, default=_xeval_default, translate=False):
    context = get_inner_vars('__inner_context__', full=True)
    try:
        return MarkerBase.eval_mixin(context, expression, translate)
    except NameError:
        if default is _xeval_default:
            raise
        else:
            return default


def _install(name):
    def posix(exe):
        s = f"{exe} install -y {name}"
        if is_user_admin():
            s = 'sudo ' + command
        return s

    if shutil.which('apt-get'):
        command = posix('apt-get')
    elif shutil.which('yum'):
        command = posix('yum')
    elif shutil.which('brew'):
        command = f"brew install {name}"
    elif shutil.which('choco'):
        command = f"choco install -y {name}"
    else:
        raise FileNotFoundError(f"Can't find a valid installer to install {name}")
    shell_wrapper(command)


path_common_methods = {
    'cd': os.chdir,
    'cwd': lambda: os.getcwd(),
    'which': lambda *x: which(*x) or '',
    'where': lambda *x: where(*x) or '',
    'which_list': which_list,
    'where_list': where_list,
    'pybin': lambda x, p=None: search_bin_by_path_tree(p or os.getcwd(), x, False),
}

default_methods = {
    'reduce': reduce,
    'chain': chain,
    'xeval': _xeval,
    'echo': lambda *x, **y: print(*x, **dict(flush=True) | y),
    'echos': lambda *x, **y: print(*x, **dict(end='', flush=True) | y),
    'echox': lambda *x, **y: print(*x, **dict(file=sys.stderr, flush=True) | y),
    'pprint': pprint,
    'o2s': obj2str,
    'now': now,
    'getpass': getpass.getpass,
    'install': _install,
    'Path': Path,
    'path': {
        **path_common_methods,
        'tree': _tree,
        'exists': os.path.exists,
        'parent': _parent_dir,
        'abs': normal_path,
        'rel': os.path.relpath,
        'fullname': os.path.basename,
        'name': lambda x: split_ext(x)[0],
        'ext': path_ext,
        'desc': format_path_desc,
        'md': lambda x: sure_dir(normal_path(x)),
        'mdp': lambda x: sure_parent_dir(normal_path(x)),
        'mdt': lambda x=None: tempfile.mkdtemp(prefix=x),
        'mdc': _sure_and_clear,

        'lsa': lambda path='.', file=None: list(_iter_dir(path, file)),
        'lso': lambda path='.', file=None: _list_dir_one(path, file) or '',
        'ls': lambda x='.': os.listdir(x),

        'iglob': iglob,
        'glob': lambda *args, **kwargs: list(iglob(*args, **kwargs)),

        'rm': _remove_path,
        'wf': write_file,
        'rt': read_text,
        'rf': read_file,
        'ci': copy_recurse_ignore,

        'sf': split_file,
        'sfr': remove_split_files,
        'sfm': meta_split_file,
        'sfc': combine_split_files,

        'hash': lambda x, name='sha256', args=None: hash_file(name, x, args=args),
    },
    **path_common_methods,
    'pu': {
        'ps': process_list_all,
        'kill': process_kill,
        'pi': process_detail,
    },

    'sys': {
        'utf8': lambda: sys.stdout.reconfigure(encoding='utf-8')
    },

    'compress': compress_files,
    'decompress': decompress_files,

    'func': FuncAnyArgs,

    'me': lambda x: x,
    'first': lambda x: x[0] if x else None,
    'true': lambda x=True: _is_true(x),
    'false': lambda x=False: not _is_true(x),

    'equal': lambda x, y: x == y,
    'notequal': lambda x, y: x != y,
    'beep': lambda x=True: sound_notify(x),

    'invoke': lambda __placeholder__filepath, *args, **kwargs: InvokeMarker.execute_file(
        None, __placeholder__filepath, args, kwargs),
    'goto': lambda __placeholder__filepath, *args, **kwargs: GotoMarker.execute_file(
        None, __placeholder__filepath, args, kwargs),

    'glob': {
        're': glob2re,
        'compile': glob_compile,
        'match': glob_match,
        'matcher': GeneralMatcher,
    },

    'shlex': {
        'split': shlex_split,
        'quote': shlex_quote,
    },

    'net': {
        'port': get_available_port,
        'fetch': download_file,
        'download': download_from_http,
    },

    'git': {
        'apply': git_apply,
        'remotes': git_list_remotes,
        'modules': git_parse_modules,
        'fetch': git_fetch_min,
        'clean': git_clean_dir,
    }
}
