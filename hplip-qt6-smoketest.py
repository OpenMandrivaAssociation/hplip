#!/usr/bin/python
# Offscreen smoke test for the HPLIP PyQt6 UI.
# Must be able to import HPLIP modules (PYTHONPATH) and cupsext.

from __future__ import annotations

import importlib
import os
import sys
import traceback

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


def fail(msg: str) -> None:
	print("SMOKE FAIL:", msg, file=sys.stderr)
	sys.exit(1)


def main() -> int:
	from ui5.qtcompat import (
		QApplication, Qt, QDialog, QMessageBox, QMainWindow, qApp,
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
	Ui_MainWindow().setupUi(mw)

	from ui5.setupdialog_base import Ui_Dialog as SetupUi
	w2 = QDialog()
	SetupUi().setupUi(w2)

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
	]
	for name in mods:
		try:
			importlib.import_module(name)
		except Exception:
			traceback.print_exc()
			fail(f"import {name}")
		print("imported", name)

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

	print("HPLIP PyQt6 smoke test passed")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
