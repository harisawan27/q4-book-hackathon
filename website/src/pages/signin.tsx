import React from 'react';
import Layout from '@theme/Layout';
import { SignIn } from '../components/SignIn';
import { useHistory } from '@docusaurus/router';

export default function SignInPage() {
  const history = useHistory();

  const handleSuccess = () => {
    history.push('/');
  };

  const handleSignUpClick = () => {
    history.push('/signup');
  };

  return (
    <Layout
      title="Sign In"
      description="Sign in to access personalized content and translation features"
    >
      <main className="container margin-vert--xl">
        <SignIn onSuccess={handleSuccess} onSignUpClick={handleSignUpClick} />
      </main>
    </Layout>
  );
}
