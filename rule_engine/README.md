# Rule Engine Application

## Overview
This application implements a rule engine using an Abstract Syntax Tree (AST) to evaluate user eligibility based on various attributes.

## Installation
1. Clone the repository.
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   
## Non-Functional Considerations
- **Security**: Input validation is enforced to prevent injection attacks and provide robust error handling for invalid rule syntax.
- **Performance**: The AST structure allows efficient evaluation of rules, minimizing redundant checks and memory usage.
- **Usability**: User documentation is provided, along with user-friendly error messages.
- **Scalability**: The modular design facilitates easy addition of new rule types, with potential for database integration for persistent rule storage.
