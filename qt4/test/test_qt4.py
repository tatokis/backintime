# Back In Time
# Copyright (C) 2016 Taylor Raack
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public Licensealong
# with this program; if not, write to the Free Software Foundation,Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import sys
import unittest

from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))

import app
import config
import guiapplicationinstance
import qt4tools

# UI test basics taken from http://johnnado.com/pyqt-qtest-example/

# Instance does nothing, but provides methods for app to call into
class DummyInstance:
    def test(self):
        return True
    
    def raise_command(self):
        i = True

cfg = config.Config()
qapp = qt4tools.create_qapplication(cfg.APP_NAME)

class TestQT4(unittest.TestCase):
    def setUp(self):
        super(TestQT4, self).setUp()
        dummyAppInstance = DummyInstance()
        raise_cmd = ''
        self.dummyAppInstance = guiapplicationinstance.GUIApplicationInstance( cfg.get_app_instance_file(), raise_cmd )
        self.mainWindow = app.MainWindow(cfg, dummyAppInstance, qapp)

    def tearDown(self):
        self.dummyAppInstance.exit_application()
        unittest.TestCase.tearDown(self)

    def test_settingsWindowAppears(self):
        # create the main window
        self.mainWindow.show()
        QTest.qWaitForWindowShown(self.mainWindow)

        # simulate a button click to open the settings dialog
        QTest.mouseClick(self.mainWindow.main_toolbar.widgetForAction(self.mainWindow.btn_settings), Qt.LeftButton)
        QTest.qWaitForWindowShown(self.mainWindow.settingsDialog)
        settingsDialog = self.mainWindow.settingsDialog

        # very basic verification - can add more verifications / actions on the dialog later
        # is the title correct?
        self.assertEqual("Settings", settingsDialog.windowTitle())

        # now close the settings dialog
        okWidget = settingsDialog.button_box.button(settingsDialog.button_box.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
