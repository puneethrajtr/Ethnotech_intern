/**
 * Scientific Calculator Frontend Application
 * 
 * This module handles all frontend logic for the scientific calculator.
 * It manages user input, sends calculation requests to the Python backend,
 * and displays results. No arithmetic operations are performed here.
 */

// ==================== Configuration ====================

const API_BASE_URL = 'http://localhost:5000/api/calculator';

// ==================== State Management ====================

const state = {
    currentValue: '0',
    previousValue: null,
    currentOperation: null,
    waitingForSecondOperand: false,
    memory: 0,
    history: [],
    degreeMode: true,
    lastResult: null
};

// ==================== DOM Elements ====================

const display = document.getElementById('display');
const expression = document.getElementById('expression');
const modeToggle = document.getElementById('degreeMode');
const modeIndicator = document.getElementById('modeIndicator');
const memoryStatus = document.getElementById('memoryStatus');
const serverStatus = document.getElementById('serverStatus');
const historyList = document.getElementById('historyList');
const clearHistoryBtn = document.getElementById('clearHistory');

// ==================== API Communication ====================

/**
 * Send a calculation request to the backend API.
 * @param {string} operation - The operation to perform
 * @param {object} params - Parameters for the operation
 * @returns {Promise<number>} - The result of the calculation
 */
async function calculate(operation, params) {
    try {
        const response = await fetch(`${API_BASE_URL}/calculate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ operation, params })
        });
        
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Calculation failed');
        }
        
        return data.result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * Get a constant value from the backend.
 * @param {string} constant - The constant name ('pi' or 'e')
 * @returns {Promise<number>} - The constant value
 */
async function getConstant(constant) {
    try {
        const response = await fetch(`${API_BASE_URL}/${constant}`);
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Failed to get constant');
        }
        
        return data.result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * Check if the backend server is available.
 */
async function checkServerStatus() {
    try {
        const response = await fetch('http://localhost:5000/api/health');
        const data = await response.json();
        
        if (data.status === 'healthy') {
            serverStatus.textContent = '● Server Connected';
            serverStatus.className = 'status-item connected';
        }
    } catch (error) {
        serverStatus.textContent = '○ Server Disconnected';
        serverStatus.className = 'status-item disconnected';
    }
}

// ==================== Display Functions ====================

/**
 * Update the calculator display.
 */
function updateDisplay() {
    display.value = formatNumber(state.currentValue);
    display.classList.remove('error');
}

/**
 * Update the expression display.
 */
function updateExpression() {
    if (state.previousValue !== null && state.currentOperation) {
        const opSymbol = getOperatorSymbol(state.currentOperation);
        expression.textContent = `${formatNumber(state.previousValue)} ${opSymbol}`;
    } else {
        expression.textContent = '';
    }
}

/**
 * Format a number for display.
 * @param {string|number} value - The value to format
 * @returns {string} - Formatted number string
 */
function formatNumber(value) {
    if (value === 'Error' || value === 'Infinity' || value === '-Infinity') {
        return value;
    }
    
    const num = parseFloat(value);
    
    if (isNaN(num)) {
        return 'Error';
    }
    
    // Handle very large or very small numbers
    if (Math.abs(num) >= 1e15 || (Math.abs(num) < 1e-10 && num !== 0)) {
        return num.toExponential(8);
    }
    
    // Round to avoid floating point issues
    const rounded = parseFloat(num.toPrecision(12));
    return rounded.toString();
}

/**
 * Get the display symbol for an operator.
 * @param {string} operation - The operation name
 * @returns {string} - The display symbol
 */
function getOperatorSymbol(operation) {
    const symbols = {
        'add': '+',
        'subtract': '−',
        'multiply': '×',
        'divide': '÷',
        'power': '^',
        'modulo': 'mod',
        'permutation': 'P',
        'combination': 'C'
    };
    return symbols[operation] || operation;
}

/**
 * Show an error message on the display.
 * @param {string} message - The error message
 */
function showError(message) {
    display.value = message || 'Error';
    display.classList.add('error');
    state.currentValue = '0';
}

// ==================== Input Handling ====================

/**
 * Handle number button clicks.
 * @param {string} digit - The digit pressed
 */
function inputDigit(digit) {
    if (state.waitingForSecondOperand) {
        state.currentValue = digit;
        state.waitingForSecondOperand = false;
    } else {
        state.currentValue = state.currentValue === '0' ? digit : state.currentValue + digit;
    }
    updateDisplay();
}

/**
 * Handle decimal point input.
 */
function inputDecimal() {
    if (state.waitingForSecondOperand) {
        state.currentValue = '0.';
        state.waitingForSecondOperand = false;
        updateDisplay();
        return;
    }
    
    if (!state.currentValue.includes('.')) {
        state.currentValue += '.';
        updateDisplay();
    }
}

/**
 * Handle backspace.
 */
function backspace() {
    if (state.currentValue.length > 1) {
        state.currentValue = state.currentValue.slice(0, -1);
    } else {
        state.currentValue = '0';
    }
    updateDisplay();
}

/**
 * Clear the current entry.
 */
function clearEntry() {
    state.currentValue = '0';
    updateDisplay();
}

/**
 * Clear all calculator state.
 */
function clearAll() {
    state.currentValue = '0';
    state.previousValue = null;
    state.currentOperation = null;
    state.waitingForSecondOperand = false;
    updateDisplay();
    updateExpression();
}

// ==================== Binary Operations ====================

/**
 * Handle binary operator input (operations requiring two operands).
 * @param {string} operation - The operation to perform
 */
async function handleBinaryOperator(operation) {
    const currentValue = parseFloat(state.currentValue);
    
    // If there's a pending operation, calculate it first
    if (state.currentOperation && state.waitingForSecondOperand) {
        state.currentOperation = operation;
        updateExpression();
        return;
    }
    
    if (state.previousValue !== null && state.currentOperation && !state.waitingForSecondOperand) {
        try {
            display.classList.add('calculating');
            const result = await performBinaryOperation();
            state.currentValue = result.toString();
            state.previousValue = result;
            updateDisplay();
        } catch (error) {
            showError(error.message);
            return;
        } finally {
            display.classList.remove('calculating');
        }
    } else {
        state.previousValue = currentValue;
    }
    
    state.currentOperation = operation;
    state.waitingForSecondOperand = true;
    updateExpression();
}

/**
 * Perform the pending binary operation.
 * @returns {Promise<number>} - The result
 */
async function performBinaryOperation() {
    const params = {
        a: state.previousValue,
        b: parseFloat(state.currentValue)
    };
    
    // Special handling for power operation
    if (state.currentOperation === 'power') {
        params.base = state.previousValue;
        params.exponent = parseFloat(state.currentValue);
        delete params.a;
        delete params.b;
    }
    
    // Special handling for permutation/combination
    if (state.currentOperation === 'permutation' || state.currentOperation === 'combination') {
        params.n = state.previousValue;
        params.r = parseFloat(state.currentValue);
        delete params.a;
        delete params.b;
    }
    
    return await calculate(state.currentOperation, params);
}

/**
 * Handle equals button - execute pending operation.
 */
async function handleEquals() {
    if (state.currentOperation === null || state.waitingForSecondOperand) {
        return;
    }
    
    try {
        display.classList.add('calculating');
        
        const expressionStr = `${formatNumber(state.previousValue)} ${getOperatorSymbol(state.currentOperation)} ${formatNumber(state.currentValue)}`;
        const result = await performBinaryOperation();
        
        // Add to history
        addToHistory(expressionStr, result);
        
        state.currentValue = result.toString();
        state.previousValue = null;
        state.currentOperation = null;
        state.waitingForSecondOperand = false;
        state.lastResult = result;
        
        updateDisplay();
        updateExpression();
    } catch (error) {
        showError(error.message);
    } finally {
        display.classList.remove('calculating');
    }
}

// ==================== Unary Operations ====================

/**
 * Handle unary operations (operations on single value).
 * @param {string} operation - The operation to perform
 */
async function handleUnaryOperation(operation) {
    const currentValue = parseFloat(state.currentValue);
    
    try {
        display.classList.add('calculating');
        
        let result;
        let params = {};
        
        switch (operation) {
            // Trigonometric
            case 'sin':
            case 'cos':
            case 'tan':
                params = { angle: currentValue, degrees: state.degreeMode };
                result = await calculate(operation, params);
                break;
            
            case 'asin':
            case 'acos':
            case 'atan':
                params = { value: currentValue, degrees: state.degreeMode };
                result = await calculate(operation, params);
                break;
            
            // Hyperbolic
            case 'sinh':
            case 'cosh':
            case 'tanh':
                params = { value: currentValue };
                result = await calculate(operation, params);
                break;
            
            // Logarithmic
            case 'log':
            case 'log10':
            case 'log2':
                params = { a: currentValue };
                result = await calculate(operation, params);
                break;
            
            // Exponential
            case 'exp':
            case 'exp2':
            case 'exp10':
                params = { a: currentValue };
                result = await calculate(operation, params);
                break;
            
            // Power and roots
            case 'square':
            case 'cube':
            case 'sqrt':
            case 'cbrt':
            case 'abs':
            case 'floor':
            case 'ceil':
            case 'reciprocal':
            case 'negate':
            case 'percentage':
                params = { a: currentValue };
                result = await calculate(operation, params);
                break;
            
            case 'factorial':
                params = { n: currentValue };
                result = await calculate(operation, params);
                break;
            
            // Constants
            case 'pi':
            case 'e':
                result = await getConstant(operation);
                break;
            
            default:
                throw new Error(`Unknown operation: ${operation}`);
        }
        
        // Add to history for significant operations
        const displayOp = getUnaryOperationDisplay(operation);
        addToHistory(`${displayOp}(${formatNumber(currentValue)})`, result);
        
        state.currentValue = result.toString();
        state.waitingForSecondOperand = false;
        updateDisplay();
        
    } catch (error) {
        showError(error.message);
    } finally {
        display.classList.remove('calculating');
    }
}

/**
 * Get display name for unary operation.
 * @param {string} operation - The operation name
 * @returns {string} - Display name
 */
function getUnaryOperationDisplay(operation) {
    const names = {
        'sin': 'sin',
        'cos': 'cos',
        'tan': 'tan',
        'asin': 'sin⁻¹',
        'acos': 'cos⁻¹',
        'atan': 'tan⁻¹',
        'sinh': 'sinh',
        'cosh': 'cosh',
        'tanh': 'tanh',
        'log': 'ln',
        'log10': 'log',
        'log2': 'log₂',
        'exp': 'eˣ',
        'exp2': '2ˣ',
        'exp10': '10ˣ',
        'square': 'x²',
        'cube': 'x³',
        'sqrt': '√',
        'cbrt': '³√',
        'factorial': 'n!',
        'abs': '|x|',
        'reciprocal': '1/x',
        'negate': '±',
        'percentage': '%',
        'pi': 'π',
        'e': 'e'
    };
    return names[operation] || operation;
}

// ==================== Memory Functions ====================

/**
 * Clear memory.
 */
function memoryClear() {
    state.memory = 0;
    updateMemoryStatus();
}

/**
 * Recall memory value.
 */
function memoryRecall() {
    state.currentValue = state.memory.toString();
    state.waitingForSecondOperand = false;
    updateDisplay();
}

/**
 * Add current value to memory.
 */
function memoryAdd() {
    state.memory += parseFloat(state.currentValue);
    updateMemoryStatus();
}

/**
 * Subtract current value from memory.
 */
function memorySubtract() {
    state.memory -= parseFloat(state.currentValue);
    updateMemoryStatus();
}

/**
 * Store current value in memory.
 */
function memoryStore() {
    state.memory = parseFloat(state.currentValue);
    updateMemoryStatus();
}

/**
 * Update the memory status indicator.
 */
function updateMemoryStatus() {
    if (state.memory !== 0) {
        memoryStatus.textContent = `M: ${formatNumber(state.memory)}`;
    } else {
        memoryStatus.textContent = '';
    }
}

// ==================== History Functions ====================

/**
 * Add a calculation to history.
 * @param {string} expr - The expression
 * @param {number} result - The result
 */
function addToHistory(expr, result) {
    const item = {
        expression: expr,
        result: result,
        timestamp: new Date()
    };
    
    state.history.unshift(item);
    
    // Limit history to 50 items
    if (state.history.length > 50) {
        state.history.pop();
    }
    
    renderHistory();
    saveHistory();
}

/**
 * Render the history list.
 */
function renderHistory() {
    if (state.history.length === 0) {
        historyList.innerHTML = '<p class="no-history">No calculations yet</p>';
        return;
    }
    
    historyList.innerHTML = state.history.map((item, index) => `
        <div class="history-item" data-index="${index}">
            <div class="history-expression">${item.expression}</div>
            <div class="history-result">= ${formatNumber(item.result)}</div>
        </div>
    `).join('');
    
    // Add click handlers
    historyList.querySelectorAll('.history-item').forEach(el => {
        el.addEventListener('click', () => {
            const index = parseInt(el.dataset.index);
            state.currentValue = state.history[index].result.toString();
            updateDisplay();
        });
    });
}

/**
 * Clear calculation history.
 */
function clearHistory() {
    state.history = [];
    localStorage.removeItem('calculatorHistory');
    renderHistory();
}

/**
 * Save history to localStorage.
 */
function saveHistory() {
    try {
        localStorage.setItem('calculatorHistory', JSON.stringify(state.history));
    } catch (e) {
        console.warn('Could not save history to localStorage');
    }
}

/**
 * Load history from localStorage.
 */
function loadHistory() {
    try {
        const saved = localStorage.getItem('calculatorHistory');
        if (saved) {
            state.history = JSON.parse(saved);
            renderHistory();
        }
    } catch (e) {
        console.warn('Could not load history from localStorage');
    }
}

// ==================== Mode Toggle ====================

/**
 * Update degree/radian mode.
 */
function updateMode() {
    state.degreeMode = modeToggle.checked;
    modeIndicator.textContent = state.degreeMode ? 'Degrees' : 'Radians';
}

// ==================== Event Handlers ====================

/**
 * Handle button clicks.
 * @param {Event} event - The click event
 */
function handleButtonClick(event) {
    const button = event.target.closest('.btn');
    if (!button) return;
    
    const action = button.dataset.action;
    const value = button.dataset.value;
    
    // Handle number input
    if (value !== undefined) {
        if (value === '.') {
            inputDecimal();
        } else {
            inputDigit(value);
        }
        return;
    }
    
    // Handle actions
    switch (action) {
        // Clear operations
        case 'clear':
            clearAll();
            break;
        case 'clearEntry':
            clearEntry();
            break;
        case 'backspace':
            backspace();
            break;
        
        // Binary operators
        case 'add':
        case 'subtract':
        case 'multiply':
        case 'divide':
        case 'modulo':
        case 'power':
        case 'permutation':
        case 'combination':
            handleBinaryOperator(action);
            break;
        
        // Equals
        case 'equals':
            handleEquals();
            break;
        
        // Unary operations
        case 'sin':
        case 'cos':
        case 'tan':
        case 'asin':
        case 'acos':
        case 'atan':
        case 'sinh':
        case 'cosh':
        case 'tanh':
        case 'log':
        case 'log10':
        case 'log2':
        case 'exp':
        case 'exp2':
        case 'exp10':
        case 'square':
        case 'cube':
        case 'sqrt':
        case 'cbrt':
        case 'factorial':
        case 'abs':
        case 'floor':
        case 'ceil':
        case 'reciprocal':
        case 'percentage':
        case 'pi':
        case 'e':
            handleUnaryOperation(action);
            break;
        
        case 'negate':
            handleUnaryOperation('negate');
            break;
        
        // Memory operations
        case 'memoryClear':
            memoryClear();
            break;
        case 'memoryRecall':
            memoryRecall();
            break;
        case 'memoryAdd':
            memoryAdd();
            break;
        case 'memorySubtract':
            memorySubtract();
            break;
        case 'memoryStore':
            memoryStore();
            break;
    }
}

/**
 * Handle keyboard input.
 * @param {KeyboardEvent} event - The keyboard event
 */
function handleKeyboard(event) {
    const key = event.key;
    
    // Prevent default for calculator keys
    if (/^[0-9.]$/.test(key) || ['+', '-', '*', '/', 'Enter', 'Escape', 'Backspace'].includes(key)) {
        event.preventDefault();
    }
    
    // Numbers and decimal
    if (/^[0-9]$/.test(key)) {
        inputDigit(key);
        return;
    }
    
    if (key === '.') {
        inputDecimal();
        return;
    }
    
    // Operators
    switch (key) {
        case '+':
            handleBinaryOperator('add');
            break;
        case '-':
            handleBinaryOperator('subtract');
            break;
        case '*':
            handleBinaryOperator('multiply');
            break;
        case '/':
            handleBinaryOperator('divide');
            break;
        case '^':
            handleBinaryOperator('power');
            break;
        case '%':
            handleBinaryOperator('modulo');
            break;
        case 'Enter':
        case '=':
            handleEquals();
            break;
        case 'Escape':
            clearAll();
            break;
        case 'Backspace':
            backspace();
            break;
        case 'Delete':
            clearEntry();
            break;
    }
}

// ==================== Initialization ====================

/**
 * Initialize the calculator application.
 */
function init() {
    // Set up event listeners
    document.querySelector('.calculator').addEventListener('click', handleButtonClick);
    document.addEventListener('keydown', handleKeyboard);
    modeToggle.addEventListener('change', updateMode);
    clearHistoryBtn.addEventListener('click', clearHistory);
    
    // Initialize display
    updateDisplay();
    updateMode();
    updateMemoryStatus();
    loadHistory();
    
    // Check server status
    checkServerStatus();
    
    // Periodically check server status
    setInterval(checkServerStatus, 10000);
}

// Start the application when DOM is ready
document.addEventListener('DOMContentLoaded', init);
