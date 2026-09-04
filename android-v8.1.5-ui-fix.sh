#!/usr/bin/env bash
set -euo pipefail
PKG="$GITHUB_WORKSPACE/android-v8/app/src/main/java/io/github/hantae_ho/twa"
python3 - <<'PY'
from pathlib import Path
import os
p=Path(os.environ['GITHUB_WORKSPACE'])/'android-v8/app/src/main/java/io/github/hantae_ho/twa/NotificationSettingsActivity.java'
s=p.read_text(encoding='utf-8')
old='''        importFromIntent(i);\n        refresh();'''
new='''        importFromIntent(i);\n        applyVisitControls();\n        refresh();'''
if s.count(old)!=1: raise SystemExit('onNewIntent anchor')
s=s.replace(old,new,1)
old='''        if (summary != null) summary.setText(summaryText());\n        applyVisitControls();\n        refreshStatus();'''
new='''        if (summary != null) summary.setText(summaryText());\n        refreshStatus();'''
if s.count(old)!=1: raise SystemExit('refresh anchor')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
PY
grep -q 'importFromIntent(i);' "$PKG/NotificationSettingsActivity.java"
echo 'V8.1.5 native UI state fix PASS'
