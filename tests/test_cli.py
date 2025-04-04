import sys
from cli import main as parse_cli_args

def test_cli_args(monkeypatch):
    test_args = ["program_name", "--num_send", "123", "--num_receive", "456", "--text", "Test message"]
    monkeypatch.setattr(sys, "argv", test_args)
    args = parse_cli_args()
    assert args.num_send == "123"
    assert args.num_receive == "456"
    assert args.text == "Test message"
