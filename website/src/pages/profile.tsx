import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../components/AuthProvider';
import { BackgroundForm } from '../components/BackgroundForm';
import { UserBackground, updateBackground, getBackground } from '../lib/auth';
import { useHistory } from '@docusaurus/router';

export default function ProfilePage() {
  const { user, hasBackground, isAuthenticated, isLoading, refreshSession } = useAuth();
  const history = useHistory();
  const [background, setBackground] = useState<UserBackground | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [isLoadingBackground, setIsLoadingBackground] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      history.push('/signin');
    }
  }, [isLoading, isAuthenticated, history]);

  // Fetch background when user is authenticated
  useEffect(() => {
    async function fetchBackground() {
      if (isAuthenticated && hasBackground) {
        setIsLoadingBackground(true);
        try {
          const bg = await getBackground();
          setBackground(bg);
        } catch (err) {
          console.error('Failed to fetch background:', err);
        } finally {
          setIsLoadingBackground(false);
        }
      }
    }
    fetchBackground();
  }, [isAuthenticated, hasBackground]);

  const handleBackgroundChange = (newBackground: UserBackground) => {
    setBackground(newBackground);
  };

  const handleSave = async () => {
    if (!background) return;

    setIsSaving(true);
    setMessage(null);

    try {
      await updateBackground(background);
      await refreshSession();
      setMessage({ type: 'success', text: 'Background updated successfully!' });
    } catch (err) {
      setMessage({
        type: 'error',
        text: err instanceof Error ? err.message : 'Failed to update background',
      });
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading || isLoadingBackground) {
    return (
      <Layout title="Profile" description="Manage your profile">
        <main className="container margin-vert--xl">
          <div className="text--center">Loading...</div>
        </main>
      </Layout>
    );
  }

  if (!isAuthenticated || !user) {
    return (
      <Layout title="Profile" description="Manage your profile">
        <main className="container margin-vert--xl">
          <div className="text--center">Redirecting to sign in...</div>
        </main>
      </Layout>
    );
  }

  return (
    <Layout title="Profile" description="Manage your profile and preferences">
      <main className="container margin-vert--xl">
        <div style={{ maxWidth: 600, margin: '0 auto' }}>
          <h1>Your Profile</h1>

          <div className="card padding--lg margin-bottom--lg">
            <h3>Account Information</h3>
            <p><strong>Email:</strong> {user.email}</p>
            {user.name && <p><strong>Name:</strong> {user.name}</p>}
            <p>
              <strong>Email Verified:</strong>{' '}
              <span className={user.email_verified ? 'badge badge--success' : 'badge badge--warning'}>
                {user.email_verified ? 'Yes' : 'No'}
              </span>
            </p>
          </div>

          <div className="card padding--lg">
            {message && (
              <div
                className={`alert margin-bottom--md ${message.type === 'success' ? 'alert--success' : 'alert--danger'}`}
                role="alert"
              >
                {message.text}
              </div>
            )}

            {background ? (
              <>
                <BackgroundForm
                  value={background}
                  onChange={handleBackgroundChange}
                  disabled={isSaving}
                />
                <button
                  className="button button--primary button--lg margin-top--md"
                  onClick={handleSave}
                  disabled={isSaving}
                >
                  {isSaving ? 'Saving...' : 'Save Changes'}
                </button>
              </>
            ) : (
              <>
                <h3>Complete Your Background</h3>
                <p className="text--secondary">
                  Add your background information to get personalized content recommendations.
                </p>
                <BackgroundForm
                  value={{
                    software_skills: 'none',
                    hardware_skills: 'none',
                    experience_level: 'student',
                  }}
                  onChange={handleBackgroundChange}
                  disabled={isSaving}
                />
                <button
                  className="button button--primary button--lg margin-top--md"
                  onClick={handleSave}
                  disabled={isSaving || !background}
                >
                  {isSaving ? 'Saving...' : 'Save Background'}
                </button>
              </>
            )}
          </div>
        </div>
      </main>
    </Layout>
  );
}
