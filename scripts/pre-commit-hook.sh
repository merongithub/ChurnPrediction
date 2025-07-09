#!/bin/bash
# Pre-commit hook for Churn Prediction Project
# This script prevents accidental commits of sensitive files

set -e

echo "🔍 Running pre-commit security checks..."

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Function to print colored output
print_error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Check for sensitive file extensions
SENSITIVE_EXTENSIONS=("json" "key" "pem" "p12" "pfx" "crt" "cert" "p8" "pem")
SENSITIVE_FILES=()

for ext in "${SENSITIVE_EXTENSIONS[@]}"; do
    while IFS= read -r -d '' file; do
        # Skip package.json and other safe JSON files
        if [[ "$file" == "package.json" ]] || [[ "$file" == "tsconfig.json" ]] || [[ "$file" == "jsconfig.json" ]]; then
            continue
        fi
        SENSITIVE_FILES+=("$file")
    done < <(git diff --cached --name-only --diff-filter=A | grep -E "\.$ext$" | tr '\n' '\0' 2>/dev/null || true)
done

if [ ${#SENSITIVE_FILES[@]} -gt 0 ]; then
    print_error "Potentially sensitive files detected:"
    for file in "${SENSITIVE_FILES[@]}"; do
        echo "  - $file"
    done
    echo ""
    echo "Please review these files and ensure no credentials are being committed."
    echo "If these files are safe to commit, add them to .gitignore exceptions."
    exit 1
fi

# Check for environment files
ENV_FILES=()
while IFS= read -r -d '' file; do
    ENV_FILES+=("$file")
done < <(git diff --cached --name-only --diff-filter=A | grep -E "\.env" | tr '\n' '\0' 2>/dev/null || true)

if [ ${#ENV_FILES[@]} -gt 0 ]; then
    print_error "Environment files detected:"
    for file in "${ENV_FILES[@]}"; do
        echo "  - $file"
    done
    echo ""
    echo "Please use env.example instead of committing actual environment files."
    echo "Environment files may contain sensitive information."
    exit 1
fi

# Check for large files (>10MB)
LARGE_FILES=()
while IFS= read -r -d '' file; do
    size=$(git cat-file -s "$(git rev-parse HEAD:$file)" 2>/dev/null || echo "0")
    if [ "$size" -gt 10485760 ]; then  # 10MB in bytes
        LARGE_FILES+=("$file ($(numfmt --to=iec $size))")
    fi
done < <(git diff --cached --name-only --diff-filter=A | tr '\n' '\0' 2>/dev/null || true)

if [ ${#LARGE_FILES[@]} -gt 0 ]; then
    print_warning "Large files detected:"
    for file in "${LARGE_FILES[@]}"; do
        echo "  - $file"
    done
    echo ""
    echo "Consider using Git LFS or storing these files in cloud storage."
    echo "Large files can bloat the repository and slow down operations."
fi

# Check for common sensitive patterns in code
SENSITIVE_PATTERNS=(
    "password.*=.*['\"]"
    "secret.*=.*['\"]"
    "key.*=.*['\"]"
    "token.*=.*['\"]"
    "credential.*=.*['\"]"
    "api_key.*=.*['\"]"
    "access_key.*=.*['\"]"
    "private_key.*=.*['\"]"
)

PATTERN_VIOLATIONS=()
for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    while IFS= read -r -d '' file; do
        # Skip binary files
        if file "$file" | grep -q "text"; then
            if grep -q "$pattern" "$file" 2>/dev/null; then
                PATTERN_VIOLATIONS+=("$file (pattern: $pattern)")
            fi
        fi
    done < <(git diff --cached --name-only --diff-filter=A | tr '\n' '\0' 2>/dev/null || true)
done

if [ ${#PATTERN_VIOLATIONS[@]} -gt 0 ]; then
    print_warning "Potential secrets detected in code:"
    for violation in "${PATTERN_VIOLATIONS[@]}"; do
        echo "  - $violation"
    done
    echo ""
    echo "Please review these files for hardcoded secrets."
    echo "Use environment variables or configuration files instead."
fi

# Check for model files
MODEL_FILES=()
while IFS= read -r -d '' file; do
    MODEL_FILES+=("$file")
done < <(git diff --cached --name-only --diff-filter=A | grep -E "\.(joblib|pkl|pickle|h5|hdf5|pb|onnx|pt|pth|ckpt|safetensors)$" | tr '\n' '\0' 2>/dev/null || true)

if [ ${#MODEL_FILES[@]} -gt 0 ]; then
    print_warning "Model files detected:"
    for file in "${MODEL_FILES[@]}"; do
        echo "  - $file"
    done
    echo ""
    echo "Model files should be stored in cloud storage, not in Git."
    echo "Consider using Google Cloud Storage for model artifacts."
fi

# Check for data files
DATA_FILES=()
while IFS= read -r -d '' file; do
    DATA_FILES+=("$file")
done < <(git diff --cached --name-only --diff-filter=A | grep -E "\.(csv|parquet|feather|hdf|xlsx|xls|db|sqlite|sqlite3)$" | tr '\n' '\0' 2>/dev/null || true)

if [ ${#DATA_FILES[@]} -gt 0 ]; then
    print_warning "Data files detected:"
    for file in "${DATA_FILES[@]}"; do
        echo "  - $file"
    done
    echo ""
    echo "Data files should be stored in cloud storage, not in Git."
    echo "Consider using Google Cloud Storage for data files."
fi

# Check for configuration files with real values
CONFIG_VIOLATIONS=()
while IFS= read -r -d '' file; do
    if grep -q "your-gcp-project-id\|your-bucket-name" "$file" 2>/dev/null; then
        CONFIG_VIOLATIONS+=("$file (contains placeholder values)")
    fi
done < <(git diff --cached --name-only --diff-filter=A | grep -E "config/.*\.py$" | tr '\n' '\0' 2>/dev/null || true)

if [ ${#CONFIG_VIOLATIONS[@]} -gt 0 ]; then
    print_warning "Configuration files with placeholder values detected:"
    for violation in "${CONFIG_VIOLATIONS[@]}"; do
        echo "  - $violation"
    done
    echo ""
    echo "Please ensure configuration files use proper values or environment variables."
fi

# All checks passed
print_success "Pre-commit checks passed!"
print_success "No sensitive files detected."

echo ""
echo "📋 Remember to:"
echo "  - Use environment variables for secrets"
echo "  - Store data and models in cloud storage"
echo "  - Use the configuration system for settings"
echo "  - Review all changes before committing"

exit 0 