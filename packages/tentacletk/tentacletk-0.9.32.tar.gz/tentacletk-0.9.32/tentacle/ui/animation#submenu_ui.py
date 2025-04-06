# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'animation#submenu.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from widgets.pushbutton import PushButton


class Ui_QtUi(object):
    def setupUi(self, QtUi):
        if not QtUi.objectName():
            QtUi.setObjectName(u"QtUi")
        QtUi.setEnabled(True)
        QtUi.resize(600, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(QtUi.sizePolicy().hasHeightForWidth())
        QtUi.setSizePolicy(sizePolicy)
        QtUi.setMinimumSize(QSize(0, 0))
        QtUi.setMaximumSize(QSize(600, 600))
        QtUi.setCursor(QCursor(Qt.ArrowCursor))
        QtUi.setToolButtonStyle(Qt.ToolButtonIconOnly)
        QtUi.setTabShape(QTabWidget.Triangular)
        QtUi.setDockNestingEnabled(True)
        QtUi.setDockOptions(QMainWindow.AllowNestedDocks|QMainWindow.AllowTabbedDocks|QMainWindow.AnimatedDocks|QMainWindow.ForceTabbedDocks)
        self.widget = QWidget(QtUi)
        self.widget.setObjectName(u"widget")
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.i013 = QPushButton(self.widget)
        self.i013.setObjectName(u"i013")
        self.i013.setGeometry(QRect(265, 290, 66, 21))
        self.i013.setMinimumSize(QSize(0, 21))
        self.i013.setMaximumSize(QSize(999, 21))
        self.i024 = QPushButton(self.widget)
        self.i024.setObjectName(u"i024")
        self.i024.setGeometry(QRect(150, 330, 66, 21))
        self.i024.setMinimumSize(QSize(0, 21))
        self.i024.setMaximumSize(QSize(999, 21))
        self.i020 = QPushButton(self.widget)
        self.i020.setObjectName(u"i020")
        self.i020.setGeometry(QRect(140, 260, 106, 21))
        self.i020.setMinimumSize(QSize(0, 21))
        self.i020.setMaximumSize(QSize(999, 21))
        self.i016 = QPushButton(self.widget)
        self.i016.setObjectName(u"i016")
        self.i016.setGeometry(QRect(160, 290, 66, 21))
        self.i016.setMinimumSize(QSize(0, 21))
        self.i016.setMaximumSize(QSize(999, 21))
        self.b000 = QPushButton(self.widget)
        self.b000.setObjectName(u"b000")
        self.b000.setEnabled(True)
        self.b000.setGeometry(QRect(295, 250, 91, 20))
        self.b000.setMinimumSize(QSize(0, 20))
        self.b000.setMaximumSize(QSize(999, 20))
        self.b000.setIconSize(QSize(18, 18))
        self.tb000 = PushButton(self.widget)
        self.tb000.setObjectName(u"tb000")
        self.tb000.setGeometry(QRect(200, 220, 119, 20))
        self.tb000.setMinimumSize(QSize(0, 20))
        self.tb000.setMaximumSize(QSize(999, 20))
        self.tb000.setCheckable(True)
        self.i027 = QPushButton(self.widget)
        self.i027.setObjectName(u"i027")
        self.i027.setGeometry(QRect(230, 330, 51, 21))
        self.i027.setMinimumSize(QSize(0, 21))
        self.i027.setMaximumSize(QSize(999, 21))
        self.i027_2 = QPushButton(self.widget)
        self.i027_2.setObjectName(u"i027_2")
        self.i027_2.setGeometry(QRect(290, 330, 76, 21))
        self.i027_2.setMinimumSize(QSize(0, 21))
        self.i027_2.setMaximumSize(QSize(999, 21))
        QtUi.setCentralWidget(self.widget)

        self.retranslateUi(QtUi)

        QMetaObject.connectSlotsByName(QtUi)
    # setupUi

    def retranslateUi(self, QtUi):
#if QT_CONFIG(whatsthis)
        QtUi.setWhatsThis(QCoreApplication.translate("QtUi", u"main", None))
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(whatsthis)
        self.i013.setWhatsThis(QCoreApplication.translate("QtUi", u"animation", None))
#endif // QT_CONFIG(whatsthis)
        self.i013.setText(QCoreApplication.translate("QtUi", u"Animation", None))
#if QT_CONFIG(whatsthis)
        self.i024.setWhatsThis(QCoreApplication.translate("QtUi", u"vfx", None))
#endif // QT_CONFIG(whatsthis)
        self.i024.setText(QCoreApplication.translate("QtUi", u"Vfx", None))
#if QT_CONFIG(whatsthis)
        self.i020.setWhatsThis(QCoreApplication.translate("QtUi", u"deformation", None))
#endif // QT_CONFIG(whatsthis)
        self.i020.setText(QCoreApplication.translate("QtUi", u"Deformation", None))
#if QT_CONFIG(whatsthis)
        self.i016.setWhatsThis(QCoreApplication.translate("QtUi", u"rigging", None))
#endif // QT_CONFIG(whatsthis)
        self.i016.setText(QCoreApplication.translate("QtUi", u"Rigging", None))
#if QT_CONFIG(tooltip)
        self.b000.setToolTip(QCoreApplication.translate("QtUi", u"Delete keys for the currently selected object(s).", None))
#endif // QT_CONFIG(tooltip)
        self.b000.setText(QCoreApplication.translate("QtUi", u"Delete Keys", None))
#if QT_CONFIG(tooltip)
        self.tb000.setToolTip(QCoreApplication.translate("QtUi", u"<html><head/><body><p>Set the current frame on the timeslider.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.tb000.setText(QCoreApplication.translate("QtUi", u"Move to Frame", None))
#if QT_CONFIG(whatsthis)
        self.i027.setWhatsThis(QCoreApplication.translate("QtUi", u"key", None))
#endif // QT_CONFIG(whatsthis)
        self.i027.setText(QCoreApplication.translate("QtUi", u"Key", None))
#if QT_CONFIG(whatsthis)
        self.i027_2.setWhatsThis(QCoreApplication.translate("QtUi", u"skeleton", None))
#endif // QT_CONFIG(whatsthis)
        self.i027_2.setText(QCoreApplication.translate("QtUi", u"Skeleton", None))
    # retranslateUi

