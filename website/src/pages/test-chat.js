import React from 'react';
import Layout from '@theme/Layout';
import BrowserOnly from '@docusaurus/BrowserOnly';
import ChatWidget from '../components/ChatWidget';

export default function TestChat() {
  return (
    <Layout title="Chat Test" description="Testing the Chat Widget">
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '50vh',
          fontSize: '20px',
        }}>
        <p>Check the bottom right corner for the Chat Widget.</p>
        <BrowserOnly>
            {() => <ChatWidget />}
        </BrowserOnly>
      </div>
    </Layout>
  );
}
