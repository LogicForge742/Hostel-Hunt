import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, test, expect } from '@jest/globals';
import Header from '../components/Header.jsx';

const renderWithRouter = (component) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('Header', () => {
  test('renders logo and navigation links', () => {
    renderWithRouter(<Header />);

    expect(screen.getByText('HostelHunt')).toBeInTheDocument();
    expect(screen.getAllByText('Home')).toHaveLength(2); // Desktop and mobile
    expect(screen.getAllByText('Explore')).toHaveLength(2); // Desktop and mobile
    expect(screen.getAllByText('Login')).toHaveLength(2); // Desktop and mobile
    expect(screen.getAllByText('Sign Up')).toHaveLength(2); // Desktop and mobile
  });

  test('toggles mobile menu on button click', () => {
    renderWithRouter(<Header />);

    const menuButton = screen.getByText('Menu');
    expect(menuButton).toBeInTheDocument();

    // Initially mobile menu should be hidden
    expect(screen.getByText('Menu')).toBeInTheDocument();

    // Click to open mobile menu
    fireEvent.click(menuButton);
    expect(screen.getByText('Close')).toBeInTheDocument();

    // Click to close mobile menu
    fireEvent.click(screen.getByText('Close'));
    expect(screen.getByText('Menu')).toBeInTheDocument();
  });

  test('logo links to home page', () => {
    renderWithRouter(<Header />);

    const logo = screen.getByText('HostelHunt');
    expect(logo.closest('a')).toHaveAttribute('href', '/');
  });
});
