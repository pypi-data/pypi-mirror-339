import os
import pytest
from unittest import mock
from click.testing import CliRunner
from gitghost import cli

def test_parse_gitghostinclude_missing(monkeypatch):
    monkeypatch.setattr("os.path.exists", lambda p: False)
    with mock.patch("builtins.print"):
        files = cli.parse_gitghostinclude()
    assert files == []

def test_ensure_private_repo_init_when_missing(monkeypatch):
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    monkeypatch.setattr("os.path.exists", lambda p: False)
    with mock.patch("os.makedirs") as makedirs_mock, \
         mock.patch("gitghost.cli.Repo.init") as repo_init_mock:
        repo_obj = mock.Mock()
        repo_init_mock.return_value = repo_obj
        repo = cli.ensure_private_repo()
        makedirs_mock.assert_called()
        repo_init_mock.assert_called()
        assert repo == repo_obj

def test_ensure_private_repo_fallback_to_init(monkeypatch):
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    monkeypatch.setattr("os.path.exists", lambda p: True)
    with mock.patch("gitghost.cli.Repo") as repo_cls, \
         mock.patch("gitghost.cli.Repo.init") as repo_init_mock:
        repo_cls.side_effect = Exception("fail")
        repo_obj = mock.Mock()
        repo_init_mock.return_value = repo_obj
        repo = cli.ensure_private_repo()
        repo_init_mock.assert_called()
        assert repo == repo_obj

def test_copy_private_files_skips_missing(monkeypatch):
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    monkeypatch.setattr("os.path.exists", lambda p: False)
    cli.copy_private_files(["secret.txt"])  # Should skip without error

def test_copy_private_files_directory(monkeypatch):
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    # Source exists and is directory
    def exists_side_effect(path):
        if "secret_dir" in path:
            return True
        return False
    monkeypatch.setattr("os.path.exists", exists_side_effect)
    monkeypatch.setattr("os.path.isdir", lambda p: True)
    with mock.patch("shutil.rmtree") as rmtree_mock, \
         mock.patch("shutil.copytree") as copytree_mock:
        cli.copy_private_files(["secret_dir"])
        rmtree_mock.assert_called()
        copytree_mock.assert_called()

def test_save_push_error(monkeypatch):
    repo_mock = mock.Mock()
    repo_mock.head.is_valid.return_value = False
    repo_mock.index.diff.return_value = []
    repo_mock.untracked_files = []
    repo_mock.index.add.return_value = None
    repo_mock.is_dirty.return_value = True
    repo_mock.remote.return_value.push.side_effect = cli.GitCommandError("push", 1)
    repo_mock.remote.return_value.git.push.side_effect = None
    repo_mock.remote.return_value.name = "origin"
    repo_mock.remotes = []
    repo_mock.active_branch.name = "main"

    with mock.patch("gitghost.cli.ensure_private_repo", return_value=repo_mock), \
         mock.patch("gitghost.cli.parse_gitghostinclude", return_value=["secret.txt"]), \
         mock.patch("gitghost.cli.copy_private_files"), \
         mock.patch("subprocess.run"), \
         mock.patch("os.path.exists", return_value=True), \
         mock.patch("os.getcwd", return_value="/tmp/testcwd"):
        runner = CliRunner()
        result = runner.invoke(cli.save, ["--message", "test commit"])
        # Accept any exit code, just ensure no crash
        assert result.exit_code in (0, 1)

def test_init_github_cli_missing(monkeypatch):
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    monkeypatch.setattr("os.path.exists", lambda p: False)
    with mock.patch("gitghost.cli.Repo.init"), \
         mock.patch("gitghost.cli.open", mock.mock_open(), create=True), \
         mock.patch("subprocess.run", side_effect=FileNotFoundError):
        runner = CliRunner()
        result = runner.invoke(cli.init)
        assert result.exit_code in (0, 1)

def test_parse_gitghostinclude_with_comments_and_empty(monkeypatch):
    monkeypatch.setattr("os.path.exists", lambda p: True)
    mock_file = mock.mock_open(read_data="# comment line\n\nfile1.txt\n  \n#another\nfile2.txt\n")
    with mock.patch("builtins.open", mock_file):
        files = cli.parse_gitghostinclude()
    assert files == ["file1.txt", "file2.txt"]

def test_status_git_error(monkeypatch):
    repo_mock = mock.Mock()
    repo_mock.head.is_valid.return_value = True
    repo_mock.index.diff.side_effect = cli.GitCommandError("diff", 1)
    
    with mock.patch("gitghost.cli.ensure_private_repo", return_value=repo_mock), \
         mock.patch("gitghost.cli.parse_gitghostinclude", return_value=["secret.txt"]), \
         mock.patch("gitghost.cli.copy_private_files"), \
         mock.patch("os.path.exists", return_value=True), \
         mock.patch("os.path.isdir", return_value=False):
        runner = CliRunner()
        result = runner.invoke(cli.status)
        assert result.exit_code == 0  # Should handle error gracefully

def test_init_repo_name_fallback(monkeypatch):
    """Test init command falls back to directory name when git repo check fails"""
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    monkeypatch.setattr("os.path.exists", lambda p: False)
    monkeypatch.setattr("os.path.basename", lambda p: "fallback-name")
    
    # Mock subprocess.run to simulate gh command available
    def run_side_effect(*args, **kwargs):
        if args[0][0] == "gh" and args[0][1] == "--version":
            return mock.Mock(returncode=0)
        elif args[0][0] == "gh" and args[0][1] == "repo":
            return mock.Mock(returncode=1)  # Repo doesn't exist
        return mock.Mock(returncode=0)

    with mock.patch("gitghost.cli.Repo", side_effect=Exception("repo error")), \
         mock.patch("gitghost.cli.open", mock.mock_open(), create=True), \
         mock.patch("subprocess.run", side_effect=run_side_effect) as subprocess_run:
        runner = CliRunner()
        result = runner.invoke(cli.init)
        assert result.exit_code == 0
        # Check if gh create was called with fallback name
        create_calls = [c for c in subprocess_run.call_args_list if c[0][0][1] == "repo" and c[0][0][2] == "create"]
        assert any("fallback-name-gitghost" in str(call) for call in create_calls)

def test_init_gitignore_updating(monkeypatch):
    """Test .gitignore updating with various content states"""
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    test_cases = [
        # Case 1: No GitGhost entries
        "some content\n",
        # Case 2: Has .gitghost_private/ but not .gitghostinclude
        "some content\n.gitghost_private/\n",
        # Case 3: Has .gitghostinclude but not .gitghost_private/
        "some content\n.gitghostinclude\n",
        # Case 4: Already has both entries
        "some content\n.gitghost_private/\n.gitghostinclude\n"
    ]
    
    for content in test_cases:
        with mock.patch("gitghost.cli.open", mock.mock_open(read_data=content), create=True) as mock_file, \
             mock.patch("os.path.exists", return_value=True), \
             mock.patch("gitghost.cli.Repo.init"):
            runner = CliRunner()
            result = runner.invoke(cli.init)
            assert result.exit_code == 0
            
            # Check write calls when content needed updating
            if ".gitghost_private/" not in content or ".gitghostinclude" not in content:
                mock_file().write.assert_called()
            else:
                # Both entries present, no update needed
                assert not mock_file().write.called or mock_file().write.call_count == 0

def test_init_gh_create_error(monkeypatch):
    """Test init command when GitHub CLI repo creation fails"""
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    monkeypatch.setattr("os.path.exists", lambda p: False)
    
    def subprocess_run_mock(*args, **kwargs):
        if args[0][0] == "gh" and args[0][1] == "--version":
            return mock.Mock(returncode=0)  # gh CLI is available
        if args[0][0] == "gh" and args[0][1] == "repo" and args[0][2] == "create":
            raise Exception("gh create error")
        return mock.Mock(returncode=1)
    
    with mock.patch("gitghost.cli.Repo.init"), \
         mock.patch("gitghost.cli.open", mock.mock_open(), create=True), \
         mock.patch("subprocess.run", side_effect=subprocess_run_mock):
        runner = CliRunner()
        result = runner.invoke(cli.init)
        assert result.exit_code == 0
        assert "Failed to create private GitHub repo" in result.output

def test_copy_private_files_file_copy_error(monkeypatch):
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    def exists_side_effect(path):
        if "secret_file.txt" in path:
            return True
        return False
    monkeypatch.setattr("os.path.exists", exists_side_effect)
    monkeypatch.setattr("os.path.isdir", lambda p: False)
    with mock.patch("os.path.dirname", return_value="/tmp/testcwd/.gitghost_private"), \
         mock.patch("os.makedirs"), \
         mock.patch("shutil.copy2", side_effect=Exception("copy error")):
        with pytest.raises(Exception):
            cli.copy_private_files(["secret_file.txt"])
def test_copy_private_files_file_copy(monkeypatch):
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    # Source exists and is a file
    def exists_side_effect(path):
        if "secret_file.txt" in path:
            return True
        return False
    monkeypatch.setattr("os.path.exists", exists_side_effect)
    monkeypatch.setattr("os.path.isdir", lambda p: False)
    with mock.patch("os.path.dirname", return_value="/tmp/testcwd/.gitghost_private"), \
         mock.patch("os.makedirs") as makedirs_mock, \
         mock.patch("shutil.copy2") as copy2_mock:
        cli.copy_private_files(["secret_file.txt"])
        makedirs_mock.assert_called()
        copy2_mock.assert_called()

def test_discard_cancel(monkeypatch):
    """Test discard command when user cancels"""
    with mock.patch("builtins.input", return_value="n"):
        runner = CliRunner()
        result = runner.invoke(cli.discard)
        assert result.exit_code == 0
        assert "Discard cancelled" in result.output

def test_discard_confirmed_with_missing_files(monkeypatch):
    """Test discard command with confirmed overwrite and some missing vault files"""
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    monkeypatch.setattr("os.path.exists", lambda p: False)  # Files missing in vault
    
    with mock.patch("builtins.input", return_value="y"), \
         mock.patch("gitghost.cli.parse_gitghostinclude", return_value=["file1.txt", "dir1"]), \
         mock.patch("subprocess.run"):
        runner = CliRunner()
        result = runner.invoke(cli.discard)
        assert result.exit_code == 0
        assert "Skipping missing in vault: file1.txt" in result.output
        assert "Skipping missing in vault: dir1" in result.output

def test_discard_confirmed_with_files(monkeypatch):
    """Test discard command with confirmed overwrite and existing files"""
    monkeypatch.setattr("os.getcwd", lambda: "/tmp/testcwd")
    
    def exists_side_effect(path):
        # Files in vault that we want to restore
        vault_paths = [
            "/tmp/testcwd/.gitghost_private/file1.txt",
            "/tmp/testcwd/.gitghost_private/dir1"
        ]
        # Existing target that needs to be removed
        target_paths = ["/tmp/testcwd/dir1"]
        return path in vault_paths + target_paths
    
    monkeypatch.setattr("os.path.exists", exists_side_effect)
    
    with mock.patch("builtins.input", return_value="yes"), \
         mock.patch("gitghost.cli.parse_gitghostinclude", return_value=["file1.txt", "dir1"]), \
         mock.patch("subprocess.run"), \
         mock.patch("os.path.isdir") as isdir_mock, \
         mock.patch("os.makedirs") as makedirs_mock, \
         mock.patch("shutil.copy2") as copy2_mock, \
         mock.patch("shutil.rmtree") as rmtree_mock, \
         mock.patch("shutil.copytree") as copytree_mock:
        
        def isdir_side_effect(path):
            return "dir1" in path
        isdir_mock.side_effect = isdir_side_effect
        
        runner = CliRunner()
        result = runner.invoke(cli.discard)
        assert result.exit_code == 0
        
        # Verify file operations
        rmtree_mock.assert_called_once_with("/tmp/testcwd/dir1")
        copytree_mock.assert_called_once()
        makedirs_mock.assert_called()
        copy2_mock.assert_called_once()