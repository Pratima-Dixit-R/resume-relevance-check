# 🔐 Secure GitHub Setup Guide

## ⚠️ IMPORTANT SECURITY NOTICE

**DO NOT use your GitHub account password for Git operations.** GitHub requires Personal Access Tokens (PATs) for enhanced security.

## 🎯 Quick Setup Steps

### Step 1: Create Personal Access Token
1. Go to GitHub.com and log in
2. Click your profile picture → Settings
3. Scroll down to "Developer settings" → "Personal access tokens" → "Tokens (classic)"
4. Click "Generate new token (classic)"
5. Give it a name: "Resume Relevance Check App"
6. Select scopes: ✅ `repo` (Full control of private repositories)
7. Click "Generate token"
8. **COPY THE TOKEN** - you won't see it again!

### Step 2: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `resume-relevance-check`
3. Description: "AI-powered resume relevance analysis with Hugging Face transformers"
4. Choose Public or Private
5. **DO NOT** initialize with README
6. Click "Create repository"

### Step 3: Run Git Setup
Execute the git setup script:
```cmd
cd "c:\Users\prati\.vscode\resume-relevance-check"
git_setup.bat
```

### Step 4: Connect to GitHub
After running the setup script, execute these commands:

```cmd
"%LOCALAPPDATA%\Programs\Git\cmd\git.exe" remote add origin https://github.com/Pratima-Dixit-R/resume-relevance-check.git
"%LOCALAPPDATA%\Programs\Git\cmd\git.exe" push -u origin main
```

When prompted:
- **Username**: `Pratima-Dixit-R`
- **Password**: `[Your Personal Access Token]` (NOT your account password)

## 🔧 Alternative: Using Git Credential Manager

If you want to save credentials securely:

```cmd
git config --global credential.helper manager-core
```

This will open a browser for secure authentication.

## ✅ Verification

After successful push, your repository will be available at:
https://github.com/Pratima-Dixit-R/resume-relevance-check

## 🛡️ Security Best Practices

1. **Never commit passwords or API keys**
2. **Use Personal Access Tokens instead of passwords**
3. **Set token expiration dates**
4. **Regularly rotate tokens**
5. **Keep your `.env` file in `.gitignore`**

## 📱 Quick Commands Reference

```cmd
# Check status
git status

# Add all files
git add .

# Commit with message
git commit -m "Your commit message"

# Push to GitHub
git push origin main

# Check remote connections
git remote -v

# View commit history
git log --oneline -10
```

## 🚨 Troubleshooting

### Issue: "Authentication failed"
- **Solution**: Use Personal Access Token instead of password

### Issue: "Repository not found"
- **Solution**: Ensure repository exists on GitHub and URL is correct

### Issue: "Permission denied"
- **Solution**: Check if token has correct permissions (`repo` scope)

### Issue: "Git command not found"
- **Solution**: Restart terminal or add Git to PATH

## 📞 Need Help?

If you encounter issues:
1. Check the token permissions
2. Verify repository URL
3. Ensure Git is properly installed
4. Try using Git Bash instead of Command Prompt

---

**Remember**: Always use Personal Access Tokens for Git operations, never your GitHub password!