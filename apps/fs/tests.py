#coding: utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import os
import random
from os import path
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from apps.fs.models import FsUrlModel


class FolderPoint(object):
    def __init__(self, name, parent=None, depth=6):
        self.path = name, parent
        self.depth = depth
        if depth:
            self.scan_folders()
            self.scan_files()

    @property
    def path(self):
        return path.abspath(self._path)

    @property
    def dirname(self):
        return path.dirname(self._path)

    @property
    def name(self):
        folder, name = path.split(self.path)
        return name

    @path.setter
    def path(self, args):
        name, parent = args
        if isinstance(parent, FolderPoint):
            self.parent = parent
            self._path = path.join(self.parent.path, name)
        else:
            self.parent = path.dirname(name)
            self._path = name

    def subdepth(self):
        if self.depth-1 > 0:
            subdepth = self.depth-1
        else:
            subdepth = 0
        return subdepth

    def scan_folders(self):
        depth = self.subdepth()
        subfolders = [folder for folder in os.listdir(self.path)
                        if path.isdir(path.join(self.path, folder))]
        self.subfolders = [FolderPoint(folder, self, depth) for folder
                            in subfolders]

    def scan_files(self):
        self.files = [filename for filename in os.listdir(self.path)
                        if path.isfile(path.join(self.path, filename))]

    @property
    def randint(self):
        try:
            randint = random.randint(1, len(self.subfolders)) - 1
        except ValueError as e:
            randint = 0
        return randint

    def deep(self, depth=4):
        if not hasattr(self, 'subfolders') or not self.subfolders:
            return self
        next_folder = self.subfolders[self.randint]
        if depth:
            return next_folder.deep(depth-1)
        return next_folder

    def diff(self):
        parent = self.parent
        while isinstance(parent, FolderPoint):
            parent = parent.parent
        return self.path.replace(parent+"/", "")

    def __repr__(self):
        return self.path


class ModelsTest(TestCase):

    def repeat(func, repeat=10, *args, **kwargs):
        def wrapper(*args, **kwargs):
            for i in range(0, repeat):
                func(*args, **kwargs)
        return wrapper

    def setUp(self):
        self.fs = FsUrlModel()
        self.graph = FolderPoint(self.fs.root, depth=4)

    @repeat
    def test_moving(self):
        folder = self.graph.deep()
        self.fs.into(folder.diff())
        self.assertEqual(self.fs.cwd, folder.path)
        print "cd %s and ls : %s" % (self.fs.cwd, folder.path)
        self.fs.to_root()

    @repeat
    def test_back(self):
        folder = self.graph.deep()
        self.fs.into(folder.diff())
        self.fs.back()
        self.assertEqual(self.fs.cwd, folder.parent.path)
        print "cd %s and back , pwd -> %s , actual -> %s" %\
              (folder.diff(), self.fs.cwd, folder.parent.path)
        self.fs.to_root()

    @repeat
    def test_back_path(self):
        folder = self.graph.deep()
        self.fs.into(folder.diff())
        back_path = "/".join(self.fs.back_path)
        self.assertEqual(back_path, folder.diff())
        self.fs.to_root()

    @repeat
    def test_files(self):
        folder = self.graph.deep()
        self.fs.into(folder.diff())
        self.assertListEqual(self.fs.files, folder.files)
        print "cd %s files : %s" % (folder.diff(), self.fs.files_url)
        self.fs.to_root()

    @repeat
    def test_dir_url(self):
        folder = self.graph.deep()
        self.fs.into(folder.diff())
        self.assertNotEqual(self.fs.dir_url, None)
        print "cd %s foldes : %s" % (folder.diff(), self.fs.files_url)
        self.fs.to_root()

    @repeat
    def test_files_url(self):
        folder = self.graph.deep()
        self.fs.into(folder.diff())
        self.assertNotEqual(self.fs.files_url, None)
        print "cd %s files : %s" % (folder.diff(), self.fs.files_url)
        self.fs.to_root()


class ViewFSCase(TestCase):
    client = Client()

    def test_view_fs(self):
        url = reverse('fs')
        response = self.client.get(url)
        self.assertContains(response, '/media', status_code=200)

    def test_view_fs_AJAX(self):
        args = (
            dict(format='json', path="Dropbox"),
            dict(format='json', path="Dropbox/job"),
            dict(format='json', path="/Dropbox/job"),
            dict(format='json', path="/Dropbox", page=1),
            # dict(format='json', path="", page=2),
        )
        url = reverse('fs')
        for arg_set in args:
            response = self.client.get(url, arg_set)
            self.assertEqual(response.status_code, 200)
            print response.content
