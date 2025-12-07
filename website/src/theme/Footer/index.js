import React from 'react';
import Footer from '@theme-original/Footer';
import BrowserOnly from '@docusaurus/BrowserOnly';
import ChatWidget from '@site/src/components/ChatWidget';

export default function FooterWrapper(props) {
  return (
    <>
      <Footer {...props} />
      <BrowserOnly>
        {() => <ChatWidget />}
      </BrowserOnly>
    </>
  );
}
