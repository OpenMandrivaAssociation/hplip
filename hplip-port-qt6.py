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
