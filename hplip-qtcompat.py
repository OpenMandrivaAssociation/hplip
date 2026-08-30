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

# exec_() / exec_loop() aliases (Qt3/Qt5 names).
# Assigning the SIP method itself is not a usable instance method on
# subclasses (NoDevicesDialog.exec_() would TypeError and abort).
def _exec_alias(self, *args, **kwargs):
	return self.exec(*args, **kwargs)


for _cls in (QApplication, QDialog, QMenu, QEventLoop, QMessageBox,
		QColorDialog, QFileDialog, QFontDialog, QInputDialog,
		QProgressDialog, QWizard):
	if hasattr(_cls, "exec") and not hasattr(_cls, "exec_"):
		_cls.exec_ = _exec_alias
	if hasattr(_cls, "exec") and not hasattr(_cls, "exec_loop"):
		_cls.exec_loop = _exec_alias

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
	# Assigning the SIP method itself is not a usable instance method.
	def _setTime_t(self, secs):
		return self.setSecsSinceEpoch(int(secs))

	QDateTime.setTime_t = _setTime_t

if not hasattr(QApplication, "UnicodeUTF8"):
	QApplication.UnicodeUTF8 = 0
	QtWidgets.QApplication.UnicodeUTF8 = 0

if not hasattr(QPalette, "Background") and hasattr(QPalette, "Window"):
	QPalette.Background = QPalette.Window

if not hasattr(QFontMetrics, "width") and hasattr(QFontMetrics, "horizontalAdvance"):
	def _fm_width(self, *args, **kwargs):
		return self.horizontalAdvance(*args, **kwargs)

	QFontMetrics.width = _fm_width

if not hasattr(QHeaderView, "setClickable") and hasattr(QHeaderView, "setSectionsClickable"):
	def _setClickable(self, *args, **kwargs):
		return self.setSectionsClickable(*args, **kwargs)

	QHeaderView.setClickable = _setClickable
if not hasattr(QHeaderView, "setMovable") and hasattr(QHeaderView, "setSectionsMovable"):
	def _setMovable(self, *args, **kwargs):
		return self.setSectionsMovable(*args, **kwargs)

	QHeaderView.setMovable = _setMovable
if not hasattr(QHeaderView, "setResizeMode") and hasattr(QHeaderView, "setSectionResizeMode"):
	def _setResizeMode(self, *args, **kwargs):
		return self.setSectionResizeMode(*args, **kwargs)

	QHeaderView.setResizeMode = _setResizeMode

# Qt3 QListWidget.setSelected(item, bool) — used by DevMgr5.activateDevice()
if not hasattr(QListWidget, "setSelected"):
	def _list_setSelected(self, item, selected=True):
		if item is not None:
			item.setSelected(selected)

	QListWidget.setSelected = _list_setSelected

# Qt 6 QDropEvent dropped pos(); fax address-book DnD still calls e.pos()
if not hasattr(QDropEvent, "pos") and hasattr(QDropEvent, "position"):
	def _drop_pos(self):
		return self.position().toPoint()

	QDropEvent.pos = _drop_pos

if not hasattr(QWheelEvent, "pos") and hasattr(QWheelEvent, "position"):
	def _wheel_pos(self):
		return self.position().toPoint()

	QWheelEvent.pos = _wheel_pos


class _PathResult(str):
	"""File-dialog path that is both a string (PyQt4) and indexable (PyQt5/6)."""

	def __new__(cls, path, selected_filter=""):
		obj = str.__new__(cls, path or "")
		obj._filter = selected_filter
		return obj

	def __getitem__(self, idx):
		if idx == 0:
			return str(self)
		if idx == 1:
			return self._filter
		raise IndexError(idx)

	def __iter__(self):
		yield str(self)
		yield self._filter


_orig_getOpenFileName = QFileDialog.getOpenFileName
_orig_getSaveFileName = QFileDialog.getSaveFileName


def _wrap_file_path_dialog(orig):
	def wrapped(*args, **kwargs):
		result = orig(*args, **kwargs)
		if isinstance(result, tuple):
			path = result[0] if result else ""
			filt = result[1] if len(result) > 1 else ""
			return _PathResult(path, filt)
		return _PathResult(result)

	return staticmethod(wrapped)


QFileDialog.getOpenFileName = _wrap_file_path_dialog(_orig_getOpenFileName)
QFileDialog.getSaveFileName = _wrap_file_path_dialog(_orig_getSaveFileName)


class _SignalSubscriptProxy:
	"""Restore PyQt5 signal[type] selection for overloads dropped in Qt 6."""

	def __init__(self, default, extra):
		self._default = default
		self._extra = extra

	def _resolve(self, key):
		if key in self._extra:
			return self._extra[key]
		if key is str or key == "str" or (
			isinstance(key, str) and "QString" in key
		):
			return self._extra.get(str)
		if key is int or key == "int":
			return self._extra.get(int)
		return None

	def __getitem__(self, key):
		try:
			return self._default[key]
		except KeyError:
			mapped = self._resolve(key)
			if mapped is not None:
				return mapped
			raise

	def connect(self, *args, **kwargs):
		return self._default.connect(*args, **kwargs)

	def disconnect(self, *args, **kwargs):
		return self._default.disconnect(*args, **kwargs)

	def emit(self, *args, **kwargs):
		return self._default.emit(*args, **kwargs)

	def __getattr__(self, name):
		return getattr(self._default, name)


class _RestoredSignalOverloads:
	def __init__(self, orig, extra_name):
		self._orig = orig
		self._extra_name = extra_name

	def __get__(self, obj, objtype=None):
		if obj is None:
			return self._orig
		default = self._orig.__get__(obj, objtype)
		extra = {
			str: getattr(obj, self._extra_name),
			int: default,
		}
		return _SignalSubscriptProxy(default, extra)


# Qt 6 dropped the QString overloads of these QComboBox signals.
# PyQt5 code selects them with activated[str] / currentIndexChanged[str] /
# highlighted[str]; map those back onto the Qt 6 replacements.
_QComboBox = QtWidgets.QComboBox
_QComboBox.activated = _RestoredSignalOverloads(
	_QComboBox.activated, "textActivated"
)
_QComboBox.currentIndexChanged = _RestoredSignalOverloads(
	_QComboBox.currentIndexChanged, "currentTextChanged"
)
_QComboBox.highlighted = _RestoredSignalOverloads(
	_QComboBox.highlighted, "textHighlighted"
)


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
