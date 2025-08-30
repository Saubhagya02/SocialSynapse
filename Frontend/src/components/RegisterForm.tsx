import React, { useState } from 'react';
import { authAPI } from '../lib/api';

const RegisterForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
  await authAPI.register({ email, password, name });
      setSuccess('Registration successful! You can now log in.');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed');
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 400, margin: '2rem auto', padding: 24, border: '1px solid #eee', borderRadius: 8 }}>
      <h2>Register</h2>
      <div style={{ marginBottom: 16 }}>
        <label>Name:</label>
        <input type="text" value={name} onChange={e => setName(e.target.value)} required style={{ width: '100%', padding: 8 }} />
      </div>
      <div style={{ marginBottom: 16 }}>
        <label>Email:</label>
        <input type="email" value={email} onChange={e => setEmail(e.target.value)} required style={{ width: '100%', padding: 8 }} />
      </div>
      <div style={{ marginBottom: 16 }}>
        <label>Password:</label>
        <input type="password" value={password} onChange={e => setPassword(e.target.value)} required style={{ width: '100%', padding: 8 }} />
      </div>
      {error && (
        <div style={{ color: 'red', marginBottom: 16 }}>
          {typeof error === 'string'
            ? error
            : Array.isArray(error)
              ? (error as any[]).map((e, i) => <div key={i}>{e.msg || JSON.stringify(e)}</div>)
              : (error as any).msg || JSON.stringify(error)}
        </div>
      )}
      {success && <div style={{ color: 'green', marginBottom: 16 }}>{success}</div>}
      <button type="submit" style={{ width: '100%', padding: 10, background: '#0072b1', color: '#fff', border: 'none', borderRadius: 4 }}>Register</button>
    </form>
  );
};

export default RegisterForm;
