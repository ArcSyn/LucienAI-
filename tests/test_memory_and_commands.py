# tests/test_memory_and_commands.py
import builtins
from io import StringIO
from unittest.mock import patch
import Lucien

def _run_main_once(input_line: str) -> str:
    buf_in = StringIO(input_line + "\nexit\n")
    buf_out = StringIO()
    with patch.object(builtins, "input", lambda _="You >>> ": buf_in.readline().rstrip("\n")), \
         patch("sys.stdout", buf_out):
        Lucien.main()
    return buf_out.getvalue()

def test_command_parsing_unknown():
    out = _run_main_once("xyzcmd")
    # Should fall back to AI chat for unknown commands
    assert len(out) > 0

def test_internet_toggle():
    out_on  = _run_main_once("internet on")
    out_off = _run_main_once("internet off")
    assert "Internet mode ON" in out_on
    assert "Internet mode OFF" in out_off
