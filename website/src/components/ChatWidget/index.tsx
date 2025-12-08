import React, { useState, useEffect, useRef } from 'react';
import styles from './styles.module.css';
import { streamChat, sendFeedback } from './api';
import { useTextSelection } from './hooks';

// Inline SVGs for Avatars and Icons
const RobotIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C10.3431 2 9 3.34315 9 5C9 6.65685 10.3431 8 12 8C13.6569 8 15 6.65685 15 5C15 3.34315 13.6569 2 12 2Z" fill="currentColor"/>
    <path d="M19 8H5C3.34315 8 2 9.34315 2 11V22H22V11C22 9.34315 20.6569 8 19 8Z" fill="currentColor"/>
    <circle cx="9" cy="14" r="1.5" fill="white"/>
    <circle cx="15" cy="14" r="1.5" fill="white"/>
  </svg>
);

const UserIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
    <circle cx="12" cy="7" r="4"></circle>
  </svg>
);

const SendIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="22" y1="2" x2="11" y2="13"></line>
    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
  </svg>
);

const CloseIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="18" y1="6" x2="6" y2="18"></line>
    <line x1="6" y1="6" x2="18" y2="18"></line>
  </svg>
);

const ChatIcon = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
  </svg>
);

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<{role: 'user' | 'assistant', content: string, id?: string, feedback?: 1 | -1, context?: string}[]>([
      { role: 'assistant', content: 'Hello! I am here to help you understand the content of this book. Feel free to ask me any questions about it!' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatWindowRef = useRef<HTMLDivElement>(null);
  
  // Selection Menu State
  const [selectionData, setSelectionData] = useState<{text: string, x: number, y: number} | null>(null);
  const [contextText, setContextText] = useState(''); // Text to be sent with query

  useEffect(() => {
    const handleSelectionChange = () => {
        const selection = window.getSelection();
        // Only handle clearing here to avoid glitching during drag
        if (!selection || selection.toString().trim().length === 0) {
            setSelectionData(null);
        }
    };

    const handleMouseUp = () => {
        const selection = window.getSelection();
        if (selection && selection.toString().trim().length > 0) {
             // Check if selection is inside chat window
            if (chatWindowRef.current && chatWindowRef.current.contains(selection.anchorNode)) {
                return;
            }

            // If chat is OPEN, auto-set context
            if (isOpen) {
                setContextText(selection.toString());
                setSelectionData(null); // Ensure button doesn't show
                return;
            }

            // If chat is CLOSED, show floating button
            const range = selection.getRangeAt(0);
            const rect = range.getBoundingClientRect();
            
            setSelectionData({
                text: selection.toString(),
                x: rect.left + rect.width / 2,
                y: rect.top - 10 
            });
        }
    };

    document.addEventListener('selectionchange', handleSelectionChange);
    document.addEventListener('mouseup', handleMouseUp);
    
    return () => {
        document.removeEventListener('selectionchange', handleSelectionChange);
        document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isOpen]); // Re-bind when open state changes to capture correct 'isOpen' value

  const handleAskAI = () => {
      if (selectionData) {
          setContextText(selectionData.text);
          setIsOpen(true);
          setSelectionData(null); // Hide button
          // Clear visual selection
          window.getSelection()?.removeAllRanges();
      }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const toggleChat = () => setIsOpen(!isOpen);
  
  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMsg = input;
    const currentContext = contextText;
    
    setMessages(prev => [...prev, { role: 'user', content: userMsg, context: currentContext }]);
    setInput('');
    setLoading(true);
    setContextText(''); // Clear context after sending
    
    setMessages(prev => [...prev, { role: 'assistant', content: '' }]);
    
    try {
        await streamChat({ 
            message: userMsg, 
            selected_text: currentContext,
        }, 
        (token) => {
             setMessages(prev => {
                const newMsgs = [...prev];
                const lastMsg = newMsgs[newMsgs.length - 1];
                if (lastMsg.role === 'assistant') {
                    lastMsg.content += token;
                }
                return newMsgs;
             });
        },
        (meta) => {
            if (meta.message_id) {
                 setMessages(prev => {
                    const newMsgs = [...prev];
                    const lastMsg = newMsgs[newMsgs.length - 1];
                    if (lastMsg.role === 'assistant') {
                        lastMsg.id = meta.message_id;
                    }
                    return newMsgs;
                 });
            }
        });
    } catch (err) {
        console.error("Chat error:", err);
    } finally {
        setLoading(false);
    }
  };

  return (
    <>
        {/* Floating Selection Menu */}
        {selectionData && !isOpen && (
            <div 
                className={styles.selectionMenu}
                style={{ top: selectionData.y, left: selectionData.x }}
                onClick={handleAskAI}
                onMouseDown={(e) => e.preventDefault()}
            >
                <div className={styles.selectionMenuIcon}><RobotIcon /></div>
                <span>Ask AI</span>
            </div>
        )}

        <div className={styles.chatWidgetContainer}>
        {!isOpen && (
            <button className={styles.chatButton} onClick={toggleChat} aria-label="Open Chat">
            <div className={styles.chatIcon}><ChatIcon /></div>
            </button>
        )}
        
        {isOpen && (
            <div className={styles.chatWindow} ref={chatWindowRef}>
            <div className={styles.chatHeader}>
                <span className={styles.chatTitle}>
                    <RobotIcon /> AI Assistant
                </span>
                <button onClick={toggleChat} className={styles.closeButton}>
                    <CloseIcon />
                </button>
            </div>
            
            <div className={styles.chatMessages}>
                {messages.map((m, i) => (
                    <div key={i} className={`${styles.messageRow} ${m.role === 'user' ? styles.user : styles.assistant}`}>
                        {m.role === 'assistant' && (
                            <div className={`${styles.avatar} ${styles.assistantAvatar}`}>
                                <RobotIcon />
                            </div>
                        )}
                        {m.role === 'user' && (
                            <div className={`${styles.avatar} ${styles.userAvatar}`}>
                                <UserIcon />
                            </div>
                        )}
                        
                        <div style={{display: 'flex', flexDirection: 'column', maxWidth: '100%'}}>
                            <div className={styles.messageBubble}>
                                {m.context && (
                                    <div className={styles.messageContext}>
                                        <div className={styles.quoteBar}></div>
                                        <span>{m.context}</span>
                                    </div>
                                )}
                                {m.content}
                            </div>
                        </div>
                    </div>
                ))}
                {loading && messages[messages.length-1].content === '' && (
                    <div className={styles.loadingIndicator}>Thinking...</div>
                )}
                <div ref={messagesEndRef} />
            </div>
            
            <div className={styles.chatInputArea}>
                {contextText && (
                    <div className={styles.contextPreview}>
                        <div className={styles.contextContent}>
                            <span className={styles.contextLabel}>Selected Context:</span>
                            <span className={styles.contextText}>"{contextText}"</span>
                        </div>
                        <button onClick={() => setContextText('')} className={styles.closeContext}>✕</button>
                    </div>
                )}
                
                <div className={styles.inputRow}>
                    <input 
                        className={styles.chatInput}
                        value={input} 
                        onChange={e => setInput(e.target.value)} 
                        onKeyDown={e => e.key === 'Enter' && handleSend()}
                        placeholder="Ask a question..."
                        disabled={loading}
                    />
                    <button className={styles.sendButton} onClick={handleSend} disabled={loading || !input.trim()}>
                        <SendIcon />
                    </button>
                </div>
            </div>
            </div>
        )}
        </div>
    </>
  );
};

export default ChatWidget;
