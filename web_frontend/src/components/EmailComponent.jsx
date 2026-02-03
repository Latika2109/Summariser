import React, { useState } from 'react';
import api from '../utils/api';
import './EmailComponent.css';

function EmailComponent({ datasetId, datasetName }) {
  const [email, setEmail] = useState('');
  const [sending, setSending] = useState(false);
  const [message, setMessage] = useState('');

  const sendEmail = async () => {
    if (!email) {
      setMessage('Please enter an email address');
      return;
    }

    setSending(true);
    setMessage('');

    try {
      const response = await api.post(`/datasets/${datasetId}/send-email/`, {
        email: email
      });

      if (response.data.success) {
        setMessage('Email sent successfully!');
        setEmail('');
      } else {
        setMessage('Failed to send email');
      }
    } catch (error) {
      console.error('Error sending email:', error);
      const errorMessage = error.response?.data?.error || 'Error sending email. Please check server logs.';
      setMessage(errorMessage);
    }

    setSending(false);
  };

  return (
    <div className="email-component">
      <h3>Email Report</h3>
      <p>Send this dataset report to an email address</p>

      <div className="email-form">
        <input
          type="email"
          placeholder="Enter email address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          disabled={sending}
        />
        <button onClick={sendEmail} disabled={sending || !email}>
          {sending ? 'Sending...' : 'Send Report'}
        </button>
      </div>

      {message && (
        <div className={`message ${message.includes('successfully') ? 'success' : 'error'}`}>
          {message}
        </div>
      )}

      <div className="email-info">
        <small>
          The report will include:
          <ul>
            <li>Summary statistics</li>
            <li>Equipment type distribution</li>
            <li>Charts and visualizations</li>
          </ul>
        </small>
      </div>
    </div>
  );
}

export default EmailComponent;
