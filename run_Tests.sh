#!/bin/bash

echo "================================================================"
echo "Starting CI Test Runner for Pink Morsel Sales Visualizer"
echo "================================================================"

# Set script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Function to print colored output
print_green() {
    echo -e "\033[0;32m$1\033[0m"
}

print_red() {
    echo -e "\033[0;31m$1\033[0m"
}

print_yellow() {
    echo -e "\033[0;33m$1\033[0m"
}

# Check if virtual environment exists
VENV_PATH="venv"
if [ -d "$VENV_PATH" ]; then
    print_green "Virtual environment found at $VENV_PATH"
    
    # Activate virtual environment
    if [ -f "$VENV_PATH/bin/activate" ]; then
        source "$VENV_PATH/bin/activate"
        print_green "Virtual environment activated"
    elif [ -f "$VENV_PATH/Scripts/activate" ]; then
        # Windows (Git Bash/Cygwin)
        source "$VENV_PATH/Scripts/activate"
        print_green "Virtual environment activated (Windows)"
    else
        print_red "Could not find activate script in virtual environment"
        exit 1
    fi
else
    print_yellow "Virtual environment not found. Creating one..."
    
    # Create virtual environment
    python3 -m venv "$VENV_PATH"
    
    if [ $? -eq 0 ]; then
        print_green "Virtual environment created"
        
        # Activate virtual environment
        if [ -f "$VENV_PATH/bin/activate" ]; then
            source "$VENV_PATH/bin/activate"
            print_green "Virtual environment activated"
        elif [ -f "$VENV_PATH/Scripts/activate" ]; then
            source "$VENV_PATH/Scripts/activate"
            print_green "Virtual environment activated (Windows)"
        else
            print_red "Could not find activate script in new virtual environment"
            exit 1
        fi
        
        # Install requirements
        print_yellow "Installing requirements..."
        pip install --upgrade pip
        if [ -f "requirements.txt" ]; then
            pip install -r requirements.txt
        else
            # Install minimum required packages
            pip install dash pandas plotly pytest
        fi
        print_green "Requirements installed"
    else
        print_red "Failed to create virtual environment"
        exit 1
    fi
fi

# Check Python version
echo ""
print_yellow "Python Environment Information:"
python --version
pip --version

# Check if app.py exists
if [ ! -f "app.py" ]; then
    print_red "app.py not found in current directory"
    exit 1
fi

# Check if test file exists
if [ ! -f "test_dash_app.py" ]; then
    print_red "test_dash_app.py not found in current directory"
    exit 1
fi

# Run the tests
echo ""
print_yellow "Running test suite..."
echo "---------------------------------------------------------------"

python test_dash_app.py
TEST_EXIT_CODE=$?

echo ""
echo "---------------------------------------------------------------"

if [ $TEST_EXIT_CODE -eq 0 ]; then
    print_green "All tests passed!"
    echo "Exit code: 0 (Success)"
else
    print_red "Tests failed!"
    echo "Exit code: 1 (Failure)"
fi

# Deactivate virtual environment if we activated it
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
    print_green "Virtual environment deactivated"
fi

echo "================================================================"
exit $TEST_EXIT_CODE