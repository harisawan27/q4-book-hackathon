import React, { useState, useCallback, useEffect, useRef } from 'react';
import { useAuth } from '../AuthProvider';
import {
  personalizeContent,
  translateContent,
  TransformationResponse,
} from '../../lib/auth';
import styles from './styles.module.css';

interface ChapterControlsProps {
  chapterSlug: string;
  initialContent: string;
  onContentChange?: (content: string, type: 'original' | 'personalized' | 'translated') => void;
}

type ContentState = 'original' | 'personalized' | 'translated';

export function ChapterControls({
  chapterSlug,
  initialContent,
  onContentChange,
}: ChapterControlsProps) {
  const { isAuthenticated, hasBackground, isLoading: authLoading } = useAuth();

  const [contentState, setContentState] = useState<ContentState>('original');
  const [isPersonalizing, setIsPersonalizing] = useState(false);
  const [isTranslating, setIsTranslating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastTransformation, setLastTransformation] = useState<TransformationResponse | null>(null);
  // Track content availability with state to trigger re-renders
  const [contentLoaded, setContentLoaded] = useState(false);

  // Use ref to track the original content - updates when initialContent changes
  const originalContentRef = useRef(initialContent);

  // Update original content ref when initial content changes
  useEffect(() => {
    if (initialContent && initialContent.length > 0) {
      originalContentRef.current = initialContent;
      setContentLoaded(true);
    }
  }, [initialContent]);

  const handlePersonalize = useCallback(async () => {
    if (!isAuthenticated || !hasBackground) return;

    const content = originalContentRef.current;
    if (!content || content.length === 0) {
      setError('Content not loaded yet. Please wait a moment and try again.');
      return;
    }

    setIsPersonalizing(true);
    setError(null);

    try {
      const response = await personalizeContent(chapterSlug, content);
      setContentState('personalized');
      setLastTransformation(response);
      onContentChange?.(response.content, 'personalized');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to personalize content');
    } finally {
      setIsPersonalizing(false);
    }
  }, [isAuthenticated, hasBackground, chapterSlug, onContentChange]);

  const handleTranslate = useCallback(async () => {
    if (!isAuthenticated) return;

    const content = originalContentRef.current;
    if (!content || content.length === 0) {
      setError('Content not loaded yet. Please wait a moment and try again.');
      return;
    }

    setIsTranslating(true);
    setError(null);

    try {
      const response = await translateContent(chapterSlug, content);
      setContentState('translated');
      setLastTransformation(response);
      onContentChange?.(response.content, 'translated');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to translate content');
    } finally {
      setIsTranslating(false);
    }
  }, [isAuthenticated, chapterSlug, onContentChange]);

  const handleReset = useCallback(() => {
    setContentState('original');
    setError(null);
    setLastTransformation(null);
    onContentChange?.(originalContentRef.current, 'original');
  }, [onContentChange]);

  // Don't render anything if not authenticated
  if (!isAuthenticated) {
    return (
      <div className={styles.container}>
        <div className={styles.hint}>
          <a href="/signin">Sign in</a> to personalize and translate chapter content.
        </div>
      </div>
    );
  }

  const isLoading = isPersonalizing || isTranslating || authLoading;
  // Use contentLoaded state to properly trigger re-renders when content becomes available
  const hasContent = contentLoaded && originalContentRef.current && originalContentRef.current.length > 0;

  return (
    <div className={styles.container}>
      <div className={styles.controls}>
        {/* Personalize Button */}
        <button
          className={`button button--primary ${contentState === 'personalized' ? styles.active : ''}`}
          onClick={handlePersonalize}
          disabled={isLoading || !hasBackground || !hasContent}
          title={!hasContent ? 'Loading content...' : !hasBackground ? 'Complete your background questionnaire first' : 'Personalize content based on your background'}
        >
          {isPersonalizing ? (
            <>
              <span className={styles.spinner} />
              Personalizing...
            </>
          ) : (
            <>Personalize Content</>
          )}
        </button>

        {/* Translate Button */}
        <button
          className={`button button--secondary ${contentState === 'translated' ? styles.active : ''}`}
          onClick={handleTranslate}
          disabled={isLoading || !hasContent}
          title={!hasContent ? 'Loading content...' : 'Translate content to Urdu'}
        >
          {isTranslating ? (
            <>
              <span className={styles.spinner} />
              Translating...
            </>
          ) : (
            <>Translate to Urdu</>
          )}
        </button>

        {/* Reset Button - only show when content is transformed */}
        {contentState !== 'original' && (
          <button
            className="button button--outline"
            onClick={handleReset}
            disabled={isLoading}
            title="Reset to original content"
          >
            Reset to Original
          </button>
        )}
      </div>

      {/* Background Warning */}
      {!hasBackground && (
        <div className={styles.warning}>
          <a href="/profile">Complete your background questionnaire</a> to enable personalization.
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className={styles.error}>
          {error}
          <button className={styles.dismissButton} onClick={() => setError(null)}>
            Dismiss
          </button>
        </div>
      )}

      {/* Transformation Info */}
      {lastTransformation && contentState !== 'original' && (
        <div className={styles.info}>
          {contentState === 'personalized' ? 'Personalized' : 'Translated'} in{' '}
          {(lastTransformation.duration_ms / 1000).toFixed(1)}s
          {contentState === 'translated' && (
            <span className={styles.rtlIndicator}> (RTL text direction applied)</span>
          )}
        </div>
      )}
    </div>
  );
}

export default ChapterControls;
