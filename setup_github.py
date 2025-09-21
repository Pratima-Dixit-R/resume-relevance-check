#!/usr/bin/env python3
"""
Git Repository Setup Script for Resume Relevance Check
Creates and pushes to GitHub repository: resume-relevance-check
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Optional

class GitSetup:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.git_path = self._find_git_executable()
        self.repo_name = "resume-relevance-check"
        self.github_username = "Pratima-Dixit-R"
        self.user_email = "pratimadixit2305@gmail.com"
        
    def _find_git_executable(self) -> str:
        """Find Git executable path"""
        # Common Git paths on Windows
        possible_paths = [
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Git\cmd\git.exe"),
            r"C:\Program Files\Git\cmd\git.exe",
            r"C:\Program Files (x86)\Git\cmd\git.exe",
            "git"  # If in PATH
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, "--version"], 
                                       capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ Found Git at: {path}")
                    return path
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        raise RuntimeError("❌ Git not found. Please install Git first.")
    
    def _run_git_command(self, args: list, check: bool = True) -> subprocess.CompletedProcess:
        """Run a git command and return the result"""
        cmd = [self.git_path] + args
        print(f"🔧 Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd, 
                cwd=self.project_root,
                capture_output=True, 
                text=True, 
                timeout=60
            )
            
            if result.stdout:
                print(f"📄 Output: {result.stdout.strip()}")
            if result.stderr and result.returncode != 0:
                print(f"⚠️ Error: {result.stderr.strip()}")
            
            if check and result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
            
            return result
        except subprocess.TimeoutExpired:
            print("⏰ Command timed out")
            raise
    
    def setup_git_config(self):
        """Configure Git user information"""
        print("\n🔧 Configuring Git user information...")
        
        self._run_git_command(["config", "user.name", self.github_username])
        self._run_git_command(["config", "user.email", self.user_email])
        
        # Configure line endings for Windows
        self._run_git_command(["config", "core.autocrlf", "true"])
        
        print("✅ Git configuration complete")
    
    def initialize_repository(self):
        """Initialize Git repository if not already initialized"""
        print("\n📂 Initializing Git repository...")
        
        git_dir = self.project_root / ".git"
        if git_dir.exists():
            print("✅ Git repository already initialized")
            return
        
        self._run_git_command(["init"])
        print("✅ Git repository initialized")
    
    def add_and_commit_files(self):
        """Add all files and create initial commit"""
        print("\n📁 Adding files to Git...")
        
        # Add all files
        self._run_git_command(["add", "."])
        
        # Check if there are changes to commit
        status_result = self._run_git_command(["status", "--porcelain"], check=False)
        if not status_result.stdout.strip():
            print("✅ No changes to commit")
            return
        
        # Commit files
        commit_message = "Initial commit: Resume Relevance Check with AI enhancements"
        self._run_git_command(["commit", "-m", commit_message])
        
        print("✅ Files committed successfully")
    
    def add_github_remote(self):
        """Add GitHub remote origin"""
        print("\n🌐 Setting up GitHub remote...")
        
        github_url = f"https://github.com/{self.github_username}/{self.repo_name}.git"
        
        # Check if remote already exists
        remotes_result = self._run_git_command(["remote", "-v"], check=False)
        if "origin" in remotes_result.stdout:
            print("✅ Remote 'origin' already exists")
            return
        
        # Add remote
        self._run_git_command(["remote", "add", "origin", github_url])
        
        print(f"✅ Added remote: {github_url}")
    
    def push_to_github(self):
        """Push repository to GitHub"""
        print("\n🚀 Pushing to GitHub...")
        print("\n⚠️ IMPORTANT: You will be prompted for credentials.")
        print("   Username: Pratima-Dixit-R")
        print("   Password: Use a Personal Access Token (NOT your GitHub password)")
        print("\n🔑 To create a Personal Access Token:")
        print("   1. Go to GitHub.com → Settings → Developer settings")
        print("   2. Personal access tokens → Tokens (classic)")
        print("   3. Generate new token with 'repo' scope")
        print("\n⏳ Attempting to push...")
        
        try:
            # Push to GitHub
            self._run_git_command(["push", "-u", "origin", "main"])
            print("🎉 Successfully pushed to GitHub!")
            print(f"\n🌐 Repository URL: https://github.com/{self.github_username}/{self.repo_name}")
            
        except subprocess.CalledProcessError as e:
            print("❌ Failed to push to GitHub")
            print("\n🔧 Possible solutions:")
            print("   1. Create the repository on GitHub first:")
            print(f"      https://github.com/new")
            print("   2. Repository name: resume-relevance-check")
            print("   3. Use Personal Access Token for authentication")
            print("\n🔄 After creating the repository, run this script again")
            raise
    
    def create_gitignore(self):
        """Create or update .gitignore file"""
        gitignore_content = """
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/settings.json
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite
*.sqlite3

# Logs
*.log
logs/

# Environment variables
.env.local
.env.production

# Temporary files
*.tmp
*.temp
temp/
tmp/

# Upload directories
uploads/
data/temp/

# Model files
*.pkl
*.joblib
models/

# API keys and secrets
secrets.txt
api_keys.txt

# Git artifacts
tatus
"""
        
        gitignore_path = self.project_root / ".gitignore"
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write(gitignore_content.strip())
        
        print("✅ Created/updated .gitignore")
    
    def show_status(self):
        """Show current Git status"""
        print("\n📊 Current Git Status:")
        print("-" * 40)
        
        try:
            # Show status
            self._run_git_command(["status", "--short"])
            
            # Show remotes
            print("\n🌐 Remote repositories:")
            self._run_git_command(["remote", "-v"])
            
            # Show recent commits
            print("\n📝 Recent commits:")
            self._run_git_command(["log", "--oneline", "-5"])
            
        except subprocess.CalledProcessError:
            print("⚠️ Could not get Git status")
    
    def run_setup(self):
        """Run the complete Git setup process"""
        print("🚀 Resume Relevance Check - Git Repository Setup")
        print("=" * 60)
        
        try:
            # Setup steps
            self.create_gitignore()
            self.initialize_repository()
            self.setup_git_config()
            self.add_and_commit_files()
            self.add_github_remote()
            
            # Show instructions before pushing
            print("\n" + "=" * 60)
            print("🎯 READY TO PUSH TO GITHUB")
            print("=" * 60)
            
            print("\n📋 Pre-push checklist:")
            print("   ✅ Repository configured")
            print("   ✅ Files committed")
            print("   ✅ Remote added")
            
            print("\n🌐 Next steps:")
            print("   1. Create repository on GitHub:")
            print(f"      https://github.com/new")
            print("   2. Repository name: resume-relevance-check")
            print("   3. Choose Public or Private")
            print("   4. DO NOT initialize with README")
            print("   5. Click 'Create repository'")
            
            # Ask user if they want to push now
            print("\n🚀 Push to GitHub now? (y/n): ", end="")
            response = input().lower().strip()
            
            if response in ['y', 'yes']:
                self.push_to_github()
            else:
                print("\n⏸️ Skipping push. To push later, run:")
                print(f"   {self.git_path} push -u origin main")
            
            # Show final status
            self.show_status()
            
            print("\n🎉 Git setup complete!")
            
        except Exception as e:
            print(f"\n❌ Setup failed: {e}")
            print("\n🔧 Manual setup instructions:")
            print("   1. Install Git if not already installed")
            print("   2. Create GitHub repository manually")
            print("   3. Run git commands manually")
            return False
        
        return True

def main():
    """Main function"""
    project_root = Path(__file__).parent
    
    # Change to project directory
    os.chdir(project_root)
    
    git_setup = GitSetup(project_root)
    success = git_setup.run_setup()
    
    if success:
        print("\n✅ All done! Your repository is ready.")
    else:
        print("\n❌ Setup incomplete. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)