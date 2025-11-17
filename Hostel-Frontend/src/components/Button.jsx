import { forwardRef } from 'react';

const Button = forwardRef(({
  variant = 'primary',
  size = 'medium',
  disabled = false,
  className = '',
  children,
  ...props
}, ref) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none';

  const variantClasses = {
    primary: 'bg-button-primary-bg text-button-primary-text hover:bg-hover focus:ring-primary',
    secondary: 'bg-button-secondary-bg text-button-secondary-text hover:bg-gray-800 focus:ring-primary',
    ghost: 'bg-transparent text-text-body hover:bg-hover focus:ring-primary'
  };

  const sizeClasses = {
    small: 'px-3 py-1.5 text-sm',
    medium: 'px-4 py-2',
    large: 'px-6 py-3'
  };

  const classes = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`;

  return (
    <button
      ref={ref}
      className={classes}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
});

Button.displayName = 'Button';

export default Button;
