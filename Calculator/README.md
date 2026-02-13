# Scientific Calculator

A full-featured scientific calculator with a Python Flask backend and modern web frontend.

## 🎯 Overview

This application is a scientific calculator that separates concerns between the frontend and backend:
- **Frontend**: Handles user interface, input capture, and result display (HTML/CSS/JavaScript)
- **Backend**: Performs all mathematical calculations (Python/Flask)

All arithmetic operations are processed on the server, ensuring consistent calculation precision and allowing for easy maintenance and testing of mathematical functions.

## 📁 Project Structure

```
Calculator/
├── backend/                    # Python Flask backend
│   ├── __init__.py            # Package initialization
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── routes/                # API route handlers
│   │   ├── __init__.py
│   │   └── calculator.py      # Calculator API endpoints
│   └── services/              # Business logic layer
│       ├── __init__.py
│       └── calculator_service.py  # Mathematical operations
├── frontend/                   # Web frontend
│   ├── index.html             # Main HTML page
│   ├── css/
│   │   └── style.css          # Stylesheet
│   └── js/
│       └── app.js             # Frontend application logic
├── README.md                  # This file
└── .gitignore                 # Git ignore rules
```

## ✨ Features

### Basic Operations
- Addition, Subtraction, Multiplication, Division
- Modulo (remainder)
- Percentage calculations

### Scientific Functions
- **Trigonometric**: sin, cos, tan, sin⁻¹, cos⁻¹, tan⁻¹
- **Hyperbolic**: sinh, cosh, tanh
- **Logarithmic**: ln (natural log), log₁₀, log₂
- **Exponential**: eˣ, 10ˣ, 2ˣ
- **Power & Roots**: x², x³, xʸ, √x, ³√x

### Special Functions
- Factorial (n!)
- Absolute value (|x|)
- Reciprocal (1/x)
- Floor and Ceiling
- Permutation (nPr) and Combination (nCr)

### Additional Features
- **Degree/Radian Toggle**: Switch between angle modes
- **Memory Functions**: MC, MR, M+, M-, MS
- **Calculation History**: View and reuse previous calculations
- **Keyboard Support**: Use keyboard for input
- **Constants**: π (pi) and e (Euler's number)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd Calculator
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**

   **On Windows (PowerShell):**
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
   
   **On Windows (Command Prompt):**
   ```cmd
   .venv\Scripts\activate.bat
   ```
   
   **On macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```
   
   > **Note:** After activation, you should see `(.venv)` at the beginning of your terminal prompt, indicating the virtual environment is active.

   > **PowerShell Execution Policy:** If you get an error about scripts being disabled, run this command first (as Administrator):
   > ```powershell
   > Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   > ```

4. **Install Python dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

### Running the Application

1. **Ensure virtual environment is activated**
   
   You should see `(.venv)` in your terminal prompt. If not, activate it:
   ```powershell
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   ```

2. **Start the backend server**
   ```bash
   python backend/app.py
   ```
   The server will start at `http://localhost:5000`
   
   You should see output like:
   ```
   ==================================================
   Scientific Calculator Backend Server
   ==================================================
   Starting server at http://localhost:5000
   API endpoints available at http://localhost:5000/api/calculator/
   Press Ctrl+C to stop the server
   ==================================================
   ```

3. **Open the calculator**
   - Open your browser and navigate to `http://localhost:5000`
   - The calculator should load with "Server Connected" status in the bottom right

4. **To stop the server**
   - Press `Ctrl+C` in the terminal

### Quick Start (Windows PowerShell)

Run these commands in sequence:
```powershell
# Navigate to project directory
cd "C:\Users\mr\OneDrive\Documents\Projects\Calculator"

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Start the server
python backend/app.py
```

### Deactivating the Virtual Environment

When you're done, deactivate the virtual environment:
```bash
deactivate
```

## 🔌 API Documentation

### Base URL
```
http://localhost:5000/api/calculator
```

### Generic Calculate Endpoint
`POST /calculate`

Send any operation with its parameters:
```json
{
    "operation": "add",
    "params": {
        "a": 5,
        "b": 3
    }
}
```

### Response Format
```json
{
    "success": true,
    "result": 8
}
```

### Error Response
```json
{
    "success": false,
    "error": "Division by zero is not allowed"
}
```

### Available Operations

#### Basic Arithmetic
| Operation | Parameters | Description |
|-----------|------------|-------------|
| `add` | `a`, `b` | Add two numbers |
| `subtract` | `a`, `b` | Subtract b from a |
| `multiply` | `a`, `b` | Multiply two numbers |
| `divide` | `a`, `b` | Divide a by b |
| `modulo` | `a`, `b` | Get remainder |

#### Power & Roots
| Operation | Parameters | Description |
|-----------|------------|-------------|
| `power` | `base`, `exponent` | Calculate base^exponent |
| `square` | `a` | Calculate a² |
| `cube` | `a` | Calculate a³ |
| `sqrt` | `a` | Square root |
| `cbrt` | `a` | Cube root |
| `nthroot` | `a`, `n` | Nth root of a |

#### Trigonometric
| Operation | Parameters | Description |
|-----------|------------|-------------|
| `sin`, `cos`, `tan` | `angle`, `degrees` (optional) | Trig functions |
| `asin`, `acos`, `atan` | `value`, `degrees` (optional) | Inverse trig |
| `sinh`, `cosh`, `tanh` | `value` | Hyperbolic functions |

#### Logarithmic & Exponential
| Operation | Parameters | Description |
|-----------|------------|-------------|
| `log` | `a` | Natural logarithm |
| `log10` | `a` | Base-10 logarithm |
| `log2` | `a` | Base-2 logarithm |
| `logbase` | `a`, `base` | Custom base |
| `exp` | `a` | e^a |
| `exp10` | `a` | 10^a |

#### Special Functions
| Operation | Parameters | Description |
|-----------|------------|-------------|
| `factorial` | `n` | n! |
| `abs` | `a` | Absolute value |
| `reciprocal` | `a` | 1/a |
| `permutation` | `n`, `r` | nPr |
| `combination` | `n`, `r` | nCr |

### Dedicated Endpoints

Each operation also has its own endpoint:
- `POST /add` - `{"a": 5, "b": 3}`
- `POST /sqrt` - `{"a": 16}`
- `GET /pi` - Returns π value
- `GET /e` - Returns e value

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `0-9` | Enter numbers |
| `.` | Decimal point |
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `^` | Power |
| `%` | Modulo |
| `Enter` or `=` | Calculate |
| `Escape` | Clear all |
| `Backspace` | Delete last digit |
| `Delete` | Clear entry |

## 🛠️ Development

### Running Tests
```bash
# Navigate to backend directory
cd backend

# Run tests (if available)
python -m pytest
```

### Code Structure

#### Backend
- `app.py`: Flask application factory and server configuration
- `routes/calculator.py`: API endpoint definitions
- `services/calculator_service.py`: Mathematical operations implementation

#### Frontend
- `index.html`: Calculator UI structure
- `css/style.css`: Visual styling
- `js/app.js`: Frontend logic and API communication

## 🔒 Error Handling

The calculator handles various mathematical errors:
- Division by zero
- Invalid logarithm inputs (negative numbers)
- Invalid trigonometric inverse inputs (outside [-1, 1])
- Negative numbers for square root
- Factorial of negative numbers

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📧 Support

If you encounter any issues or have questions, please open an issue in the repository.
