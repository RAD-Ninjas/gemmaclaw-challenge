#!/bin/bash
# GemmaClaw Challenge — Verify Setup
# Checks that all components are installed and working

echo "============================================"
echo "  GemmaClaw Setup Verification"
echo "============================================"
echo ""

PASS=0
FAIL=0

check() {
    if eval "$2" &>/dev/null; then
        echo "  ✅ $1"
        PASS=$((PASS + 1))
    else
        echo "  ❌ $1"
        FAIL=$((FAIL + 1))
    fi
}

echo "Checking components..."
echo ""

check "Ollama installed" "command -v ollama"
check "Ollama running" "curl -sf http://localhost:11434/api/tags"
check "Gemma 4 E2B pulled" "ollama list | grep -q gemma4"
check "Node.js 22+" "node --version | grep -qE 'v2[2-9]|v[3-9][0-9]'"
check "OpenClaw installed" "command -v openclaw"
check "OpenClaw config exists" "test -f ~/.openclaw/openclaw.json"

echo ""
echo "--------------------------------------------"
echo "  Results: $PASS passed, $FAIL failed"
echo "--------------------------------------------"

if [ "$FAIL" -eq 0 ]; then
    echo ""
    echo "  Everything looks good! 🎉"
    echo "  Run: openclaw --model ollama/gemma4:e2b"
else
    echo ""
    echo "  Some checks failed. See TROUBLESHOOTING.md"
fi

echo ""
echo "System info:"
echo "  OS:   $(uname -s) $(uname -r)"
echo "  Arch: $(uname -m)"
if [ -f /proc/meminfo ]; then
    echo "  RAM:  $(free -h | awk '/^Mem:/{print $2}')"
fi
echo ""
