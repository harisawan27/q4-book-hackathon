import React from 'react';
import { useAuth } from '../AuthProvider';

interface NavbarAuthProps {
  mobile?: boolean;
}

export function NavbarAuth({ mobile = false }: NavbarAuthProps) {
  const { user, isAuthenticated, isLoading, signOut } = useAuth();

  if (isLoading) {
    if (mobile) {
      return <div className="navbar-auth-mobile"><span>Loading...</span></div>;
    }
    return <span className="navbar__item">Loading...</span>;
  }

  if (isAuthenticated && user) {
    if (mobile) {
      return (
        <div className="navbar-auth-mobile">
          <a className="menu__link" href="/profile">
            Profile ({user.name || user.email.split('@')[0]})
          </a>
          <button
            className="menu__link"
            onClick={() => signOut()}
            style={{ background: 'none', border: 'none', width: '100%', textAlign: 'left', cursor: 'pointer', padding: '10px 16px' }}
          >
            Sign Out
          </button>
        </div>
      );
    }
    return (
      <div className="navbar__item dropdown dropdown--hoverable dropdown--right navbar-auth-desktop">
        <button className="navbar__link" style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
          {user.name || user.email.split('@')[0]}
        </button>
        <ul className="dropdown__menu">
          <li>
            <a className="dropdown__link" href="/profile">
              Profile
            </a>
          </li>
          <li>
            <button
              className="dropdown__link"
              onClick={() => signOut()}
              style={{ background: 'none', border: 'none', width: '100%', textAlign: 'left', cursor: 'pointer' }}
            >
              Sign Out
            </button>
          </li>
        </ul>
      </div>
    );
  }

  if (mobile) {
    return (
      <div className="navbar-auth-mobile">
        <a className="menu__link" href="/signin">
          Sign In
        </a>
        <a className="menu__link menu__link--signup" href="/signup">
          Sign Up
        </a>
      </div>
    );
  }

  return (
    <>
      <a className="navbar__item navbar__link navbar-auth-desktop" href="/signin">
        Sign In
      </a>
      <a className="navbar__item navbar__link button button--primary button--md navbar-auth-desktop" href="/signup" style={{ marginLeft: 8, marginRight: 8 }}>
        Sign Up
      </a>
    </>
  );
}

export default NavbarAuth;
