import { Component } from 'react';

export default class ErrorBoundary extends Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center p-4">
          <div className="text-center bg-white dark:bg-gray-800 p-8 rounded shadow-lg max-w-md">
            <h1 className="text-2xl font-bold mb-2">Something went wrong</h1>
            <p className="mb-4">Please try refreshing.</p>
            <button
              onClick={() => window.location.reload()}
              className="px-6 py-2 bg-gray-200 dark:bg-gray-700 rounded hover:bg-gray-300 dark:hover:bg-gray-600"
            >
              Reload
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
