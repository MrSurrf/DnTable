# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'design.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDockWidget, QFrame,
    QHBoxLayout, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(727, 1165)
        MainWindow.setTabletTracking(False)
        MainWindow.setDockNestingEnabled(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 727, 21))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName(u"menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.main_map_widget = QDockWidget(MainWindow)
        self.main_map_widget.setObjectName(u"main_map_widget")
        self.main_map_widget.setMinimumSize(QSize(700, 600))
        self.main_map_widget.setMaximumSize(QSize(700, 600))
        self.main_map_widget.setFloating(False)
        self.main_map_widget.setFeatures(QDockWidget.DockWidgetMovable)
        self.dockWidgetContents_4 = QWidget()
        self.dockWidgetContents_4.setObjectName(u"dockWidgetContents_4")
        self.dockWidgetContents_4.setMinimumSize(QSize(700, 600))
        self.dockWidgetContents_4.setMaximumSize(QSize(700, 600))
        self.widget = QWidget(self.dockWidgetContents_4)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(31, 41, 301, 465))
        self.verticalLayout_6 = QVBoxLayout(self.widget)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.widget)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(291, 50))
        self.frame.setMaximumSize(QSize(291, 50))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(1)
        self.widget1 = QWidget(self.frame)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(0, 0, 291, 25))
        self.horizontalLayout_2 = QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.nextButton = QPushButton(self.widget1)
        self.nextButton.setObjectName(u"nextButton")

        self.horizontalLayout_2.addWidget(self.nextButton)

        self.prevButton = QPushButton(self.widget1)
        self.prevButton.setObjectName(u"prevButton")

        self.horizontalLayout_2.addWidget(self.prevButton)

        self.map_comboBox = QComboBox(self.widget1)
        self.map_comboBox.setObjectName(u"map_comboBox")

        self.horizontalLayout_2.addWidget(self.map_comboBox)


        self.verticalLayout_6.addWidget(self.frame)

        self.frame_2 = QFrame(self.widget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(291, 400))
        self.frame_2.setMaximumSize(QSize(291, 400))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.map_label = QLabel(self.frame_2)
        self.map_label.setObjectName(u"map_label")
        self.map_label.setGeometry(QRect(0, 0, 299, 411))

        self.verticalLayout_6.addWidget(self.frame_2)

        self.widget2 = QWidget(self.dockWidgetContents_4)
        self.widget2.setObjectName(u"widget2")
        self.widget2.setGeometry(QRect(400, 10, 293, 537))
        self.verticalLayout_7 = QVBoxLayout(self.widget2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.widget2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(291, 400))
        self.frame_3.setMaximumSize(QSize(291, 400))
        self.frame_3.setFrameShape(QFrame.Box)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.widget3 = QWidget(self.frame_3)
        self.widget3.setObjectName(u"widget3")
        self.widget3.setGeometry(QRect(0, 0, 291, 401))
        self.horizontalLayout_4 = QHBoxLayout(self.widget3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.widget3)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(200, 300))
        self.frame_5.setMaximumSize(QSize(200, 300))
        self.frame_5.setFrameShape(QFrame.Box)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.effect_label = QLabel(self.frame_5)
        self.effect_label.setObjectName(u"effect_label")
        self.effect_label.setGeometry(QRect(0, 0, 131, 41))

        self.horizontalLayout_4.addWidget(self.frame_5)

        self.effect_comboBox = QComboBox(self.widget3)
        self.effect_comboBox.setObjectName(u"effect_comboBox")
        self.effect_comboBox.setMinimumSize(QSize(75, 25))
        self.effect_comboBox.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_4.addWidget(self.effect_comboBox)


        self.verticalLayout_7.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.widget2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(291, 50))
        self.frame_4.setMaximumSize(QSize(291, 50))
        self.frame_4.setFrameShape(QFrame.Box)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.widget4 = QWidget(self.frame_4)
        self.widget4.setObjectName(u"widget4")
        self.widget4.setGeometry(QRect(0, 0, 291, 41))
        self.horizontalLayout_3 = QHBoxLayout(self.widget4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.apply_effectButton = QPushButton(self.widget4)
        self.apply_effectButton.setObjectName(u"apply_effectButton")

        self.horizontalLayout_3.addWidget(self.apply_effectButton)

        self.clean_effectButton = QPushButton(self.widget4)
        self.clean_effectButton.setObjectName(u"clean_effectButton")

        self.horizontalLayout_3.addWidget(self.clean_effectButton)


        self.verticalLayout_7.addWidget(self.frame_4)

        self.showButton = QPushButton(self.widget2)
        self.showButton.setObjectName(u"showButton")

        self.verticalLayout_7.addWidget(self.showButton)

        self.main_map_widget.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.main_map_widget)
        self.test_widget = QDockWidget(MainWindow)
        self.test_widget.setObjectName(u"test_widget")
        self.test_widget.setMinimumSize(QSize(330, 500))
        self.test_widget.setMaximumSize(QSize(330, 500))
        self.test_widget.setFloating(False)
        self.test_widget.setFeatures(QDockWidget.DockWidgetMovable)
        self.test_widget.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.dockWidgetContents_6 = QWidget()
        self.dockWidgetContents_6.setObjectName(u"dockWidgetContents_6")
        self.test_widget.setWidget(self.dockWidgetContents_6)
        MainWindow.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.test_widget)
        self.dice_widget = QDockWidget(MainWindow)
        self.dice_widget.setObjectName(u"dice_widget")
        self.dice_widget.setMinimumSize(QSize(330, 500))
        self.dice_widget.setMaximumSize(QSize(330, 500))
        self.dice_widget.setFloating(False)
        self.dice_widget.setFeatures(QDockWidget.DockWidgetMovable)
        self.dice_widget.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.dockWidgetContents_5 = QWidget()
        self.dockWidgetContents_5.setObjectName(u"dockWidgetContents_5")
        self.dice_widget.setWidget(self.dockWidgetContents_5)
        MainWindow.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.dice_widget)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u041a\u0430\u0440\u0442\u0430", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u0413\u0440\u0438\u0434", None))
        self.menu_3.setTitle(QCoreApplication.translate("MainWindow", u"\u042d\u0444\u0444\u0435\u043a\u0442\u044b", None))
        self.nextButton.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.prevButton.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.map_label.setText(QCoreApplication.translate("MainWindow", u"map", None))
        self.effect_label.setText(QCoreApplication.translate("MainWindow", u"effect", None))
        self.apply_effectButton.setText(QCoreApplication.translate("MainWindow", u"apply", None))
        self.clean_effectButton.setText(QCoreApplication.translate("MainWindow", u"clean", None))
        self.showButton.setText(QCoreApplication.translate("MainWindow", u"show", None))
    # retranslateUi

