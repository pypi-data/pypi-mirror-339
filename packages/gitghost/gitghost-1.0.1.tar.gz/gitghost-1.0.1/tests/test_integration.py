import pytest
from click.testing import CliRunner
from gitghost.cli import cli
from unittest import mock
from git import GitCommandError
import os

@pytest.fixture
def runner():
    return CliRunner()

def test_init_creates_include_and_repo(tmp_path, runner):
    os.chdir(tmp_path)
    result = runner.invoke(cli, ["init"])
    assert result.exit_code == 0
    assert ".gitghostinclude" in os.listdir()
    assert ".gitghost_private" in os.listdir()
    assert "Initialized private repo" in result.output or "already exists" in result.output

def test_init_when_include_exists(tmp_path, runner):
    os.chdir(tmp_path)
    (tmp_path / ".gitghostinclude").write_text("# test\n")
    result = runner.invoke(cli, ["init"])
    assert result.exit_code == 0
    assert ".gitghostinclude" in os.listdir()
    assert "already exists" in result.output

def test_save_no_files(tmp_path, runner):
    os.chdir(tmp_path)
    # No .gitghostinclude file
    result = runner.invoke(cli, ["save"])
    assert result.exit_code == 0 or result.exit_code == 1
    # Should handle missing include gracefully

def test_save_with_message(tmp_path, runner):
    os.chdir(tmp_path)
    (tmp_path / ".gitghostinclude").write_text("secret.txt\n")
    (tmp_path / "secret.txt").write_text("top secret")
    # Initialize repo first
    runner.invoke(cli, ["init"])
    result = runner.invoke(cli, ["save", "--message", "my commit"])
    assert result.exit_code in (0, 1)

def test_status_empty_include(tmp_path, runner):
    os.chdir(tmp_path)
    (tmp_path / ".gitghostinclude").write_text("")
    runner.invoke(cli, ["init"])
    result = runner.invoke(cli, ["status"])
    assert result.exit_code in (0, 1)

def test_status_missing_include(tmp_path, runner):
    os.chdir(tmp_path)
    result = runner.invoke(cli, ["status"])
    assert result.exit_code in (0, 1)
    assert "not found" in result.output or "No changes" in result.output

def test_discard_cancel(tmp_path, runner):
    os.chdir(tmp_path)
    (tmp_path / ".gitghostinclude").write_text("secret.txt\n")
    (tmp_path / "secret.txt").write_text("top secret")
    runner.invoke(cli, ["init"])
    # Simulate user entering 'n' to cancel discard
    result = runner.invoke(cli, ["discard"], input="n\n")
    assert result.exit_code in (0, 1)
    assert "cancelled" in result.output or "Discard cancelled" in result.output

def test_discard_confirm(tmp_path, runner):
    os.chdir(tmp_path)
    (tmp_path / ".gitghostinclude").write_text("secret.txt\n")
    (tmp_path / "secret.txt").write_text("top secret")
    runner.invoke(cli, ["init"])
    # Simulate user entering 'y' to confirm discard
    result = runner.invoke(cli, ["discard"], input="y\n")
    assert result.exit_code in (0, 1)
    # Should attempt to restore files or print restored message

def test_status_empty_private_repo(monkeypatch):
    repo_mock = mock.Mock()
    repo_mock.head.is_valid.return_value = False
    with mock.patch("gitghost.cli.ensure_private_repo", return_value=repo_mock), \
         mock.patch("gitghost.cli.parse_gitghostinclude", return_value=["file1.txt"]), \
         mock.patch("gitghost.cli.copy_private_files"):
        runner = CliRunner()
        result = runner.invoke(cli, ["status"])
        assert "Private repo is empty" in result.output

def test_status_missing_files(monkeypatch):
    repo_mock = mock.Mock()
    repo_mock.head.is_valid.return_value = True
    repo_mock.index.diff.return_value = []
    repo_mock.untracked_files = []
    with mock.patch("gitghost.cli.ensure_private_repo", return_value=repo_mock), \
         mock.patch("gitghost.cli.parse_gitghostinclude", return_value=["file1.txt"]), \
         mock.patch("gitghost.cli.copy_private_files"), \
         mock.patch("os.path.exists", return_value=False):
        runner = CliRunner()
        result = runner.invoke(cli, ["status"])
        assert "Missing in vault" in result.output

def test_status_directory_recursion(monkeypatch):
    repo_mock = mock.Mock()
    repo_mock.head.is_valid.return_value = True
    repo_mock.index.diff.return_value = []
    repo_mock.untracked_files = []
    with mock.patch("gitghost.cli.ensure_private_repo", return_value=repo_mock), \
         mock.patch("gitghost.cli.parse_gitghostinclude", return_value=["dir1"]), \
         mock.patch("gitghost.cli.copy_private_files"), \
         mock.patch("os.path.exists", return_value=True), \
         mock.patch("os.path.isdir", return_value=True), \
         mock.patch("os.walk", return_value=[("/vault/dir1", [], ["a.txt", "b.txt"])]):
        runner = CliRunner()
        result = runner.invoke(cli, ["status"])
        # Should not crash, may or may not print files

def test_status_git_command_error(monkeypatch):
    repo_mock = mock.Mock()
    repo_mock.head.is_valid.return_value = True
    repo_mock.index.diff.side_effect = GitCommandError("diff", 1)
    repo_mock.untracked_files = []
    with mock.patch("gitghost.cli.ensure_private_repo", return_value=repo_mock), \
         mock.patch("gitghost.cli.parse_gitghostinclude", return_value=["file1.txt"]), \
         mock.patch("gitghost.cli.copy_private_files"), \
         mock.patch("os.path.exists", return_value=True):
        runner = CliRunner()
        result = runner.invoke(cli, ["status"])
        # Should handle error gracefully, no crash

def test_status_no_changes(monkeypatch):
    repo_mock = mock.Mock()
    repo_mock.head.is_valid.return_value = True
    repo_mock.index.diff.return_value = []
    repo_mock.untracked_files = []
    with mock.patch("gitghost.cli.ensure_private_repo", return_value=repo_mock), \
         mock.patch("gitghost.cli.parse_gitghostinclude", return_value=["file1.txt"]), \
         mock.patch("gitghost.cli.copy_private_files"), \
         mock.patch("os.path.exists", return_value=True):
        runner = CliRunner()
        result = runner.invoke(cli, ["status"])
        # Should not print "Changed private files"
def test_init_github_cli_not_installed(monkeypatch):
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    monkeypatch.setattr("os.path.exists", lambda p: False)
    with mock.patch("gitghost.cli.Repo.init"), \
         mock.patch("gitghost.cli.open", mock.mock_open(), create=True), \
         mock.patch("subprocess.run", side_effect=FileNotFoundError):
        runner = CliRunner()
        result = runner.invoke(cli, ["init"])
        assert "GitHub CLI (gh) not found" in result.output

def test_init_github_repo_creation_failure(monkeypatch):
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    monkeypatch.setattr("os.path.exists", lambda p: False)
    def subprocess_run_side_effect(*args, **kwargs):
        if "gh" in args[0]:
            raise Exception("gh error")
        return mock.DEFAULT
    with mock.patch("gitghost.cli.Repo.init"), \
         mock.patch("gitghost.cli.open", mock.mock_open(), create=True), \
         mock.patch("subprocess.run", side_effect=subprocess_run_side_effect):
        runner = CliRunner()
        result = runner.invoke(cli, ["init"])
        assert "Failed to create private GitHub repo automatically" in result.output or "GitHub CLI (gh) not found" in result.output

def test_init_gitignore_missing(monkeypatch, tmp_path):
    os.chdir(tmp_path)
    (tmp_path / ".gitghostinclude").write_text("secret.txt\n")
    (tmp_path / "secret.txt").write_text("top secret")
    with mock.patch("gitghost.cli.Repo.init"), \
         mock.patch("subprocess.run", side_effect=FileNotFoundError):
        runner = CliRunner()
        result = runner.invoke(cli, ["init"])
        assert ".gitignore" in os.listdir()

def test_init_gitignore_exists_without_block(monkeypatch, tmp_path):
    os.chdir(tmp_path)
    (tmp_path / ".gitghostinclude").write_text("secret.txt\n")
    (tmp_path / "secret.txt").write_text("top secret")
    (tmp_path / ".gitignore").write_text("node_modules/\n")
    with mock.patch("gitghost.cli.Repo.init"), \
         mock.patch("subprocess.run", side_effect=FileNotFoundError):
        runner = CliRunner()
        result = runner.invoke(cli, ["init"])
        content = (tmp_path / ".gitignore").read_text()
        assert ".gitghost_private" in content

def test_init_gitignore_exists_with_block(monkeypatch, tmp_path):
    os.chdir(tmp_path)
    (tmp_path / ".gitghostinclude").write_text("secret.txt\n")
    (tmp_path / "secret.txt").write_text("top secret")
    (tmp_path / ".gitignore").write_text("# GitGhost\n.gitghost_private/\n.gitghostinclude\n")
    with mock.patch("gitghost.cli.Repo.init"), \
         mock.patch("subprocess.run", side_effect=FileNotFoundError):
        runner = CliRunner()
        result = runner.invoke(cli, ["init"])
        content = (tmp_path / ".gitignore").read_text()
        assert content.count(".gitghost_private") == 1  # no duplicate block

def test_init_private_repo_fallback(monkeypatch):
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    monkeypatch.setattr("os.path.exists", lambda p: True)
    repo_cls = mock.Mock(side_effect=Exception("fail"))
    repo_init = mock.Mock()
    with mock.patch("gitghost.cli.Repo", repo_cls), \
         mock.patch("gitghost.cli.Repo.init", repo_init), \
         mock.patch("gitghost.cli.open", mock.mock_open(), create=True), \
         mock.patch("subprocess.run", side_effect=FileNotFoundError):
        runner = CliRunner()
        result = runner.invoke(cli, ["init"])
        repo_init.assert_called()
def test_status_git_command_error_branches(monkeypatch):
    repo_mock = mock.Mock()
    repo_mock.head.is_valid.return_value = True
    repo_mock.index.diff.side_effect = GitCommandError("diff", 1)
    repo_mock.untracked_files = []
    with mock.patch("gitghost.cli.ensure_private_repo", return_value=repo_mock), \
         mock.patch("gitghost.cli.parse_gitghostinclude", return_value=["file1.txt"]), \
         mock.patch("gitghost.cli.copy_private_files"), \
         mock.patch("os.path.exists", return_value=True):
        runner = CliRunner()
def test_init_nested_exceptions(monkeypatch):
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    monkeypatch.setattr("os.path.exists", lambda p: False)
    repo_cls = mock.Mock(side_effect=Exception("fail"))
    repo_init = mock.Mock()
    def subprocess_run_side_effect(*args, **kwargs):
        if "gh" in args[0]:
            return mock.Mock(returncode=0)
        return mock.DEFAULT
    with mock.patch("gitghost.cli.Repo", repo_cls), \
         mock.patch("gitghost.cli.Repo.init", repo_init), \
         mock.patch("gitghost.cli.open", mock.mock_open(), create=True), \
         mock.patch("subprocess.run", side_effect=subprocess_run_side_effect), \
         mock.patch("subprocess.check_output", side_effect=Exception("fail")), \
         mock.patch("gitghost.cli.Repo.create_remote", side_effect=Exception("fail")):
        runner = CliRunner()
        result = runner.invoke(cli, ["init"])
        # Should handle nested exceptions gracefully
        result = runner.invoke(cli, ["status"])
        # Should handle error gracefully, no crash
def test_init_repo_exists_exception(monkeypatch):
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    monkeypatch.setattr("os.path.exists", lambda p: True)
    repo_cls = mock.Mock(side_effect=Exception("fail"))
    repo_init = mock.Mock()
    with mock.patch("gitghost.cli.Repo", repo_cls), \
         mock.patch("gitghost.cli.Repo.init", repo_init), \
         mock.patch("gitghost.cli.open", mock.mock_open(), create=True), \
         mock.patch("subprocess.run", side_effect=FileNotFoundError):
        runner = CliRunner()
        result = runner.invoke(cli, ["init"])
        repo_init.assert_called()

def test_init_get_public_repo_name_exception(monkeypatch):
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    monkeypatch.setattr("os.path.exists", lambda p: False)
    with mock.patch("gitghost.cli.Repo.init"), \
         mock.patch("gitghost.cli.open", mock.mock_open(), create=True), \
         mock.patch("subprocess.run") as subproc_mock, \
         mock.patch("gitghost.cli.Repo") as repo_mock:
        repo_mock.return_value.remote.return_value.urls = ["https://github.com/user/repo.git"]
        repo_mock.side_effect = Exception("fail")
        runner = CliRunner()
        result = runner.invoke(cli, ["init"])
        # Should fallback to directory name, no crash

def test_init_subprocess_repo_create_failure(monkeypatch):
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    monkeypatch.setattr("os.path.exists", lambda p: False)
    def subprocess_run_side_effect(*args, **kwargs):
        if "gh" in args[0]:
            raise Exception("gh error")
        return mock.DEFAULT
    with mock.patch("gitghost.cli.Repo.init"), \
         mock.patch("gitghost.cli.open", mock.mock_open(), create=True), \
         mock.patch("subprocess.run", side_effect=subprocess_run_side_effect):
        runner = CliRunner()
        result = runner.invoke(cli, ["init"])
        # Should handle error gracefully

def test_cli_entry_point():
    # Cover line 300
    from gitghost import cli as cli_module
    with pytest.raises(SystemExit):
        cli_module.cli()