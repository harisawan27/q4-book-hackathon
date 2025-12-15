export interface ChatRequest {
    session_id?: string;
    message: string;
    selected_text?: string;
    page_context?: string;
}

// API URL - defaults to localhost for development, production URL for deployed sites
const getApiUrl = (): string => {
  if (typeof window !== 'undefined') {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      return 'http://localhost:8000/api/v1';
    }
    return 'https://harisawan07-q4-hackathon-1.hf.space/api/v1';
  }
  return 'https://harisawan07-q4-hackathon-1.hf.space/api/v1';
};

const API_URL = getApiUrl();

export const streamChat = async (
    request: ChatRequest, 
    onToken: (token: string) => void,
    onMetadata?: (meta: any) => void
) => {
    const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(request)
    });

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    if (!response.body) return;

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let buffer = "";

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value, { stream: true });
        buffer += chunk;
        
        // SSE messages are separated by \n\n
        const lines = buffer.split("\n\n");
        buffer = lines.pop() || ""; // Keep the last incomplete chunk in buffer
        
        for (const line of lines) {
            if (line.startsWith("data: ")) {
                const data = line.substring(6);
                if (data === "[DONE]") return;

                try {
                    // Try to parse as JSON
                    if (data.startsWith('{')) {
                        const json = JSON.parse(data);
                        if (json.type === 'meta' && onMetadata) {
                            onMetadata(json);
                            continue;
                        }
                    }
                    // If not meta, treat as token (or if parsing failed/not object)
                    onToken(data);
                } catch (e) {
                     onToken(data);
                }
            }
        }
    }
};

export const sendFeedback = async (messageId: string, score: number, comment?: string) => {
    await fetch(`${API_URL}/feedback?message_id=${messageId}&score=${score}${comment ? `&comment=${comment}` : ''}`, {
        method: 'POST'
    });
};
