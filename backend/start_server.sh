#!/bin/bash


echo "=========================================="
echo "  SurakshaSetu Legal RAG API - Port 3000"
echo "=========================================="
echo ""


if ! command -v python3 &> /dev/null; then
    echo " Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo " Python 3 found: $(python3 --version)"
echo ""


echo "🔍 Checking required packages..."

REQUIRED_PACKAGES=(
    "fastapi"
    "uvicorn"
    "sentence_transformers"
    "faiss"
    "google"
    "numpy"
    "pydantic"
)

MISSING_PACKAGES=()

for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! python3 -c "import $package" 2>/dev/null; then
        MISSING_PACKAGES+=("$package")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -ne 0 ]; then
    echo "  Missing packages detected: ${MISSING_PACKAGES[*]}"
    echo ""
    read -p "Would you like to install them now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo " Installing required packages..."
        pip install fastapi uvicorn sentence-transformers faiss-cpu google-genai numpy pydantic requests
    else
        echo "Cannot start without required packages. Please install them manually:"
        echo "   pip install fastapi uvicorn sentence-transformers faiss-cpu google-genai numpy pydantic requests"
        exit 1
    fi
fi

echo "✅ All required packages are installed"
echo ""

# Check for Gemini API key
if [ -z "$GEMINI_API_KEY" ]; then
    echo "GEMINI_API_KEY environment variable not set"
    read -p "Enter your Gemini API key (or press Enter to use default): " api_key
    if [ -n "$api_key" ]; then
        export GEMINI_API_KEY="$api_key"
        echo "API key set for this session"
    else
        echo " Using default API key from code (not recommended for production)"
    fi
else
    echo "GEMINI_API_KEY is set"
fi

echo ""
echo "Starting server on port 3000..."
echo ""
echo "Server will be available at:"
echo "   • http://localhost:3000/          - API Status"
echo "   • http://localhost:3000/docs      - API Documentation"
echo "   • http://localhost:3000/health    - Health Check"
echo ""
echo " Press Ctrl+C to stop the server"
echo ""
echo "=========================================="
echo ""

# Start the server
python3 combined_backend.py
