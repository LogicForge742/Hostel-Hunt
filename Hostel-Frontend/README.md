# Hostel Hunt Frontend

A modern React application for finding and booking hostels, built with Vite, Tailwind CSS v4, and React Router.

## Features

- **Modern React Setup**: Uses React 19 with Vite for fast development and building
- **Tailwind CSS v4**: Latest version of Tailwind CSS for utility-first styling
- **Responsive Design**: Mobile-first approach with responsive components
- **Component Library**: Reusable UI components (Button, Card, Modal, etc.)
- **Authentication**: Login and signup pages with context-based auth management
- **Booking System**: Complete booking flow with confirmation pages
- **Search Functionality**: Advanced search with filters and results
- **Dashboard**: User dashboard with booking history and favorites
- **Error Handling**: Error boundaries and loading states

## Tech Stack

- **Frontend Framework**: React 19
- **Build Tool**: Vite
- **Styling**: Tailwind CSS v4
- **Routing**: React Router DOM v6
- **State Management**: React Context API
- **HTTP Client**: TanStack Query (React Query)
- **Animations**: Framer Motion
- **Linting**: ESLint with React plugins
- **Code Quality**: Stylelint for CSS

## Getting Started

### Prerequisites

- Node.js (version 18 or higher)
- npm or yarn

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
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

4. In a separate terminal, start Tailwind CSS compilation:
   ```bash
   npx tailwindcss -i ./src/index.css -o ./src/output.css --watch
   ```

5. Open [http://localhost:5173](http://localhost:5173) in your browser.

### Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the project for production
- `npm run preview` - Preview the production build locally
- `npm run lint` - Run ESLint for code quality checks

## Project Structure

```
src/
├── components/          # Reusable UI components
├── contexts/           # React contexts for state management
├── hooks/              # Custom React hooks
├── pages/              # Page components organized by feature
├── routes/             # Routing configuration
├── utils/              # Utility functions and helpers
├── assets/             # Static assets
├── App.jsx             # Main app component
├── main.jsx            # Application entry point
└── index.css           # Global styles (Tailwind imports)
```

## Tailwind CSS v4 Setup

This project uses Tailwind CSS v4, which has a different setup process compared to v3:

- CSS is compiled from `src/index.css` to `src/output.css`
- The compiled CSS is imported in `main.jsx`
- PostCSS configuration is handled via `postcss.config.js`

## Contributing

1. Follow the existing code style and structure
2. Run linting before committing: `npm run lint`
3. Test your changes thoroughly
4. Update documentation as needed

## License

This project is licensed under the MIT License.
