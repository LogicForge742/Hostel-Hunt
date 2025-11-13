import { BrowserRouter } from 'react-router-dom';
import ErrorBoundary from './components/ErrorBoundary';
import { AuthProvider } from './contexts/AuthContext.jsx';
import { BookingProvider } from './contexts/BookingContext.jsx';
import AppRouter from './routes/AppRouter.jsx';

export default function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <BookingProvider>
          <BrowserRouter>
            <AppRouter />
          </BrowserRouter>
        </BookingProvider>
      </AuthProvider>
    </ErrorBoundary>
  );
}
