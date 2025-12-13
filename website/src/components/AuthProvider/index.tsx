import React, { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import {
  User,
  UserBackgroundResponse,
  getSession,
  signIn as apiSignIn,
  signUp as apiSignUp,
  signOut as apiSignOut,
  UserBackground,
  clearToken,
} from '../../lib/auth';

interface AuthContextType {
  user: User | null;
  hasBackground: boolean;
  isLoading: boolean;
  isAuthenticated: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string, name?: string, background?: UserBackground) => Promise<void>;
  signOut: () => Promise<void>;
  refreshSession: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [hasBackground, setHasBackground] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const refreshSession = useCallback(async () => {
    try {
      const session = await getSession();
      if (session) {
        setUser(session.user);
        setHasBackground(session.has_background);
      } else {
        setUser(null);
        setHasBackground(false);
      }
    } catch (error) {
      console.error('Failed to refresh session:', error);
      setUser(null);
      setHasBackground(false);
      clearToken();
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    refreshSession();
  }, [refreshSession]);

  const signIn = useCallback(async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const response = await apiSignIn(email, password);
      setUser(response.user);
      // Refresh to get has_background status
      await refreshSession();
    } finally {
      setIsLoading(false);
    }
  }, [refreshSession]);

  const signUp = useCallback(async (
    email: string,
    password: string,
    name?: string,
    background?: UserBackground
  ) => {
    setIsLoading(true);
    try {
      const response = await apiSignUp(email, password, name, background);
      setUser(response.user);
      setHasBackground(!!background);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const signOut = useCallback(async () => {
    setIsLoading(true);
    try {
      await apiSignOut();
    } finally {
      setUser(null);
      setHasBackground(false);
      setIsLoading(false);
    }
  }, []);

  const value: AuthContextType = {
    user,
    hasBackground,
    isLoading,
    isAuthenticated: !!user,
    signIn,
    signUp,
    signOut,
    refreshSession,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export default AuthProvider;
