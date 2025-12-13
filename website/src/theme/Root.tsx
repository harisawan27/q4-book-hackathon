import React from 'react';
import { AuthProvider } from '../components/AuthProvider';

interface RootProps {
  children: React.ReactNode;
}

// This is the Root component that wraps the entire Docusaurus app.
// It provides the AuthProvider context to all components.
export default function Root({ children }: RootProps) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}
