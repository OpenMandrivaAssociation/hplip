#!/usr/bin/python
# Offscreen smoke test for the HPLIP PyQt6 UI.
# Must be able to import HPLIP modules (PYTHONPATH) and cupsext.

from __future__ import annotations

import importlib
import os
import re
import sys
import traceback

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


def fail(msg: str) -> None:
	print("SMOKE FAIL:", msg, file=sys.stderr)
	sys.exit(1)


def main() -> int:
	from ui5.qtcompat import (
		QApplication, Qt, QDialog, QMessageBox, QMainWindow, qApp,
		QComboBox, QDateTime, QTimer, QListWidget, QListWidgetItem,
		QDropEvent, QMimeData, QPointF, QFileDialog,
	)
	if not hasattr(QDialog, "exec_"):
		fail("QDialog.exec_ missing from compat layer")

	for name in ("AlignCenter", "WaitCursor", "ItemIsEnabled", "Horizontal"):
		if not hasattr(Qt, name):
			fail(f"Qt.{name} missing from compat layer")
	if not hasattr(QDialog, "Accepted"):
		fail("QDialog.Accepted missing")
	if not hasattr(QMessageBox, "Yes"):
		fail("QMessageBox.Yes missing")

	app = QApplication(["hplip-qt6-smoketest"])
	if QApplication.instance() is None:
		fail("QApplication.instance() is None")
	# qApp proxy
	qApp.processEvents()

	# Generated forms (pure Qt)
	from ui5.aboutdialog_base import Ui_AboutDlg_base
	w = QDialog()
	Ui_AboutDlg_base().setupUi(w)

	from ui5.devmgr5_base import Ui_MainWindow
	mw = QMainWindow()
	devmgr_ui = Ui_MainWindow()
	devmgr_ui.setupUi(mw)

	from ui5.setupdialog_base import Ui_Dialog as SetupUi
	w2 = QDialog()
	SetupUi().setupUi(w2)

	# Qt 6 dropped QComboBox.activated(QString) etc. The compat layer must
	# restore signal[str] or hp-toolbox dies in DevMgr5.initUI().
	got = []

	def _record(value):
		got.append(value)

	cb = QComboBox()
	cb.addItems(["alpha", "beta"])
	try:
		cb.activated[str].connect(_record)
		cb.currentIndexChanged[str].connect(_record)
		cb.highlighted[str].connect(_record)
		cb.activated[int].connect(lambda i: got.append(("int", i)))
	except KeyError:
		traceback.print_exc()
		fail("QComboBox signal[str] overload missing (Qt6 combo API)")
	cb.setCurrentIndex(1)
	cb.activated[str].emit("beta")
	if "beta" not in got:
		fail("activated[str] did not deliver the item text")
	print("QComboBox signal[str] overloads OK")

	dt = QDateTime()
	try:
		dt.setTime_t(0)
	except Exception:
		traceback.print_exc()
		fail("QDateTime.setTime_t missing or not callable")
	print("QDateTime.setTime_t OK")

	# exec_ must work on a QDialog *subclass*. Assigning the SIP exec
	# method onto the class looks fine until NoDevicesDialog.exec_().
	class _CompatDialog(QDialog):
		pass

	dlg = _CompatDialog()
	QTimer.singleShot(0, dlg.reject)
	try:
		dlg.exec_()
	except TypeError:
		traceback.print_exc()
		fail("QDialog subclass exec_ is not callable")
	print("QDialog subclass exec_ OK")

	lw = QListWidget()
	item = QListWidgetItem("dev", lw)
	try:
		lw.setSelected(item, True)
	except Exception:
		traceback.print_exc()
		fail("QListWidget.setSelected missing (DevMgr5.activateDevice)")
	if not item.isSelected():
		fail("QListWidget.setSelected did not select the item")
	print("QListWidget.setSelected OK")

	drop = QDropEvent(
		QPointF(4, 5),
		Qt.CopyAction,
		QMimeData(),
		Qt.LeftButton,
		Qt.NoModifier,
	)
	try:
		p = drop.pos()
	except Exception:
		traceback.print_exc()
		fail("QDropEvent.pos missing (fabgrouptable dragMoveEvent)")
	if p.x() != 4 or p.y() != 5:
		fail(f"QDropEvent.pos returned {p}")
	print("QDropEvent.pos OK")

	from ui5.qtcompat import _PathResult
	fd = _PathResult("/tmp/foo.ppd", "PPD (*.ppd)")
	if fd[0] != "/tmp/foo.ppd" or str(fd) != "/tmp/foo.ppd" or not fd:
		fail("QFileDialog path result is not both indexable and a string")
	print("QFileDialog.getOpenFileName compat OK")

	# Logic modules that exercise signals, qApp.translate, exec_ aliases
	mods = [
		"ui5.ui_utils",
		"ui5.aboutdialog",
		"ui5.settingsdialog",
		"ui5.printsettingstoolbox",
		"ui5.systrayframe",
		"ui5.filetable",
		"ui5.queuesconf",
		"ui5.setupdialog",
		"ui5.systemtray",
		"ui5.devmgr5",
		"ui5.wifisetupdialog",
		"ui5.plugindialog",
		"ui5.printdialog",
		"ui5.sendfaxdialog",
		"ui5.printernamecombobox",
		"ui5.deviceuricombobox",
	]
	for name in mods:
		try:
			importlib.import_module(name)
		except Exception:
			traceback.print_exc()
			fail(f"import {name}")
		print("imported", name)

	# The exact connections hp-toolbox makes during DevMgr5.initUI()
	devmgr_ui.PrintControlPrinterNameCombo.activated[str].connect(lambda s: None)
	devmgr_ui.PrintSettingsPrinterNameCombo.activated[str].connect(lambda s: None)
	devmgr_ui.Tabs.currentChanged[int].connect(lambda i: None)
	devmgr_ui.DeviceList.customContextMenuRequested["const QPoint &"].connect(lambda p: None)
	devmgr_ui.DeviceList.currentItemChanged["QListWidgetItem *", "QListWidgetItem *"].connect(
		lambda a, b: None
	)
	print("DevMgr5.initUI signal connections OK")

	from ui5.printernamecombobox import PrinterNameComboBox
	pnc = PrinterNameComboBox(None)
	pnc.close()
	print("constructed PrinterNameComboBox")

	from ui5.deviceuricombobox import DeviceUriComboBox
	duc = DeviceUriComboBox(None)
	duc.close()
	print("constructed DeviceUriComboBox")

	# Construct a couple of real dialogs (pixmap paths may be incomplete
	# in the buildroot; setupUi success is still a hard failure above).
	try:
		from ui5.aboutdialog import AboutDialog
		dlg = AboutDialog(None, "3.26.4", "3.26.4")
		dlg.close()
		print("constructed AboutDialog")
	except Exception:
		traceback.print_exc()
		print("AboutDialog construct skipped", file=sys.stderr)

	try:
		from ui5.settingsdialog import SettingsDialog
		sd = SettingsDialog(None)
		sd.close()
		print("constructed SettingsDialog")
	except Exception:
		traceback.print_exc()
		print("SettingsDialog construct skipped", file=sys.stderr)

	# This is what `hp-toolbox` does. Import-only testing missed the crash.
	try:
		from ui5.devmgr5 import DevMgr5
		from ui5.nodevicesdialog import NoDevicesDialog
		toolbox = DevMgr5("15.0", None, None)
		# initalUpdate() is queued on a timer; with no printers it opens
		# NoDevicesDialog.exec_(), which is what the event loop hits.
		_orig_exec = NoDevicesDialog.exec_

		def _auto_close(self, *args, **kwargs):
			QTimer.singleShot(0, self.reject)
			return _orig_exec(self, *args, **kwargs)

		NoDevicesDialog.exec_ = _auto_close
		toolbox.initalUpdate()
		app.processEvents()
		toolbox.close()
		print("constructed DevMgr5")
	except Exception:
		traceback.print_exc()
		fail("DevMgr5 construct (hp-toolbox startup)")

	from ui5.fabgrouptable import FABGroupTable
	if tuple(FABGroupTable.namesAddedToGroup.signatures) == ("",):
		fail("namesAddedToGroup is still a no-arg signal (FAB drop emits row, items)")
	print("FABGroupTable.namesAddedToGroup signature OK")

	# GUI tools that still imported PyQt4/ui4 after the first Qt6 pass.
	leftover = []
	for rel in (
		"colorcal.py",
		"linefeedcal.py",
		"pqdiag.py",
		"makecopies.py",
		"check-plugin.py",
		"prnt/cups.py",
	):
		for base in sys.path:
			p = os.path.join(base, rel)
			if os.path.isfile(p):
				src = open(p, encoding="utf-8", errors="replace").read()
				if re.search(r"^[^#\n]*from PyQt4", src, re.M):
					leftover.append(rel)
				if "from ui4 import ui_utils" in src:
					leftover.append(rel)
				break
	if leftover:
		fail("still importing PyQt4: " + ", ".join(leftover))
	print("leftover PyQt4 GUI entry points rewritten")

	print("HPLIP PyQt6 smoke test passed")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
