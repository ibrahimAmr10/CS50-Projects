# Web-Based Calculator with History Functionality

#### Video Demo : https://youtu.be/kXkhilTh3rQ?si=G-K6lUH6oyvk8u0n
## Project Overview

This project is a fully functional web-based calculator application built using Flask, a lightweight Python web framework. The calculator provides a clean, intuitive user interface that mimics the appearance and functionality of a physical calculator while leveraging the power of web technologies to store calculation history in a persistent database. The application demonstrates the seamless integration of frontend and backend technologies to create an interactive, data-driven user experience.

## Purpose and Motivation

The primary purpose of this calculator application is to provide users with a convenient tool for performing basic arithmetic operations while maintaining a complete history of all calculations. Unlike traditional calculators that lose data when cleared or powered off, this web-based solution stores every calculation in a SQLite database, allowing users to review their past operations at any time. This feature is particularly valuable for users who need to track their calculations for accounting, budgeting, education, or personal record-keeping purposes.

The project also serves as an excellent demonstration of modern web development practices, showcasing how different technologies work together to create a cohesive application. It illustrates the MVC (Model-View-Controller) pattern through Flask's routing system, template rendering, and database interactions.

## Key Features

### Basic Calculator Functionality
The calculator supports all fundamental arithmetic operations including addition (+), subtraction (-), multiplication (*), division (/), and modulo (%). Users can input numbers using on-screen buttons that respond to both mouse clicks and keyboard input, providing flexibility in how they interact with the application. The display updates dynamically as users input numbers and operators, providing immediate visual feedback.

### Persistent History Storage
Every calculation performed is automatically saved to a SQLite database with complete details including both operands, the operator used, the result, and a timestamp. This creates a permanent record that users can access whenever needed. The history feature transforms the calculator from a simple computational tool into a comprehensive calculation log.

### Modern User Interface
The calculator features a visually appealing design with a gradient background, smooth animations, and intuitive button layouts. The interface closely resembles a physical calculator with distinct visual styles for number buttons, operator buttons, and special functions. The color scheme uses a dark theme for the calculator body with highlighted operator buttons in purple, the clear button in red, and the equals button in green, providing clear visual cues for different button types.

### Responsive Design
The application is fully responsive and works seamlessly across different device sizes, from desktop computers to mobile phones. The CSS includes media queries that adjust button sizes, font sizes, and spacing to ensure optimal usability on smaller screens.

## Technical Architecture

### Backend Structure
The backend is built with Flask, which handles routing, request processing, and database operations. The application defines several routes:

- **Root Route (/)**: Serves the main calculator interface
- **History Route (/history)**: Displays all past calculations in reverse chronological order
- **Calculate Route (/calculate)**: Processes POST requests containing calculation data, performs the operation, saves it to the database, and returns the result
- **Clear History Route (/clear-history)**: Allows users to delete all calculation history

The Flask application initializes the SQLite database on startup, ensuring the calculations table exists before any operations are performed. All database operations use proper connection handling and commit transactions to ensure data integrity.

### Frontend Implementation
The frontend consists of HTML templates styled with CSS and enhanced with JavaScript for interactivity. The calculator interface uses a grid layout for button placement, ensuring consistent spacing and alignment. JavaScript handles all user interactions, maintaining application state for multi-step calculations and communicating with the backend via asynchronous fetch requests.

The JavaScript implementation includes sophisticated state management, tracking the current input, first operand, selected operator, and whether the calculator is waiting for a second operand. This state machine approach ensures the calculator behaves correctly even with complex input sequences.

### Database Design
The SQLite database uses a simple but effective schema with a single table named "calculations". Each record contains an auto-incrementing ID, the two operands as real numbers, the operator as text, the calculated result, and an automatically generated timestamp. This design allows for efficient storage and retrieval of calculation history while maintaining data integrity through the use of NOT NULL constraints.

## File Structure and Organization

The project follows Flask's conventional directory structure with clear separation between templates, static assets, and application logic. Templates are stored in the "templates" folder and are rendered using Jinja2, Flask's templating engine. Static files including CSS and JavaScript are kept in the "static" folder and served efficiently by Flask. This organization makes the project easy to understand, maintain, and extend.

## How to Use the Calculator

### Installation and Setup
To run the calculator, ensure Python 3 and Flask are installed on your system. Install Flask using pip if needed: `pip install flask`. Navigate to the project directory and run the application with `python app.py`. The Flask development server will start, typically on http://127.0.0.1:5000/, which you can access in any web browser.

### Performing Calculations
Click number buttons to input values, then click an operator button (+, -, *, /, %). Input the second number and press the equals button (=) to see the result. The calculator supports decimal numbers through the decimal point button. The clear button (C) resets the calculator to its initial state. Keyboard input is also fully supported: number keys for digits, operator keys for operations, Enter or = for calculation, and Escape or C for clearing.

### Viewing History
Click the "View History" link in the calculator header to navigate to the history page. This page displays all calculations in a scrollable list, with the most recent at the top. Each history item shows the complete calculation (operand, operator, operand, result) along with the timestamp. The history page includes a "Clear History" button that, when clicked, deletes all records from the database after confirmation.

## Design Decisions

### Color Scheme and Visual Design
The purple gradient background was chosen to create a modern, professional appearance while providing good contrast with the dark calculator interface. The button color coding (purple for operators, red for clear, green for equals) follows common design patterns that users intuitively understand. Shadows and hover effects add depth and provide visual feedback, making the interface feel responsive and polished.

### Database Choice
SQLite was selected for data storage due to its simplicity, zero-configuration setup, and perfect suitability for single-user applications. It requires no separate database server and stores all data in a single file, making the application portable and easy to deploy. For this use case, SQLite's performance characteristics are more than adequate.

### Error Handling
The application includes robust error handling for edge cases such as division by zero. When errors occur, user-friendly messages are displayed rather than technical error codes. The backend validates all input and returns appropriate HTTP status codes and error messages for invalid requests.

## Extensibility and Future Enhancements

The modular design of this application makes it easy to extend with additional features. Potential enhancements could include: support for more advanced mathematical functions (square root, exponents, trigonometric functions), user accounts with separate calculation histories, export functionality to download history as CSV or PDF, calculation notes or tags for organization, and data visualization showing calculation patterns over time.

## Conclusion

This web calculator project successfully demonstrates the integration of Flask, JavaScript, and SQLite to create a practical, user-friendly application. It combines clean design, robust functionality, and persistent data storage in a package that is both useful as a tool and educational as a code example. The project serves as an excellent starting point for developers learning web development or looking for a template to build upon for more complex calculator applications.
