# PyQt6 compatibility layer that exposes a PyQt5-like API for HPLIP's ui5.
# Upstream still ships PyQt5-only UI code; this keeps that code working on Qt 6.

from __future__ import annotations

import enum
import locale as _locale

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import *  # noqa: F401,F403
from PyQt6.QtGui import *  # noqa: F401,F403
from PyQt6.QtWidgets import *  # noqa: F401,F403
from PyQt6.QtCore import pyqtSignal, pyqtSlot, pyqtProperty  # noqa: F401
from PyQt6.QtCore import PYQT_VERSION_STR, qVersion  # noqa: F401

# QAction / QShortcut live in QtGui in Qt 6
QtWidgets.QAction = QtGui.QAction
if hasattr(QtGui, "QShortcut"):
	QtWidgets.QShortcut = QtGui.QShortcut


def _promote_enums(obj):
	for name in dir(obj):
		if name.startswith("_"):
			continue
		try:
			nested = getattr(obj, name)
		except Exception:
			continue
		if isinstance(nested, type) and issubclass(nested, enum.Enum):
			# __members__ includes combination aliases such as AlignCenter
			members = getattr(nested, "__members__", {})
			for item_name, item in members.items():
				if hasattr(obj, item_name):
					continue
				try:
					setattr(obj, item_name, item)
				except Exception:
					pass


def _promote_module(module):
	_promote_enums(module)
	for name in dir(module):
		if name.startswith("_"):
			continue
		try:
			obj = getattr(module, name)
		except Exception:
			continue
		if isinstance(obj, type):
			_promote_enums(obj)


for _mod in (QtCore, QtGui, QtWidgets, Qt):
	_promote_module(_mod)

# Common classes whose nested enums are used unscoped by HPLIP
for _cls in (
	QDialog, QMessageBox, QAbstractItemView, QHeaderView, QEvent,
	QSizePolicy, QFrame, QTabWidget, QComboBox, QLineEdit, QTextEdit,
	QEventLoop, QAbstractItemView, QSystemTrayIcon, QBoxLayout,
	QFormLayout, QLayout, QPainter, QImage, QFont, QPalette, QStyle,
	QApplication, QWidget, QAbstractSpinBox, QSlider, QToolButton,
	QListView, QTreeView, QTableView, QDialogButtonBox, QFileDialog,
	QProgressBar, QTextBrowser, QPlainTextEdit, QGroupBox,
):
	try:
		_promote_enums(_cls)
	except Exception:
		pass

# exec_() / exec_loop() aliases (Qt3/Qt5 names)
for _cls in (QApplication, QDialog, QMenu, QEventLoop, QMessageBox,
		QColorDialog, QFileDialog, QFontDialog, QInputDialog,
		QProgressDialog, QWizard):
	if hasattr(_cls, "exec") and not hasattr(_cls, "exec_"):
		_cls.exec_ = _cls.exec
	if hasattr(_cls, "exec") and not hasattr(_cls, "exec_loop"):
		_cls.exec_loop = _cls.exec

# qApp was a PyQt5 builtin
class _QAppProxy:
	def __getattr__(self, name):
		app = QApplication.instance()
		if app is None:
			raise RuntimeError("No QApplication instance")
		return getattr(app, name)

	def __bool__(self):
		return QApplication.instance() is not None

qApp = _QAppProxy()

# Removed / renamed Qt 6 APIs used by HPLIP
if not hasattr(QDateTime, "setTime_t"):
	QDateTime.setTime_t = QDateTime.setSecsSinceEpoch

if not hasattr(QApplication, "UnicodeUTF8"):
	QApplication.UnicodeUTF8 = 0
	QtWidgets.QApplication.UnicodeUTF8 = 0


class QTextCodec:
	@staticmethod
	def locale():
		try:
			return QLocale.system().name()
		except Exception:
			loc = _locale.getlocale()[0] or "C"
			return loc


class QStringList(list):
	pass


# Old-style SIGNAL("foo(int)") used by a few leftover emit() calls
def SIGNAL(signature):
	return signature.split("(", 1)[0].strip()


def SLOT(signature):
	return signature.split("(", 1)[0].strip()
