#coding: utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from apps.video.models import FsUrlModel
from apps.video.models import Link


class ModelsTest(TestCase):

    move = [
       'Dropbox/job',
       'Dropbox',
       'job',
       '..' ,
       'Dropbox/job/..',
       'lounge3-1'
    ]
    exp_path = [
        '/home/ridhid/Dropbox/job',
        '/home/ridhid/Dropbox',
        '/home/ridhid',
        '/home/ridhid',
        '/home/ridhid/Dropbox',
        '/home/ridhid/lounge3-1'
    ]
    exp_back_path = [
        ['Dropbox', 'job'],
        ['Dropbox'],
        [],
        [],
        ['Dropbox'],
        ['lounge3-1'],
    ]
    exp_back = [
        '/home/ridhid/Dropbox',
        '/home/ridhid',
        '/home/ridhid',
        '/home/ridhid',
        '/home/ridhid',
        '/home/ridhid'
    ]
    exp_dirs = [
        ['preRecord', 'mfc_site', 'camera_parser', 'mfc', 'Backup', 'smev', 'queue'],
        ['\xd0\x94\xd0\xb8\xd0\xbf\xd0\xbb\xd0\xbe\xd0\xbc', 'scripts', 'Uml', 'job', '.dropbox.cache', 'Camera Uploads', 'MimeCart', 'XMind', '\xd0\x9f\xd0\xb8\xd0\xba\xd1\x87\xd0\xb8', 'games', 'tools', '\xd1\x84\xd0\xb8\xd0\xbd\xd0\xb0\xd0\xbb', 'Backup', 'All projects', 'books', '\xd0\xa0\xd0\xb0\xd0\xb7\xd0\xbd\xd0\xbe\xd0\xb5', 'Diplom'],
        ['.pip', '\xd0\xa0\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x87\xd0\xb8\xd0\xb9 \xd1\x81\xd1\x82\xd0\xbe\xd0\xbb', 'lounge3-1', '.dropbox-dist', '.npm', 'PycharmProjects', '\xd0\x94\xd0\xbe\xd0\xba\xd1\x83\xd0\xbc\xd0\xb5\xd0\xbd\xd1\x82\xd1\x8b', '\xd0\xa5\xd0\xbb\xd0\xb0\xd0\xbc', '.thumbnails', '.kde', 'workspace', '.dbus', '.local', '.rpmdb', '\xd0\x9e\xd0\xb1\xd1\x89\xd0\xb5\xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xbd\xd1\x8b\xd0\xb5', '.java', '.bower', 'third_party', '.ssh', '.PyCharm20', 'Dropbox', 'local', '\xd0\x9c\xd1\x83\xd0\xb7\xd1\x8b\xd0\xba\xd0\xb0', '\xd0\xa8\xd0\xb0\xd0\xb1\xd0\xbb\xd0\xbe\xd0\xbd\xd1\x8b', '.dropbox', '.xmind', '.macromedia', '.mozilla', '\xd0\x92\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe', '.adobe', '\xd0\x97\xd0\xb0\xd0\xb3\xd1\x80\xd1\x83\xd0\xb7\xd0\xba\xd0\xb8', '.psi', '.gconf', '.config', '.gstreamer-0.10', '\xd0\x98\xd0\xb7\xd0\xbe\xd0\xb1\xd1\x80\xd0\xb0\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f', '.virtualenv', 'tmp', '.cache', '.pki'],
        ['.pip', '\xd0\xa0\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x87\xd0\xb8\xd0\xb9 \xd1\x81\xd1\x82\xd0\xbe\xd0\xbb', 'lounge3-1', '.dropbox-dist', '.npm', 'PycharmProjects', '\xd0\x94\xd0\xbe\xd0\xba\xd1\x83\xd0\xbc\xd0\xb5\xd0\xbd\xd1\x82\xd1\x8b', '\xd0\xa5\xd0\xbb\xd0\xb0\xd0\xbc', '.thumbnails', '.kde', 'workspace', '.dbus', '.local', '.rpmdb', '\xd0\x9e\xd0\xb1\xd1\x89\xd0\xb5\xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xbd\xd1\x8b\xd0\xb5', '.java', '.bower', 'third_party', '.ssh', '.PyCharm20', 'Dropbox', 'local', '\xd0\x9c\xd1\x83\xd0\xb7\xd1\x8b\xd0\xba\xd0\xb0', '\xd0\xa8\xd0\xb0\xd0\xb1\xd0\xbb\xd0\xbe\xd0\xbd\xd1\x8b', '.dropbox', '.xmind', '.macromedia', '.mozilla', '\xd0\x92\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe', '.adobe', '\xd0\x97\xd0\xb0\xd0\xb3\xd1\x80\xd1\x83\xd0\xb7\xd0\xba\xd0\xb8', '.psi', '.gconf', '.config', '.gstreamer-0.10', '\xd0\x98\xd0\xb7\xd0\xbe\xd0\xb1\xd1\x80\xd0\xb0\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f', '.virtualenv', 'tmp', '.cache', '.pki'],
        ['\xd0\x94\xd0\xb8\xd0\xbf\xd0\xbb\xd0\xbe\xd0\xbc', 'scripts', 'Uml', 'job', '.dropbox.cache', 'Camera Uploads', 'MimeCart', 'XMind', '\xd0\x9f\xd0\xb8\xd0\xba\xd1\x87\xd0\xb8', 'games', 'tools', '\xd1\x84\xd0\xb8\xd0\xbd\xd0\xb0\xd0\xbb', 'Backup', 'All projects', 'books', '\xd0\xa0\xd0\xb0\xd0\xb7\xd0\xbd\xd0\xbe\xd0\xb5', 'Diplom'],
        [],
    ]
    exp_files = [
        [],
        [],
        ["Bestamvsofalltime_Binary_Overdrive_AMV.mp4"],
        ["Bestamvsofalltime_Binary_Overdrive_AMV.mp4"],
        [],
        ['lounge3-1 19:19:32.avi', 'lounge3-2 19:19:32.avi']
    ]
    exp_urls = [
        [],
        [],
        [],
        [],
        [],
        [
            Link('lounge3-1 19:19:32.avi', 'file', '/media/lounge3-1/lounge3-1 19:19:32.avi'),
            Link('lounge3-2 19:19:32.avi', 'file', '/media/lounge3-1/lounge3-2 19:19:32.avi')
        ]
    ]

    def setUp(self):
        self.fs = FsUrlModel()

    def test_moving(self):
        def test(path, equal):
            self.fs.into(path)
            self.assertEqual(self.fs.cwd, equal)
            self.fs.to_root()

        map(lambda path, equal: test(path, equal), self.move, self.exp_path)

    def test_back(self):
        def test(path, equal):
            self.fs.into(path)
            self.fs.back()
            self.assertEqual(self.fs.cwd, equal)
            self.fs.to_root()

        map(lambda path, equal: test(path, equal), self.move, self.exp_back)

    def test_back_path(self):
        def test(path, equal):
            self.fs.into(path)
            self.assertListEqual(self.fs.back_path, equal)
            self.fs.to_root()

        map(lambda path, equal: test(path, equal), self.move, self.exp_back_path)

    def test_files(self):
        def test(path, equal):
            self.fs.into(path)
            self.assertListEqual(self.fs.files, equal)
            self.fs.to_root()

        map(lambda path, equal: test(path, equal), self.move, self.exp_files)

    # def test_to_urls(self):
    #     def test(path, equal):
    #         self.fs.into(path)
    #         self.assertListEqual(self.fs.files_url, equal)
    #         self.fs.to_root()
    #
    #     map(lambda path, equal: test(path, equal), self.move, self.exp_urls)

    def test_dir_url(self):
        self.fs.into('lounge3-1')
        self.assertNotEqual(self.fs.dir_url, None)

class ViewFSCase(TestCase):
    client = Client()

    def test_view_fs(self):
        url = reverse('video')
        response = self.client.get(url)
        self.assertContains(response, '/static', status_code=200)

    def test_view_fs_AJAX(self):
        args = (
            dict(format='json', path="Dropbox"),
            dict(format='json', path="Dropbox/job"),
            dict(format='json', path="/Dropbox/job"),
            dict(format='json', path="/Dropbox", page=1),
            # dict(format='json', path="", page=2),
        )
        url = reverse('video')
        for arg_set in args:
            response = self.client.get(url, arg_set)
            self.assertEqual(response.status_code, 200)
            print response.content
