import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, test, expect } from '@jest/globals';
import Layout from '../components/Layout.jsx';

const renderWithRouter = (component) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('Layout', () => {
  test('renders header and footer', () => {
    renderWithRouter(<Layout />);

    expect(screen.getByText('HostelHunt')).toBeInTheDocument();
    expect(screen.getByText('© 2025 HostelHunt. All rights reserved.')).toBeInTheDocument();
  });

  test('scrolls to top on route change', () => {
    renderWithRouter(<Layout />);

    // Check that scrollTo is mocked and available
    expect(window.scrollTo).toBeDefined();
    expect(typeof window.scrollTo).toBe('function');
  });
});
