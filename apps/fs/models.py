#coding: utf-8

import os
from os.path import isfile
from os.path import isdir
from camsViewer import settings

#todo рекурсивный поиск видео
class FSModel(object):
    extensions = ('.avi',)
    root = settings.VIDEO_ROOT
    url_prefix = settings.VIDEO_URL_PREFIX
    cwd = None

    def __init__(self):
        self.cwd = self.root

    @property
    def dir(self):
        path = os.path.join(self.root, self.cwd)
        return os.listdir(path)

    @property
    def directories(self):
        return [path for path in self.dir if isdir(os.path.join(self.cwd, path))]

    @property
    def files(self):
        def ext_check(path):
            return any(map(lambda e: path.endswith(e), self.extensions))
        def is_file(path):
            return isfile(os.path.join(self.cwd, path))

        return [path for path in self.dir if ext_check(path) and is_file(path)]

    @property
    def files_url(self):
        def to_url(path):
            path = os.path.join(self.cwd, path)
            return path.replace(self.root, self.url_prefix)

        return map(lambda path: to_url(path), self.files)

    @property
    def back_path(self):
        cwd = self.cwd
        back_steps = list()
        while not os.path.samefile(cwd, self.root):
            cwd, path = os.path.split(cwd)
            back_steps.append(path)
        return back_steps

    def into(self, folder):
        def into_folder(folder):
            new_cwd = os.path.join(self.cwd, folder)
            if folder and folder != '..' and os.path.isdir(new_cwd):
                self.cwd = new_cwd
            elif folder == '..':
                self.back()
        if folder:
            map(lambda folder: into_folder(folder), folder.split('/'))

    def back(self):
        if not os.path.samefile(self.root, self.cwd):
            self.cwd, back = os.path.split(self.cwd)

    def to_root(self):
        self.cwd = self.root