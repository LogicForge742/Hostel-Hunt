# Hostel-Hunt

## Overview

Hostel-Hunt is a full-stack web application designed for searching and booking hostels. The project is structured as a monorepo with separate directories for the backend and frontend components. The backend is built with Flask (Python), providing RESTful APIs for data management, while the frontend is a modern React application with JavaScript, offering a responsive user interface for hostel discovery and booking.
 The application aims to provide a seamless experience for users looking to find and reserve accommodations, with a focus on hostels.
 

## Tech Stack

### Backend (Hostel-Backend)
- **Framework**: Flask (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Database Driver**: psycopg2
- **Migration Tool**: Alembic
- **Purpose**: RESTful API server for handling business logic, database interactions, and authentication

### Frontend (Hostel-Frontend)
- **Framework**: React 19 with JavaScript
- **Build Tool**: Vite
- **Styling**: CSS (with potential for CSS-in-JS or styled-components in future iterations)
- **Linting**: ESLint with React-specific rules
- **Purpose**: Client-side application for user interactions, hostel listings, and booking flows

## Project Structure

```
Hostel-Hunt/
├── LICENSE
├── README.md (this file)
├── Hostel-Backend/          # Flask backend application
│   └── (currently empty - planned structure below)
│       ├── app/
│       │   ├── __init__.py
│       │   ├── models/      # Database models
│       │   ├── routes/      # API endpoints
│       │   ├── services/    # Business logic
│       │   └── utils/       # Helper functions
│       ├── config.py        # Configuration settings
│       ├── requirements.txt # Python dependencies
│       └── run.py           # Application entry point
└── Hostel-Frontend/         # React frontend application
    ├── public/              # Static assets
    │   └── vite.svg
    ├── src/
    │   ├── assets/          # Imported assets (images, icons)
    │   │   └── react.svg
    │   ├── App.css          # Main app styles
    │   ├── App.jsx          # Root React component
    │   ├── index.css        # Global styles
    │   ├── main.jsx         # React app entry point
    │   └── (future components, pages, hooks, etc.)
    ├── .gitignore           # Git ignore rules
    ├── eslint.config.js     # ESLint configuration
    ├── index.html           # Main HTML template
    ├── package.json         # Node.js dependencies and scripts
    ├── package-lock.json    # Lockfile for exact dependency versions
    ├── README.md            # Frontend-specific documentation
    └── vite.config.js       # Vite build configuration
```

## Backend Structure (Planned)

The backend will follow Flask best practices:
- **Blueprints**: For modular route organization
- **SQLAlchemy**: For ORM and database interactions
- **Flask-JWT-Extended**: For authentication
- **Flask-CORS**: For cross-origin requests
- **Environment-based configuration**: For different deployment stages

## Frontend Structure

The frontend is set up with Vite for fast development and optimized builds:
- **Component-based architecture**: Using React functional components with hooks
- **TypeScript**: For type safety and better developer experience
- **Modular CSS**: Separate stylesheets for components and global styles
- **Asset management**: Organized assets in the `src/assets` directory

## Setup Instructions

### Prerequisites
- Python 3.8+ (for backend)
- Node.js 18+ and npm (for frontend)
- Git

### Backend Setup (Hostel-Backend)
1. Navigate to the backend directory:
   ```bash
   cd Hostel-Backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables (create a `.env` file based on `config.py`)
5. Run the application:
   ```bash
   python run.py
   ```

### Frontend Setup (Hostel-Frontend)
1. Navigate to the frontend directory:
   ```bash
   cd Hostel-Frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Build for production:
   ```bash
   npm run build
   ```
5. Preview the production build:
   ```bash
   npm run preview
   ```

## Development Workflow

1. **Backend Development**:
   - Implement API endpoints in Flask
   - Use Postman or similar for API testing
   - Follow RESTful conventions

2. **Frontend Development**:
   - Develop components in React with TypeScript
   - Use Vite's hot module replacement for fast development
   - Run linting with `npm run lint`

3. **Integration**:
   - Ensure frontend API calls match backend endpoints
   - Implement proper error handling and loading states

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a pull request

## License

This project is licensed under the terms specified in the LICENSE file.

## Contact

For questions or contributions, please open an issue in the repository.
