import React, { useEffect, useRef, useState } from 'react';
import DocItem from '@theme-original/DocItem';
import type DocItemType from '@theme/DocItem';
import type { WrapperProps } from '@docusaurus/types';
import { useLocation } from '@docusaurus/router';
import { ChapterControls } from '../../components/ChapterControls';

type Props = WrapperProps<typeof DocItemType>;

export default function DocItemWrapper(props: Props) {
  const location = useLocation();
  const contentRef = useRef<HTMLDivElement>(null);
  const [docContent, setDocContent] = useState<string>('');
  const [contentKey, setContentKey] = useState<number>(0);

  // Extract chapter slug from URL path (remove leading /docs/)
  const chapterSlug = location.pathname.replace(/^\/docs\/?/, '').replace(/\/$/, '') || 'index';

  // Extract content after DocItem renders
  useEffect(() => {
    // Small delay to ensure content is rendered
    const timer = setTimeout(() => {
      if (contentRef.current) {
        const contentElement = contentRef.current.querySelector('.theme-doc-markdown.markdown');
        if (contentElement) {
          setDocContent(contentElement.innerHTML);
        }
      }
    }, 100);

    return () => clearTimeout(timer);
  }, [location.pathname]);

  // Handle content change from ChapterControls
  const handleContentChange = (newContent: string, type: 'original' | 'personalized' | 'translated') => {
    if (contentRef.current) {
      const contentElement = contentRef.current.querySelector('.theme-doc-markdown.markdown');
      if (contentElement) {
        if (type === 'original') {
          // Reset - need to force re-render of DocItem
          setContentKey(prev => prev + 1);
        } else {
          // Apply transformed content
          contentElement.innerHTML = newContent;

          // Apply RTL styling for Urdu translation
          if (type === 'translated') {
            contentElement.setAttribute('dir', 'rtl');
            (contentElement as HTMLElement).style.textAlign = 'right';
          } else {
            contentElement.removeAttribute('dir');
            (contentElement as HTMLElement).style.textAlign = '';
          }
        }
      }
    }
  };

  return (
    <div ref={contentRef}>
      <ChapterControls
        chapterSlug={chapterSlug}
        initialContent={docContent}
        onContentChange={handleContentChange}
      />
      <DocItem key={contentKey} {...props} />
    </div>
  );
}
