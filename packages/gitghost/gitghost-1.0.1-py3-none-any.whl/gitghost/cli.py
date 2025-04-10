import os
import shutil
import datetime
import click
from git import Repo, GitCommandError

GITVAULT_INCLUDE = ".gitghostinclude"
PRIVATE_REPO_DIR = ".gitghost_private"

def parse_gitghostinclude():
    """Parse .gitghostinclude and return list of file paths."""
    if not os.path.exists(GITVAULT_INCLUDE):
        click.echo(f"Error: {GITVAULT_INCLUDE} not found.")
        return []
    with open(GITVAULT_INCLUDE, "r") as f:
        lines = f.readlines()
    files = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        files.append(line)
    return files

def ensure_private_repo():
    """Ensure the private repo exists and return Repo object."""
    private_repo_path = os.path.join(os.getcwd(), PRIVATE_REPO_DIR)
    if not os.path.exists(private_repo_path):
        os.makedirs(private_repo_path, exist_ok=True)
        repo = Repo.init(private_repo_path)
    else:
        try:
            repo = Repo(private_repo_path)
        except Exception:
            repo = Repo.init(private_repo_path)
    return repo

def copy_private_files(files):
    """Copy private files into .gitghost_private/ preserving paths."""
    for file_path in files:
        src = os.path.join(os.getcwd(), file_path)
        if not os.path.exists(src):
            continue
        dest = os.path.join(os.getcwd(), PRIVATE_REPO_DIR, file_path)
        if os.path.isdir(src):
            # Copy directory recursively
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
        else:
            dest_dir = os.path.dirname(dest)
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copy2(src, dest)

@click.group()
def cli():
    """GitGhost CLI - manage private files securely."""
    pass

@cli.command()
def status():
    """Show status of private files."""
    files = parse_gitghostinclude()
    if not files:
        return

    # Copy private files into private repo dir
    copy_private_files(files)

    # Open or init private repo
    repo = ensure_private_repo()
    
    # If private repo has no commits, instruct user to run save
    if not repo.head.is_valid():
        click.echo("Private repo is empty. The following files/folders will be added on first save:")
        for f in files:
            click.echo(f"  {f}")
        click.echo("Run 'gitghost save' to create the initial commit of your private files.")
        return
    
    changed_files = []
    import os as _os
    
    for file_path in files:
        vault_path = os.path.join(os.getcwd(), PRIVATE_REPO_DIR, file_path)
        if not os.path.exists(vault_path):
            click.echo(f"Missing in vault: {file_path}")
            continue
    
        paths_to_check = []
        if os.path.isdir(vault_path):
            # Recursively add all files inside directory
            for root, dirs, filenames in _os.walk(vault_path):
                for fname in filenames:
                    full_path = os.path.join(root, fname)
                    rel = os.path.relpath(full_path, os.path.join(os.getcwd(), PRIVATE_REPO_DIR))
                    paths_to_check.append(rel)
        else:
            rel = file_path
            paths_to_check.append(rel)
    
        try:
            diff_index = repo.index.diff(None)
            for rel_path in paths_to_check:
                changed = any(d.a_path == rel_path for d in diff_index)
                untracked = rel_path in repo.untracked_files
                if changed or untracked:
                    changed_files.append(rel_path)
        except GitCommandError:
            continue

    if changed_files:
        click.echo("Changed private files:")
        for f in changed_files:
            click.echo(f"  {f}")
    else:
        click.echo("No changes in private files.")

@cli.command()
@click.option('--message', '-m', default=None, help='Commit message')
def save(message):
    """Save changes of private files to private repo."""
    if not message:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        message = f"GitGhost backup on {now}"
    files = parse_gitghostinclude()
    if not files:
        return
    
    import subprocess
    private_repo_path = os.path.join(os.getcwd(), PRIVATE_REPO_DIR)
    repo = Repo(private_repo_path)
    if repo.head.is_valid():
        subprocess.run(["git", "-C", private_repo_path, "reset", "--hard", "HEAD"], check=True)
    else:
        click.echo("Private repo is empty, skipping reset.")

    # Copy private files into private repo dir
    copy_private_files(files)

    # Open or init private repo
    repo = ensure_private_repo()

    to_add = []
    for file_path in files:
        rel_path = file_path
        abs_path = os.path.join(os.getcwd(), PRIVATE_REPO_DIR, rel_path)
        if os.path.exists(abs_path):
            to_add.append(rel_path)

    if not to_add:
        click.echo("No files to add.")
        return

    try:
        repo.index.add(to_add)

        # Always commit if repo has no commits yet
        if not repo.head.is_valid() or repo.is_dirty(index=True, working_tree=True, untracked_files=True):
            repo.index.commit(message)
            origin = repo.remote(name='origin')
            try:
                origin.push()
            except GitCommandError as e:
                if "has no upstream branch" in str(e):
                    repo.git.push('--set-upstream', 'origin', repo.active_branch.name)
                else:
                    raise
            click.echo("Changes saved and pushed.")
        else:
            click.echo("No changes to commit.")
    except GitCommandError as e:
        click.echo(f"Git error: {e}")
@cli.command()
def discard():
    """Restore private files/folders from the last private repo commit, discarding local changes."""
    import shutil

    confirm = input("This will OVERWRITE your private files/folders with the last saved private vault snapshot. Are you sure? (y/n): ").strip().lower()
    if confirm not in ("y", "yes"):
        click.echo("Discard cancelled.")
        return

    files = parse_gitghostinclude()
    # Reset private repo working directory to last commit
    import subprocess
    subprocess.run(["git", "-C", os.path.join(os.getcwd(), PRIVATE_REPO_DIR), "reset", "--hard", "HEAD"], check=True)
    for file_path in files:
        src = os.path.join(os.getcwd(), PRIVATE_REPO_DIR, file_path)
        dest = os.path.join(os.getcwd(), file_path)

        if not os.path.exists(src):
            click.echo(f"Skipping missing in vault: {file_path}")
            continue

        if os.path.isdir(src):
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
            click.echo(f"Restored directory: {file_path}")
        else:
            dest_dir = os.path.dirname(dest)
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copy2(src, dest)
            click.echo(f"Restored file: {file_path}")

    click.echo("Private files/folders restored from private vault.")


@cli.command()
def init():
    """Initialize GitGhost: create .gitghostinclude, .gitghost_private repo, and update .gitignore."""
    # Create .gitghostinclude if missing
    if not os.path.exists(GITVAULT_INCLUDE):
        with open(GITVAULT_INCLUDE, "w") as f:
            f.write("# List private files and folders, one per line\n")
        click.echo(f"Created {GITVAULT_INCLUDE}")
    else:
        click.echo(f"{GITVAULT_INCLUDE} already exists.")

    # Create .gitghost_private directory and init repo
    private_repo_path = os.path.join(os.getcwd(), PRIVATE_REPO_DIR)
    if not os.path.exists(private_repo_path):
        os.makedirs(private_repo_path, exist_ok=True)
        Repo.init(private_repo_path)
        click.echo(f"Initialized private repo in {PRIVATE_REPO_DIR}")
    else:
        try:
            Repo(private_repo_path)
            click.echo(f"Private repo already exists in {PRIVATE_REPO_DIR}")
        except Exception:
            Repo.init(private_repo_path)
            click.echo(f"Initialized private repo in {PRIVATE_REPO_DIR}")

    # Add .gitghost_private/ to .gitignore if not present
    # Attempt to create private GitHub repo automatically if gh CLI is available
    import subprocess

    def has_gh():
        try:
            subprocess.run(["gh", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return True
        except Exception:
            return False

    def get_public_repo_name():
        try:
            repo = Repo(os.getcwd())
            url = next(repo.remote().urls)
            name = url.split("/")[-1]
            if name.endswith(".git"):
                name = name[:-4]
            return name
        except Exception:
            # fallback to current directory name
            return os.path.basename(os.getcwd())

    private_repo_url = None
    if has_gh():
        repo_name = get_public_repo_name() + "-gitghost"
        try:
            # Check if repo already exists
            result = subprocess.run(["gh", "repo", "view", repo_name, "--json", "name"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode != 0:
                # Repo does not exist, create it
                subprocess.run(["gh", "repo", "create", repo_name, "--private", "-y"], check=True)
            else:
                click.echo(f"Private GitHub repo '{repo_name}' already exists.")
            username = subprocess.check_output(["gh", "api", "user"], text=True)
            import json as js
            username = js.loads(username)["login"]
            private_repo_url = f"https://github.com/{username}/{repo_name}.git"
            repo = Repo(private_repo_path)
            if "origin" not in [r.name for r in repo.remotes]:
                repo.create_remote("origin", private_repo_url)
                click.echo(f"Created and added remote: {private_repo_url}")
        except Exception:
            click.echo("Failed to create private GitHub repo automatically. You can create it manually and add as remote.")
    else:
        click.echo("GitHub CLI (gh) not found. Skipping automatic private repo creation.")
    gitignore_path = os.path.join(os.getcwd(), ".gitignore")
    vault_block = "# GitGhost\n.gitghost_private/\n.gitghostinclude\n"
    
    def block_present(content):
        return ".gitghost_private/" in content and ".gitghostinclude" in content
    
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            content = f.read()
        if not block_present(content):
            content = content.rstrip()
            if content != "":
                content += "\n\n"  # ensure one blank line before block
            content += vault_block
            with open(gitignore_path, "w") as f:
                f.write(content)
            click.echo("Added GitGhost block to .gitignore")
        else:
            click.echo("GitGhost block already present in .gitignore")
    else:
        with open(gitignore_path, "w") as f:
            f.write(vault_block)
        click.echo("Created .gitignore with GitGhost block")

if __name__ == "__main__":
    cli()