import React, { useState } from 'react';
import { useAuth } from '../AuthProvider';

interface SignInProps {
  onSuccess?: () => void;
  onSignUpClick?: () => void;
}

export function SignIn({ onSuccess, onSignUpClick }: SignInProps) {
  const { signIn, isLoading } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      await signIn(email, password);
      onSuccess?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Sign in failed');
    }
  };

  return (
    <div className="card padding--lg" style={{ maxWidth: 400, margin: '0 auto' }}>
      <h2>Sign In</h2>
      <p className="text--secondary">
        Sign in to access personalized content and translation features.
      </p>

      {error && (
        <div className="alert alert--danger margin-bottom--md" role="alert">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="margin-bottom--md">
          <label htmlFor="email" className="form-label">
            Email
          </label>
          <input
            id="email"
            type="email"
            className="form-input"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={isLoading}
            placeholder="you@example.com"
          />
        </div>

        <div className="margin-bottom--md">
          <label htmlFor="password" className="form-label">
            Password
          </label>
          <input
            id="password"
            type="password"
            className="form-input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={isLoading}
            placeholder="Your password"
          />
        </div>

        <button
          type="submit"
          className="button button--primary button--lg button--block"
          disabled={isLoading}
        >
          {isLoading ? 'Signing in...' : 'Sign In'}
        </button>

        <p className="text--center margin-top--md">
          Don't have an account?{' '}
          <a href="#" onClick={(e) => { e.preventDefault(); onSignUpClick?.(); }}>
            Create one
          </a>
        </p>
      </form>
    </div>
  );
}

export default SignIn;
