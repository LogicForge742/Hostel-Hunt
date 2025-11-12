import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Header from '../components/Header';

test('mobile menu toggles', () => {
  render(
    <MemoryRouter>
      <Header />
    </MemoryRouter>
  );

  fireEvent.click(screen.getByText('Menu'));
  expect(screen.getByText('Home')).toBeInTheDocument();

  fireEvent.click(screen.getByText('Close'));
  expect(screen.queryByText('Home')).not.toBeInTheDocument();
});