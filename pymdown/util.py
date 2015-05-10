#!/usr/bin/env python
"""
Uitl

PyMdown file utillity library.

Licensed under MIT
Copyright (c) 2014 Isaac Muse <isaacmuse@gmail.com>
"""
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
import sys
import traceback
import codecs
import re
import yaml
import os
import subprocess
import webbrowser
import json
import os.path as path
from . import logger
from .compat import PLATFORM, to_unicode
from collections import OrderedDict

RESOURCE_PATH = path.abspath(path.join(path.dirname(__file__), ".."))
WIN_DRIVE = re.compile(r"(^[A-Za-z]{1}:(?:\\|/))")
DATA_FOLDER = "pymdown/data"
DEFAULT_CSS = "pymdown/data/default-markdown.css"
DEFAULT_TEMPLATE = "pymdown/data/default-template.html"
DEFAULT_SETTINGS = "pymdown/data/pymdown.cfg"
USER_VERSION = "pymdown/data/version.txt"
NO_COPY = ('licenses.txt',)
NO_UPDATE = (path.basename(DEFAULT_SETTINGS),)
NOT_DEFAULT = (path.basename(DEFAULT_SETTINGS), 'version.txt')

CRITIC_IGNORE = 0
CRITIC_ACCEPT = 1
CRITIC_REJECT = 2
CRITIC_VIEW = 4
CRITIC_DUMP = 8


def yaml_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    """
    Make all YAML dictionaries load as ordered Dicts.
    http://stackoverflow.com/a/21912744/3609487
    """
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping
    )

    return yaml.load(stream, OrderedLoader)


def get_frontmatter(string):
    """ Get frontmatter from string """
    frontmatter = {}

    if string.startswith("---"):
        m = re.search(r'^(---(.*?)---\r?\n)', string, re.DOTALL)
        if m:
            try:
                frontmatter = yaml_load(m.group(2))
            except:
                logger.Log.error(traceback.format_exc())
                pass
            string = string[m.end(1):]

    return frontmatter, string


def _get_encoding(enc):
    """ Check if encoding exists else return utf-8 """
    try:
        codecs.lookup(enc)
    except LookupError:
        enc = 'utf-8'
    return enc


def splitenc(entry, default='utf-8'):
    """ Split encoding from file name """
    parts = entry.split(';')
    if len(parts) > 1:
        entry = ';'.join(parts[:-1])
        encoding = _get_encoding(parts[-1])
    else:
        encoding = _get_encoding(default)
    return entry, encoding


def is_absolute(pth):
    """ Check if path is an absolute path. """
    absolute = False
    if pth is not None:
        if sys.platform.startswith('win'):
            if WIN_DRIVE.match(pth) is not None or pth.startswith("//"):
                absolute = True
        elif pth.startswith('/'):
            absolute = True
    return absolute


def get_user_path():
    """
    Get user data path
    """

    if PLATFORM == "windows":
        folder = path.expanduser("~\\.PyMdown")
    elif PLATFORM == "osx":
        folder = path.expanduser("~/.PyMdown")
    elif PLATFORM == "linux":
        folder = path.expanduser("~/.config/PyMdown")

    if not path.exists(folder):
        try:
            os.mkdir(folder)
        except:
            pass

    defaults = path.join(folder, 'default')
    if not path.exists(defaults):
        try:
            os.mkdir(defaults)
        except:
            pass

    return folder


def update_user_files():
    """ See if user data files should be updated """
    user_ver_file = path.join(get_user_path(), 'version.txt')
    ver = load_text_resource(USER_VERSION, internal=True)
    if ver is not None:
        try:
            current_ver = yaml_load(ver).get('version', 0)
        except:
            current_ver = 0
    try:
        with codecs.open(user_ver_file, 'r', encoding='utf-8') as f:
            user_ver = yaml_load(f.read()).get('version', 0)
    except:
        user_ver = 0

    return current_ver != user_ver


def unpack_user_files():
    """ Unpack user data files """
    user_path = get_user_path()
    folder = resource_exists(DATA_FOLDER, internal=True, dir=True)
    should_update = update_user_files()
    if folder is not None:
        for f in os.listdir(folder):
            if f in NOT_DEFAULT:
                dest = path.join(user_path, path.basename(f))
            else:
                dest = path.join(user_path, 'default', path.basename(f))
            source = path.join(folder, f)
            if path.isfile(source) and f not in NO_COPY:
                if not path.exists(dest) or (should_update and f not in NO_UPDATE):
                    text = load_text_resource(source, internal=True)
                    if text is not None:
                        try:
                            with codecs.open(dest, "w", encoding='utf-8') as f:
                                f.write(text)
                        except:
                            pass


def load_egg_resources():
    """
    Add egg to system path if the name indicates it
    is for the current python version and for pymdown.
    This only runs if we are not in a pyinstaller environment.
    """
    if (
        not bool(getattr(sys, "frozen", 0)) and
        path.exists('eggs') and not path.isfile('eggs')
    ):
        egg_extension = "py%d.%d.egg" % (
            sys.version_info.major, sys.version_info.minor
        )
        egg_start = "pymdown"
        for f in os.listdir("eggs"):
            target = path.abspath(path.join('eggs', f))
            if (
                path.isfile(target) and f.endswith(egg_extension) and
                f.startswith(egg_start)
            ):
                sys.path.append(target)


def resource_exists(*args, **kwargs):
    """ If resource could be found return path else None """

    if kwargs.get('internal', False):
        base = None
        if getattr(sys, "frozen", 0):
            base = sys._MEIPASS
        else:
            base = RESOURCE_PATH

        pth = path.join(base, *args)
    else:
        pth = path.join(*args)

    directory = kwargs.get('dir', False)

    if not path.exists(pth) or (not path.isfile(pth) if not directory else path.isfile(pth)):
        pth = None

    return pth


def load_text_resource(*args, **kwargs):
    """ Load text resource from either the package source location """
    pth = resource_exists(*args, **kwargs)

    encoding = _get_encoding(kwargs.get('encoding', 'utf-8'))

    data = None
    if pth is not None:
        try:
            with codecs.open(pth, "rb") as f:
                data = f.read().decode(encoding).replace('\r', '')
        except:
            logger.Log.debug(traceback.format_exc())
            pass
    return data


def get_references(references, basepath, encoding):
    """ Get footnote and general references from outside source """

    text = ''
    for file_name in references:
        file_name, encoding = splitenc(file_name, default=encoding)
        user_path = path.join(get_user_path(), file_name)

        is_abs = is_absolute(file_name)

        # Find path relative to basepath or global user path
        # If basepath is defined set paths relative to the basepath if possible
        # or just keep the absolute
        if not is_abs:
            # Is relative path
            base_temp = path.normpath(path.join(basepath, file_name)) if basepath is not None else None
            user_temp = path.normpath(path.join(user_path, file_name)) if user_path is not None else None
            if base_temp is not None and path.exists(base_temp) and path.isfile(base_temp):
                ref_path = base_temp
            elif user_temp is not None and path.exists(user_temp) and path.isfile(user_temp):
                ref_path = user_temp
            else:
                # Is an unknown path
                ref_path = None
        elif is_abs and path.exists(file_name) and path.isfile(file_name):
            # Is absolute path
            ref_path = file_name
        else:
            # Is an unknown path
            ref_path = None

        if ref_path is not None:
            text += load_text_resource(ref_path, encoding=encoding)
        else:
            logger.Log.error("Could not find reference file %s!" % file_name)
    return text


def open_in_browser(name):
    """ Auto open HTML """

    # Here is an attempt to load the HTML in the
    # the default browser.  I guess if this doesn't work
    # I could always just inlcude the desktop lib.
    if PLATFORM == "osx":
        web_handler = None
        try:
            launch_services = path.expanduser('~/Library/Preferences/com.apple.LaunchServices/com.apple.launchservices.secure.plist')
            if not path.exists(launch_services):
                launch_services = path.expanduser('~/Library/Preferences/com.apple.LaunchServices.plist')
            with open(launch_services, "rb") as f:
                content = f.read()
            args = ["plutil", "-convert", "json", "-o", "-", "--", "-"]
            p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            p.stdin.write(content)
            out, err = p.communicate()
            plist = json.loads(to_unicode(out))
            for handler in plist['LSHandlers']:
                print('found')
                if handler.get('LSHandlerURLScheme', '') == "http":
                    web_handler = handler.get('LSHandlerRoleAll', None)
                    break
        except:
            pass
        if web_handler is not None:
            subprocess.Popen(['open', '-b', web_handler, name])
        else:
            subprocess.Popen(['open', name])
    elif PLATFORM == "windows":
        webbrowser.open(name, new=2)
    else:
        try:
            # Maybe...?
            subprocess.Popen(['xdg-open', name])
        except OSError:
            webbrowser.open(name, new=2)
            # Well we gave it our best...


def resolve_destination(out_name, file_name, critic_mode=0, batch=False):
    """ Get the path to output the file. """

    critic_enabled = critic_mode & (CRITIC_ACCEPT | CRITIC_REJECT | CRITIC_VIEW)
    output = None
    if out_name is not None:
        out_name = path.expanduser(out_name)
    if not batch:
        if out_name is not None:
            name = path.abspath(out_name)
            if path.isdir(out_name):
                logger.Log.error("'%s' is a directory!" % name)
            elif path.exists(path.dirname(name)):
                output = name
            else:
                logger.Log.error("'%s' directory does not exist!" % name)
    else:
        name = path.abspath(file_name)
        if critic_mode & CRITIC_DUMP and critic_enabled:
            if critic_mode & CRITIC_REJECT:
                label = ".rejected"
            elif critic_mode & CRITIC_ACCEPT:
                label = ".accepted"
            else:
                label = '.view'
            base, ext = path.splitext(path.abspath(file_name))
            output = path.join(name, "%s%s%s" % (base, label, ext))
        else:
            output = path.join(name, "%s.html" % path.splitext(path.abspath(file_name))[0])

    return output


def resolve_base_path(basepath, file_name, is_stream=False):
    """ Get the relative path to use when resolving relative paths if possible """
    if basepath is not None:
        basepath = path.expanduser(basepath)
    if basepath is not None and path.exists(basepath):
        # A valid path was fed in
        pth = basepath
        basepath = path.dirname(path.abspath(pth)) if path.isfile(pth) else path.abspath(pth)
    elif not is_stream:
        # Use the current file path
        basepath = path.dirname(path.abspath(file_name))
    else:
        # Okay, there is no way to tell the orign.
        # We are probably a stream that has no specified
        # physical location.
        basepath = None

    return basepath


def resolve_relative_path(relpath):
    """ Get the relative path to use when resolving relpath paths if possible. """
    if relpath is not None:
        relpath = path.expanduser(relpath)
    if relpath is not None and path.exists(relpath):
        # A valid path was fed in
        pth = relpath
        relpath = path.dirname(path.abspath(pth)) if path.isfile(pth) else path.abspath(pth)
    else:
        # Okay, there is no way to tell the orign.
        # We are probably a stream that has no specified
        # physical location.
        relpath = None

    return relpath


def resolve_meta_path(target, basepath):
    """
    Resolve the path returned in the meta data.
    1. See if path is defined as absolute and if so see
       if it exists
    2. If relative, use the file's basepath (default its physical directory
       if available) if the file
       can be found
    """
    if target is not None:
        target = path.expanduser(target)
        if not is_absolute(target):
            new_target = None
            if basepath is not None:
                temp = path.join(basepath, target)
                if path.exists(temp):
                    new_target = temp
            target = new_target
        elif not path.exists(target):
            target = None
    return target