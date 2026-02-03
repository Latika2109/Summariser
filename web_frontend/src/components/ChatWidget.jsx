import React, { useState, useRef, useEffect } from 'react';
import api from '../utils/api';
import './ChatWidget.css';

function ChatWidget({ datasetId, navigateTo }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'ai', text: 'Hi! I am your Equipment Assistant. Ask me anything about your data.' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isOpen]);

  const handleSend = async () => {
    if (!input.trim() || !datasetId) return;

    const userMsg = input.trim();
    setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setInput('');
    setLoading(true);

    try {
      const response = await api.post(`/datasets/${datasetId}/chat/`, {
        message: userMsg
      });

      const rawResponse = response.data.response;

      // Parse Navigation Commands
      let cleanResponse = rawResponse;
      if (rawResponse.includes('<<NAV:')) {
        const navMatch = rawResponse.match(/<<NAV:([A-Z]+)>>/);
        if (navMatch) {
          const destination = navMatch[1]; // DASHBOARD, ALERTS, etc.
          cleanResponse = rawResponse.replace(/<<NAV:[A-Z]+>>/g, '').trim();

          // Trigger Navigation
          // We expect navigateTo to be a function prop passed from App.js
          setTimeout(() => {
            if (navigateTo) navigateTo(destination);
          }, 1000);
        }
      }

      setMessages(prev => [...prev, { role: 'ai', text: cleanResponse }]);
    } catch (error) {
      console.error('Chat error:', error);
      let errorText = "Sorry, I encountered an error connecting to the brain.";
      if (error.response) {
        errorText += ` (Status: ${error.response.status})`;
        if (error.response.data && error.response.data.error) {
          errorText += `\nDetails: ${error.response.data.error}`;
        }
      } else if (error.message) {
        errorText += `\n${error.message}`;
      }
      setMessages(prev => [...prev, { role: 'ai', text: errorText }]);
    }
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <>
      {/* Floating Button */}
      <button
        className="chat-widget-fab"
        onClick={() => setIsOpen(!isOpen)}
        title="Chat with AI"
      >
        {isOpen ? '×' : '💬'}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <h3>AI Assistant</h3>
            <button className="close-btn" onClick={() => setIsOpen(false)}>×</button>
          </div>

          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.role}`}>
                {msg.text}
              </div>
            ))}
            {loading && <div className="typing-indicator">Thinking...</div>}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-area">
            <input
              type="text"
              placeholder={datasetId ? "Ask a question..." : "Please load a dataset first"}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={loading || !datasetId}
            />
            <button
              className="send-btn"
              onClick={handleSend}
              disabled={loading || !input.trim() || !datasetId}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </>
  );
}

export default ChatWidget;
