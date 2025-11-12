import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Layout from '../components/Layout';

test('renders children', () => {
  render(
    <MemoryRouter>
      <Layout>
        <div data-testid="child">Test</div>
      </Layout>
    </MemoryRouter>
  );

  expect(screen.getByTestId('child')).toBeInTheDocument();
});