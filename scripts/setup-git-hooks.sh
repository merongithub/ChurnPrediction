#!/bin/bash
# Setup script for Git hooks in Churn Prediction Project

set -e

echo "🔧 Setting up Git hooks for Churn Prediction Project..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Check if we're in a Git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a Git repository. Please run this script from the project root."
    exit 1
fi

# Create scripts directory if it doesn't exist
if [ ! -d "scripts" ]; then
    mkdir -p scripts
    print_info "Created scripts directory"
fi

# Make the pre-commit hook executable
if [ -f "scripts/pre-commit-hook.sh" ]; then
    chmod +x scripts/pre-commit-hook.sh
    print_success "Made pre-commit hook executable"
else
    echo "❌ Error: pre-commit-hook.sh not found in scripts directory"
    exit 1
fi

# Create .git/hooks directory if it doesn't exist
if [ ! -d ".git/hooks" ]; then
    mkdir -p .git/hooks
    print_info "Created .git/hooks directory"
fi

# Copy pre-commit hook
cp scripts/pre-commit-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
print_success "Installed pre-commit hook"

# Create a post-commit hook for reminders
cat > .git/hooks/post-commit << 'EOF'
#!/bin/bash
# Post-commit hook for Churn Prediction Project

echo ""
echo "🔍 Remember to:"
echo "  - Run 'python -m config.validate_config' to verify configuration"
echo "  - Test your changes before pushing"
echo "  - Update documentation if needed"
echo "  - Check for any sensitive information in your commits"
echo ""
EOF

chmod +x .git/hooks/post-commit
print_success "Installed post-commit hook"

# Create a commit-msg hook to check commit message format
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/bash
# Commit message hook for Churn Prediction Project

commit_msg_file="$1"
commit_msg=$(cat "$commit_msg_file")

# Check for conventional commit format
if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|test|chore|ci|build|perf|revert)(\(.+\))?: .+"; then
    echo ""
    echo "⚠️  Warning: Commit message doesn't follow conventional format"
    echo "Recommended format: <type>(<scope>): <description>"
    echo "Types: feat, fix, docs, style, refactor, test, chore, ci, build, perf, revert"
    echo "Example: feat(config): add centralized secrets management"
    echo ""
    echo "Current message: $commit_msg"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
EOF

chmod +x .git/hooks/commit-msg
print_success "Installed commit-msg hook"

# Create a pre-push hook for additional checks
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
# Pre-push hook for Churn Prediction Project

echo "🔍 Running pre-push checks..."

# Check if configuration is valid
if command -v python &> /dev/null; then
    if python -c "from config import get_config; config = get_config(); print('Configuration loaded successfully')" 2>/dev/null; then
        echo "✅ Configuration validation passed"
    else
        echo "⚠️  Warning: Configuration validation failed"
        echo "Run 'python -m config.validate_config' to check your configuration"
    fi
else
    echo "⚠️  Warning: Python not found, skipping configuration validation"
fi

# Check for any uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Warning: You have uncommitted changes"
    echo "Consider committing or stashing them before pushing"
fi

echo "✅ Pre-push checks completed"
EOF

chmod +x .git/hooks/pre-push
print_success "Installed pre-push hook"

echo ""
print_success "Git hooks setup completed!"
echo ""
echo "📋 Installed hooks:"
echo "  - pre-commit: Security checks and file validation"
echo "  - commit-msg: Commit message format validation"
echo "  - post-commit: Reminders and best practices"
echo "  - pre-push: Configuration validation and status checks"
echo ""
echo "🔧 To test the hooks:"
echo "  - Try committing a .env file (should be blocked)"
echo "  - Try committing a large file (should show warning)"
echo "  - Try committing with a non-conventional message (should show warning)"
echo ""
echo "📚 For more information, see SECURITY.md" 