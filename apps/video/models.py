#coding: utf-8

import os
import re
from os.path import isfile
from os.path import isdir
from camsViewer import settings

class Link(object):
    name = None
    url = None
    type = None
    available_type = [
        'dir',
        'file'
    ]

    def __init__(self, name, type, url=None):
        self.name = name
        if type in self.available_type:
            self.type = type
        else:
            raise TypeError
        if url:
            self.url = url

    def to_dict(self):
        return dict(name=self.name, type=self.type, url=self.url)

    def __unicode__(self):
        return ", ".join((self.name, self.type))

    def __repr__(self):
        return self.__unicode__()

    def __eq__(self, other):
        return self.name == other.name and self.type == other.type\
            and self.url == other.url


#todo рекурсивный поиск видео
class FsModel(object):
    """simple file browser

    search files with math in extension
    """
    extensions = ('.avi', '.mp4')
    exclude = ('^\.',)
    root = settings.VIDEO_ROOT
    url_prefix = settings.VIDEO_URL_PREFIX
    cwd = None

    def __init__(self):
        self.cwd = self.root
        self._prepare_patterns()

    def _prepare_patterns(self):
        self.exclude = map(lambda pattern: re.compile(pattern), self.exclude)

    @property
    def all(self):
        path = os.path.join(self.root, self.cwd)
        return os.listdir(path)

    @property
    def folders(self):
        def is_dir(path):
            return isdir(os.path.join(self.cwd, path))
        def is_exc(path):
            return any(map(lambda pattern: re.match(pattern, path), self.exclude))
        return (path for path in self.all if is_dir(path) and not is_exc(path))

    @property
    def files(self):
        def ext_check(path):
            return any(map(lambda e: path.endswith(e), self.extensions))
        def is_file(path):
            return isfile(os.path.join(self.cwd, path))
        return [path for path in self.all if ext_check(path) and is_file(path)]

    @property
    def dir(self):
        listdir = self.folders + self.files
        listdir.sort()
        return listdir

    @property
    def back_path(self):
        cwd = self.cwd
        back_steps = list()
        while not os.path.samefile(cwd, self.root):
            cwd, path = os.path.split(cwd)
            back_steps.append(path)
        back_steps.reverse()
        return back_steps

    def into(self, folder=None):
        def into_folder(folder):
            new_cwd = os.path.join(self.cwd, folder)
            if folder and folder != '..' and os.path.isdir(new_cwd):
                self.cwd = new_cwd
            elif folder == '..':
                self.back()
        if folder:
            map(lambda folder: into_folder(folder), folder.split('/'))
        else:
            self.to_root()

    def back(self):
        if not os.path.samefile(self.root, self.cwd):
            self.cwd, back = os.path.split(self.cwd)

    def to_root(self):
        self.cwd = self.root


class FsUrlModel(FsModel):
    @property
    def dir_url(self):
        list_links = self.folders_url + self.files_url
        list_links.sort(key=lambda link: link.name)
        return list_links

    @property
    def files_url(self):
        def to_url(path):
            path = os.path.join(self.cwd, path)
            return path.replace(self.root, self.url_prefix)
        files = self.files
        urls = map(lambda path: to_url(path), files)
        return map(lambda name, url: Link(name, 'file', url), files, urls)

    @property
    def folders_url(self):
        return map(lambda name: Link(name, 'dir'), self.folders)