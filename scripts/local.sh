#!/bin/bash

# Default flag values
clean=false
lint=false
run=false

print_help() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  -c, clean    Remove the existing virtual environment."
    echo "  -l, lint     Run linting and formatting on the application code."
    echo "  -r, run      Run the application with the existing or newly created environment."
    echo "  -h, help     Display this help message."
    echo
    exit 0
}

# Parse command-line options
for arg in "$@"; do
    case $arg in
        -c|clean)
            clean=true
            ;;
        -l|lint)
            lint=true
            ;;
        -r|run)
            run=true
            ;;
        -h|help)
            print_help
            ;;
        *)
            echo "Invalid option: $arg"
            print_help
            ;;
    esac
done

clean_environment() {
    if [ -d "venv" ]; then
        echo "Removing existing virtual environment..."
        rm -rf venv
    else
        echo "No virtual environment found."
    fi
}

setup_environment() {
    if [ ! -d "venv" ]; then
        echo "Virtual environment not found. Setting up environment..."

        # Create virtual environment and activate
        echo "Creating virtual environment..."
        python3 -m venv venv
        source venv/bin/activate

        # Install dependencies
        echo "Installing dependencies..."
        pip install --no-cache-dir -r requirements.txt
    else
        echo "Virtual environment found. Activating..."
        source venv/bin/activate
    fi
}

lint_and_format() {
    # Run formatting
    echo "Running formatting..."
    ./scripts/format_local.sh

    # Run linting and type checking
    echo "Running linting and type checking..."
    ./scripts/lint.sh
}

run_application() {
    echo "Running the application..."
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir app
}

# Main logic to manage provided flags
if [ "$clean" = true ]; then
    clean_environment
fi

if [ "$lint" = true ]; then
    setup_environment
    lint_and_format
fi

if [ "$run" = true ]; then
    setup_environment
    run_application
fi
