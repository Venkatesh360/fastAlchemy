# fastAlchemy

A practice repository demonstrating a full-stack web application using FastAPI, SQLAlchemy, and a modern frontend stack.

## Overview

This project showcases a web application built with:

- **Backend**: FastAPI with SQLAlchemy for database interactions.  
- **Frontend**: Modern JavaScript framework (React).  
- **Database**: SQLite.

## Project Structure

```
fastAlchemy/
├── fast_backend/
│   └── app/
│       ├── main.py
│       ├── models.py
│       ├── schemas.py
│       └── database.py
├────requirements.txt
│
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       ├── App.vue
│       └── main.ts
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js and npm
- PostgreSQL (or SQLite)

### Backend Setup

Navigate to the backend directory:

```bash
cd fast_backend
```

Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Configure the database settings in `database.py`.

Run the FastAPI application:

```bash
uvicorn app.main:app --reload
```

### Frontend Setup

Navigate to the frontend directory:

```bash
cd frontend
```

Install the dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

## Features

- User authentication and authorization  
- CRUD operations for various models  
- Responsive UI with modern design  
- RESTful API endpoints  

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.
