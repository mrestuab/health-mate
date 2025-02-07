import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Input, Button, Typography, message } from 'antd';

const { Title } = Typography;

function Register() {
  const navigate = useNavigate();
  const [phoneNumber, setPhoneNumber] = useState('');
  const [error, setError] = useState('');

  const handlePhoneChange = (e) => {
    const value = e.target.value;

    const phoneRegex = /^62[0-9]{9,13}$/;

    if (!phoneRegex.test(value)) {
      setError('Nomor telepon harus dimulai dengan 62 dan memiliki 9-13 digit.');
    } else {
      setError('');
    }

    setPhoneNumber(value);
  };

  const onFinish = async (values) => {
    const payload = {
      name: values.name,
      email: values.email,
      phone_number: values.phone_number,
      password: values.password,
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const result = await response.json();

      if (response.ok) {
        message.success(result.message || 'Registration successful!');
        if (result.token) {
          localStorage.setItem('access_token', result.token);
        }
        navigate('/login');
      } else {
        message.error(result.error || 'Registration failed.');
      }
    } catch (error) {
      console.error('Error:', error);
      message.error('Something went wrong!');
    }
  };

  const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
  };

  return (
    <div
      style={{
        display: 'flex',
        flexWrap: 'wrap',
        minHeight: '100vh',
      }}
    >
      <div
        style={{
          flex: 1,
          backgroundColor: '#F2F9FF',
          padding: '50px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          minWidth: '300px',
        }}
      >
        <Title level={2}>Welcome!</Title>

        <Form
          name="register"
          layout="vertical"
          initialValues={{ remember: true }}
          onFinish={onFinish}
          onFinishFailed={onFinishFailed}
          style={{ width: '100%', maxWidth: '350px' }}
        >
          <Form.Item
            label="Name"
            name="name"
            rules={[{ required: true, message: 'Please input your name!' }]}
          >
            <Input placeholder="Restu Agis" />
          </Form.Item>

          <Form.Item
            label="Email address"
            name="email"
            rules={[
              { required: true, message: 'Please input your email!' },
              { type: 'email', message: 'Please enter a valid email!' },
            ]}
          >
            <Input placeholder="Enter your email" />
          </Form.Item>

          <Form.Item
            label="Phone Number"
            name="phone_number"
            rules={[
              { required: true, message: 'Please input your phone number!' },
              {
                pattern: /^62[0-9]{9,13}$/,
                message: 'Nomor telepon harus dimulai dengan 62 dan memiliki 9-13 digit.',
              },
            ]}
          >
            <Input onChange={handlePhoneChange} placeholder="Contoh: 6281234567890" />
          </Form.Item>

          <Form.Item
            label="Password"
            name="password"
            rules={[{ required: true, message: 'Please input your password!' }]}
          >
            <Input.Password placeholder="Enter your password" />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              block
              style={{ marginBottom: '16px' }}
            >
              Sign Up
            </Button>
          </Form.Item>
        </Form>

        <p style={{ marginTop: '16px' }}>
          Ohh you have an account? <a href="/login">Sign in</a>
        </p>
      </div>

      <div
        style={{
          flex: 1,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          padding: '50px',
          minWidth: '300px',
        }}
      >
        <div style={{ textAlign: 'center' }}>
          <img
            src="image/medicine.gif"
            alt="reminder"
            style={{ width: '100%', maxWidth: '400px' }}
          />
          <p>Set your Time to take your medication on Time!</p>
        </div>
      </div>
    </div>
  );
}

export default Register;
