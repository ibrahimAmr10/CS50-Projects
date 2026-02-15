let currentInput = '0';
let firstOperand = null;
let operator = null;
let waitingForSecondOperand = false;

const display = document.getElementById('display');

function updateDisplay() {
    display.textContent = currentInput;
}

function inputNumber(num) {
    if (waitingForSecondOperand) {
        currentInput = num;
        waitingForSecondOperand = false;
    } else {
        currentInput = currentInput === '0' ? num : currentInput + num;
    }
    updateDisplay();
}

function inputDecimal() {
    if (waitingForSecondOperand) {
        currentInput = '0.';
        waitingForSecondOperand = false;
        updateDisplay();
        return;
    }
    
    if (!currentInput.includes('.')) {
        currentInput += '.';
        updateDisplay();
    }
}

function inputOperator(nextOperator) {
    const inputValue = parseFloat(currentInput);
    
    if (firstOperand === null && !isNaN(inputValue)) {
        firstOperand = inputValue;
    } else if (operator) {
        const result = performCalculation();
        if (result !== null) {
            currentInput = String(result);
            firstOperand = result;
        }
    }
    
    waitingForSecondOperand = true;
    operator = nextOperator;
    updateDisplay();
}

function performCalculation() {
    const inputValue = parseFloat(currentInput);
    
    if (isNaN(inputValue) || firstOperand === null || operator === null) {
        return null;
    }
    
    let result;
    
    switch (operator) {
        case '+':
            result = firstOperand + inputValue;
            break;
        case '-':
            result = firstOperand - inputValue;
            break;
        case '*':
            result = firstOperand * inputValue;
            break;
        case '/':
            if (inputValue === 0) {
                alert('Cannot divide by zero');
                clearDisplay();
                return null;
            }
            result = firstOperand / inputValue;
            break;
        case '%':
            result = firstOperand % inputValue;
            break;
        default:
            return null;
    }
    
    // Round to avoid floating point errors
    result = Math.round(result * 100000000) / 100000000;
    
    return result;
}

function calculate() {
    const inputValue = parseFloat(currentInput);
    
    if (firstOperand === null || operator === null || isNaN(inputValue)) {
        return;
    }
    
    // Send calculation to server
    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            number1: firstOperand,
            number2: inputValue,
            operator: operator
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            clearDisplay();
        } else {
            currentInput = String(data.result);
            firstOperand = data.result;
            operator = null;
            waitingForSecondOperand = true;
            updateDisplay();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error performing calculation');
    });
}

function clearDisplay() {
    currentInput = '0';
    firstOperand = null;
    operator = null;
    waitingForSecondOperand = false;
    updateDisplay();
}

// Keyboard support
document.addEventListener('keydown', function(event) {
    const key = event.key;
    
    // Numbers
    if (key >= '0' && key <= '9') {
        inputNumber(key);
    }
    
    // Operators
    if (key === '+' || key === '-' || key === '*' || key === '/' || key === '%') {
        inputOperator(key);
    }
    
    // Decimal point
    if (key === '.') {
        inputDecimal();
    }
    
    // Enter or equals
    if (key === 'Enter' || key === '=') {
        event.preventDefault();
        calculate();
    }
    
    // Clear
    if (key === 'Escape' || key === 'c' || key === 'C') {
        clearDisplay();
    }
    
    // Backspace
    if (key === 'Backspace') {
        event.preventDefault();
        if (currentInput.length > 1) {
            currentInput = currentInput.slice(0, -1);
        } else {
            currentInput = '0';
        }
        updateDisplay();
    }
});

// Initialize display
updateDisplay();
