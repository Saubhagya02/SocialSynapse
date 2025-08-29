import React, { useState } from 'react';
import { authAPI } from '../lib/api';

const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | { msg?: string }[] | { msg?: string } | null>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      const response = await authAPI.login({ email, password });
      localStorage.setItem('token', response.data.access_token);
      window.location.href = '/'; // Redirect to home or dashboard
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{
      maxWidth: 400,
      margin: '3rem auto',
      padding: 32,
      borderRadius: 16,
      boxShadow: '0 4px 24px rgba(0,0,0,0.08)',
      background: 'linear-gradient(135deg, #f8fafc 0%, #e3e8ee 100%)',
      border: 'none',
      position: 'relative',
    }}>
      <h2 style={{
        textAlign: 'center',
        marginBottom: 32,
        fontWeight: 700,
        fontSize: 28,
        color: '#0072b1',
        letterSpacing: 1
      }}>Sign in to LinkedIn AI Agent</h2>
      <div style={{ marginBottom: 24 }}>
        <label style={{ display: 'block', marginBottom: 8, fontWeight: 500, color: '#333' }}>Email</label>
        <input type="email" value={email} onChange={e => setEmail(e.target.value)} required style={{
          width: '100%',
          padding: '12px 16px',
          borderRadius: 8,
          border: '1px solid #d1d5db',
          fontSize: 16,
          background: '#fff',
          boxSizing: 'border-box',
        }} />
      </div>
      <div style={{ marginBottom: 24 }}>
        <label style={{ display: 'block', marginBottom: 8, fontWeight: 500, color: '#333' }}>Password</label>
        <input type="password" value={password} onChange={e => setPassword(e.target.value)} required style={{
          width: '100%',
          padding: '12px 16px',
          borderRadius: 8,
          border: '1px solid #d1d5db',
          fontSize: 16,
          background: '#fff',
          boxSizing: 'border-box',
        }} />
      </div>
      {error && (
        <div style={{ color: '#e53e3e', marginBottom: 20, textAlign: 'center', fontWeight: 500 }}>
          {typeof error === 'string'
            ? error
            : Array.isArray(error)
              ? (error as any[]).map((e: any, i: number) => <div key={i}>{e.msg || JSON.stringify(e)}</div>)
              : error.msg || JSON.stringify(error)}
        </div>
      )}
      <button type="submit" style={{
        width: '100%',
        padding: '12px 0',
        background: 'linear-gradient(90deg, #0072b1 0%, #005580 100%)',
        color: '#fff',
        border: 'none',
        borderRadius: 8,
        fontWeight: 600,
        fontSize: 18,
        boxShadow: '0 2px 8px rgba(0,114,177,0.08)',
        cursor: 'pointer',
        transition: 'background 0.2s',
      }}>Login</button>
      <div style={{ marginTop: 24, textAlign: 'center' }}>
        <a href="/register" style={{
          color: '#0072b1',
          textDecoration: 'none',
          fontWeight: 500,
          fontSize: 16,
          borderBottom: '1px dotted #0072b1',
          paddingBottom: 2,
          transition: 'color 0.2s',
        }}>Don't have an account? <span style={{ fontWeight: 700 }}>Register</span></a>
      </div>
    </form>
  );
};

export default LoginForm;
