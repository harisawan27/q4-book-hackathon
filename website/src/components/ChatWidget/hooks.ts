import { useState, useEffect } from 'react';

export const useTextSelection = () => {
    const [selection, setSelection] = useState<string>('');

    useEffect(() => {
        const handleSelectionChange = () => {
            const sel = window.getSelection();
            if (sel && sel.toString().trim().length > 0) {
                // Get selected text
                setSelection(sel.toString().trim());
            } else {
                // Only clear if explicit click outside? 
                // Usually we want to keep it until user clears it or selects something else.
                // But for standard behavior, maybe we don't clear immediately on click?
                // Let's clear if selection is empty (user clicked somewhere)
                if (sel && sel.toString().length === 0) {
                    setSelection('');
                }
            }
        };

        document.addEventListener('selectionchange', handleSelectionChange);
        return () => document.removeEventListener('selectionchange', handleSelectionChange);
    }, []);

    return selection;
};
