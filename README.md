# ComfyBank-AI-Banking-multi-AI-Agent

## Overview

ComfyBank AI is a simulated banking application that combines a web interface, backend APIs, and a multi-agent system to demonstrate banking operations. It provides user authentication, account-related operations, transaction history, loan EMI calculations, and an AI banking assistant.

## Features

- User registration and login
- JWT-based authentication
- Account balance viewing
- Money transfer between accounts
- Transaction history
- Loan EMI calculation
- AI banking assistant
- Multi-agent request routing
- Security and authentication support

## Technology Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **Programming Language:** Python
- **HTTP Requests:** Requests
- **Authentication:** JWT and Passlib
- **Database:** SQLite (`banking.db`, based on the project filename)
- **AI Agent Architecture:** Supervisor, Banking, Loan, and Security Agents

## Project Structure

```text
banking-multi-Aiagent/
├── agents/
│   ├── __init__.py
│   ├── banking_ag.py
│   ├── loan_ag.py
│   ├── security_ag.py
│   └── supervisor_ag.py
│
├── backend/
│   ├── __init__.py
│   ├── auth.py
│   └── main.py
│
├── database/
│
├── frontend/
│   ├── assets/
│   └── app.py
│
├── tests/
├── .env
├── .gitignore
├── banking.db
└── README.md
```
## System Architecture
<img width="1536" height="1024" alt="ComfyBank AI System Architecture Diagram" src="https://github.com/user-attachments/assets/0611547d-7d88-48f6-a1c7-0256cd22df3f" />

## Architecture

The application follows a frontend–backend architecture supported by database operations and AI agents.

1. **Frontend:** Streamlit provides the interface for registration, login, dashboard, transfers, transaction history, and AI chat.
2. **Backend:** FastAPI exposes endpoints to process authentication and banking requests.
3. **Database:** The `banking.db` file is the project's database file. Database operations are handled through the database-related code.
4. **Supervisor Agent:** Receives supported requests and routes them to the appropriate agent.
5. **Banking Agent:** Handles supported account and banking-related requests.
6. **Loan Agent:** Handles loan-related requests and EMI calculations.
7. **Security Agent:** Supports the project's security-related workflow.

The backend returns the processed result to the frontend, where it is displayed to the user.

## Prerequisites

- Python 3.10 or a compatible version
- pip
- Git
- Visual Studio Code or another Python IDE

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd banking-multi-Aiagent
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

If not, install the dependencies listed in your actual project imports. Do not rely on this README as a complete dependency list until `requirements.txt` has been created and tested.

### 4. Configure environment variables

Create or update the `.env` file with the environment variables required by your application.

**Security:** Never upload real passwords, API keys, secret keys, or other credentials to GitHub. Keep `.env` out of version control.

## Running the Application

Open two terminals in the project root.

**Terminal 1 – Start the backend**

```bash
uvicorn backend.main:app --reload
```

The API is expected to run at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is usually available at:

```text
http://127.0.0.1:8000/docs
```

**Terminal 2 – Start the frontend**

```bash
streamlit run frontend/app.py
```

Open the local URL printed by Streamlit in your browser.

Ensure the frontend's API URL matches the backend address.

## Loan EMI Calculation

The loan EMI calculation uses:

- Principal loan amount
- Annual interest rate
- Loan tenure in months

The application calculates the estimated monthly EMI, total interest, and total repayment amount.

## Testing

The project contains a `tests/` directory for tests.

Run the tests with:

```bash
pytest
```

Ensure that the required testing dependencies are installed.

## Security and Limitations

- This is a simulated banking application intended for educational and demonstration purposes.
- Use fictional account details when demonstrating the application.
- Do not use real banking credentials or sensitive financial information.
- Test authentication, transfer validation, and error handling before presenting the application.

## Future Enhancements

- Improve loan eligibility analysis.
- Add automated tests for banking APIs and agent workflows.
- Improve input validation and error handling.
- Enhance audit logging and security.
- Deploy the application to a suitable hosting environment.

## Author

Developed as a project demonstrating web application development, banking API integration, and multi-agent automation.
