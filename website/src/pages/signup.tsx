import React from 'react';
import Layout from '@theme/Layout';
import { SignUp } from '../components/SignUp';
import { useHistory } from '@docusaurus/router';

export default function SignUpPage() {
  const history = useHistory();

  const handleSuccess = () => {
    history.push('/');
  };

  const handleSignInClick = () => {
    history.push('/signin');
  };

  return (
    <Layout
      title="Sign Up"
      description="Create an account to personalize your learning experience"
    >
      <main className="container margin-vert--xl">
        <SignUp onSuccess={handleSuccess} onSignInClick={handleSignInClick} />
      </main>
    </Layout>
  );
}
