import React, { useState } from 'react';
import { useAuth } from '../AuthProvider';
import { BackgroundForm } from '../BackgroundForm';
import { UserBackground } from '../../lib/auth';

interface SignUpProps {
  onSuccess?: () => void;
  onSignInClick?: () => void;
}

const defaultBackground: UserBackground = {
  software_skills: 'none',
  hardware_skills: 'none',
  experience_level: 'student',
};

export function SignUp({ onSuccess, onSignInClick }: SignUpProps) {
  const { signUp, isLoading } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [name, setName] = useState('');
  const [background, setBackground] = useState<UserBackground>(defaultBackground);
  const [includeBackground, setIncludeBackground] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Validation
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    try {
      await signUp(
        email,
        password,
        name || undefined,
        includeBackground ? background : undefined
      );
      onSuccess?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Signup failed');
    }
  };

  return (
    <div className="card padding--lg" style={{ maxWidth: 500, margin: '0 auto' }}>
      <h2>Create Account</h2>
      <p className="text--secondary">
        Sign up to personalize your learning experience.
      </p>

      {error && (
        <div className="alert alert--danger margin-bottom--md" role="alert">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="margin-bottom--md">
          <label htmlFor="email" className="form-label">
            Email *
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
          <label htmlFor="name" className="form-label">
            Name (optional)
          </label>
          <input
            id="name"
            type="text"
            className="form-input"
            value={name}
            onChange={(e) => setName(e.target.value)}
            disabled={isLoading}
            placeholder="Your name"
          />
        </div>

        <div className="margin-bottom--md">
          <label htmlFor="password" className="form-label">
            Password *
          </label>
          <input
            id="password"
            type="password"
            className="form-input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
            disabled={isLoading}
            placeholder="At least 8 characters"
          />
        </div>

        <div className="margin-bottom--md">
          <label htmlFor="confirmPassword" className="form-label">
            Confirm Password *
          </label>
          <input
            id="confirmPassword"
            type="password"
            className="form-input"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            disabled={isLoading}
            placeholder="Confirm your password"
          />
        </div>

        <hr className="margin-vert--md" />

        <div className="margin-bottom--md">
          <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer' }}>
            <input
              type="checkbox"
              checked={includeBackground}
              onChange={(e) => setIncludeBackground(e.target.checked)}
              disabled={isLoading}
              style={{ width: 18, height: 18 }}
            />
            <span>Complete background questionnaire (recommended)</span>
          </label>
          <span className="form-helper">
            This helps us personalize chapter content to your experience level.
          </span>
        </div>

        {includeBackground && (
          <div className="margin-bottom--md">
            <BackgroundForm
              value={background}
              onChange={setBackground}
              disabled={isLoading}
            />
          </div>
        )}

        <button
          type="submit"
          className="button button--primary button--lg button--block"
          disabled={isLoading}
        >
          {isLoading ? 'Creating Account...' : 'Create Account'}
        </button>

        <p className="text--center margin-top--md">
          Already have an account?{' '}
          <a href="#" onClick={(e) => { e.preventDefault(); onSignInClick?.(); }}>
            Sign in
          </a>
        </p>
      </form>
    </div>
  );
}

export default SignUp;
