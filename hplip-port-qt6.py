#!/usr/bin/python
# Rewrite HPLIP's PyQt5 UI onto the PyQt6 compatibility layer.
# Run from the unpacked source tree after patches have been applied.

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")

SKIP_DIRS = {"ui", "ui4", ".git"}

# Multi-line emit(SIGNAL(...), arg) -> obj.signal.emit(arg)
EMIT_SIGNAL_RE = re.compile(
	r"""(?P<obj>\w+(?:\.\w+)*)\.emit\(\s*SIGNAL\(\s*["'](?P<sig>[^"']+)["']\s*\)\s*,\s*""",
	re.M,
)

CONNECT_LASTWINDOW_RE = re.compile(
	r"""QObject\.connect\(\s*(?P<app>\w+)\s*,\s*SIGNAL\(\s*["']lastWindowClosed\(\)["']\s*\)\s*,\s*(?P=app)\s*,\s*SLOT\(\s*["']quit\(\)["']\s*\)\s*\)""",
)

QSTRING_SIG_RE = re.compile(
	r"""\[(?:["']const QString\s*&["']|["']const QString &["'])\]"""
)


def rewrite_imports(text: str, in_ui5: bool) -> str:
	compat = ".qtcompat" if in_ui5 else "ui5.qtcompat"

	text = text.replace(
		"from PyQt5.QtCore import *\nfrom PyQt5.QtGui import *\nfrom PyQt5.QtWidgets import *",
		f"from {compat} import *",
	)
	text = text.replace(
		"from PyQt5.QtCore import *\nfrom PyQt5.QtGui import *",
		f"from {compat} import *",
	)
	text = text.replace(
		"from PyQt5 import QtCore, QtGui, QtWidgets",
		f"from {compat} import QtCore, QtGui, QtWidgets",
	)
	text = re.sub(
		r"from PyQt5\.QtWidgets import ([^\n]+)",
		rf"from {compat} import \1",
		text,
	)
	text = re.sub(
		r"from PyQt5\.QtGui import ([^\n]+)",
		rf"from {compat} import \1",
		text,
	)
	text = re.sub(
		r"from PyQt5\.QtCore import ([^\n]+)",
		rf"from {compat} import \1",
		text,
	)
	text = re.sub(
		r"from PyQt5 import ([^\n]+)",
		rf"from {compat} import \1",
		text,
	)
	text = re.sub(
		r"^(\s*)import PyQt5\s*$",
		rf"\1import PyQt6 as PyQt5",
		text,
		flags=re.M,
	)
	# Collapse accidental duplicate star-imports from overlapping replacements
	text = re.sub(
		rf"(from {re.escape(compat)} import \*\n){{2,}}",
		f"from {compat} import *\n",
		text,
	)
	# setupdialog.py has a try/except that imported Core/Gui then Core/Gui/Widgets
	text = re.sub(
		rf"try:\n    from {re.escape(compat)} import \*\nexcept ImportError:\n    from {re.escape(compat)} import \*\n",
		f"from {compat} import *\n",
		text,
	)
	text = text.replace(
		"from dbus.mainloop.pyqt5 import",
		"from dbus.mainloop.pyqt6 import",
	)
	return text


def rewrite_apis(text: str) -> str:
	text = EMIT_SIGNAL_RE.sub(
		lambda m: f"{m.group('obj')}.{SIGNAL_name(m.group('sig'))}.emit(",
		text,
	)
	text = CONNECT_LASTWINDOW_RE.sub(
		r"\g<app>.lastWindowClosed.connect(\g<app>.quit)",
		text,
	)
	text = QSTRING_SIG_RE.sub("[str]", text)
	text = text.replace(".clicked['bool']", ".clicked[bool]")
	text = text.replace("QTextCodec.locale()", "QLocale.system().name()")
	# If QTextCodec import vanished, QLocale comes from qtcompat star-import
	return text


def SIGNAL_name(sig: str) -> str:
	return sig.split("(", 1)[0].strip()


# Live PyQt4/ui4 imports that the PyQt5 rewrite never touched.
PYQT4_UI4_BLOCK_RE = re.compile(
	r"""(?P<indent>[ \t]*)try:\n"""
	r"""(?P=indent)    from PyQt4\.QtGui import QApplication(?P<extra>, QMessageBox)?\n"""
	r"""(?P=indent)    from ui4\.(?P<mod>\w+) import (?P<cls>\w+)\n"""
	r"""(?:(?P=indent)    from installer import core_install\n)?"""
	r"""(?P=indent)except ImportError:\n"""
	r"""(?P=indent)    log\.error\("[^"]*"\)\n"""
	r"""(?P=indent)    sys\.exit\(1\)\n""",
)


def _ensure_import_module(text: str) -> str:
	if re.search(
		r"from importlib import import_module|dyn_import_mod as import_module",
		text,
	):
		return text
	needle = "from base.g import *\n"
	if needle in text:
		return text.replace(
			needle,
			needle
			+ "try:\n"
			+ "    from importlib import import_module\n"
			+ "except ImportError:\n"
			+ "    from base.utils import dyn_import_mod as import_module\n",
			1,
		)
	return text


def rewrite_qt4_entry(text: str) -> str:
	"""Point leftover hp-* GUI tools at ui5 via import_dialog()."""

	def repl(m: re.Match) -> str:
		indent = m.group("indent")
		mod = m.group("mod")
		cls = m.group("cls")
		extra = m.group("extra") or ""
		block = (
			f"{indent}QApplication, ui_package = utils.import_dialog(ui_toolkit)\n"
			f"{indent}ui = import_module(ui_package + \".{mod}\")\n"
		)
		if extra:
			block += f"{indent}from ui5.qtcompat import QMessageBox\n"
		# Keep the dialog construction working after the import rewrite.
		nonlocal_text_fix.append((rf"\b{cls}\(", f"ui.{cls}("))
		return block

	nonlocal_text_fix: list[tuple[str, str]] = []
	text = PYQT4_UI4_BLOCK_RE.sub(repl, text)
	for pat, repl_s in nonlocal_text_fix:
		text = re.sub(pat, repl_s, text)
	if "utils.import_dialog(ui_toolkit)" in text:
		text = _ensure_import_module(text)
	# Tools that only advertised Qt4 never selected the configured Qt5 toolkit.
	text = text.replace("(UI_TOOLKIT_QT4,)", "(UI_TOOLKIT_QT4, UI_TOOLKIT_QT5)")
	# cups_operation() treated every non-Qt3 toolkit as Qt4.
	text = text.replace(
		"from ui4 import ui_utils\n                    ui_utils.FailureUI(",
		"from ui5 import ui_utils\n                    ui_utils.FailureUI(",
	)
	return text


def rewrite_signal_defs(text: str) -> str:
	# FAB group table emits (row, items) but the signal was declared with no args.
	text = text.replace(
		"namesAddedToGroup = pyqtSignal()",
		"namesAddedToGroup = pyqtSignal(int, object)",
	)
	return text


def process(path: pathlib.Path) -> bool:
	rel = path.relative_to(ROOT)
	parts = rel.parts
	if parts and parts[0] in SKIP_DIRS:
		return False
	text = path.read_text(encoding="utf-8", errors="replace")
	orig = text
	in_ui5 = len(parts) >= 2 and parts[0] == "ui5"
	if "PyQt5" in text or "pyqt5" in text or "QTextCodec" in text or "SIGNAL(" in text:
		text = rewrite_imports(text, in_ui5)
		text = rewrite_apis(text)
	if "from PyQt4" in text or "from ui4" in text:
		text = rewrite_qt4_entry(text)
	if "utils.import_dialog(ui_toolkit)" in text:
		text = _ensure_import_module(text)
	if "pyqtSignal()" in text:
		text = rewrite_signal_defs(text)
	if text != orig:
		path.write_text(text, encoding="utf-8")
		return True
	return False


def main() -> int:
	changed = 0
	for path in ROOT.rglob("*.py"):
		if process(path):
			print("ported", path.relative_to(ROOT))
			changed += 1
	print(f"{changed} files rewritten")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
