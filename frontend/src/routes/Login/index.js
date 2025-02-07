import React from 'react';
import { Form, Input, Button, Typography } from 'antd';
import { useNavigate } from 'react-router-dom';
import cookie from '../../core/helpers/cookie';
import useLocalData from "../../core/hook/useLocalData";

const { Title, Link } = Typography;

function Login() {
  const navigate = useNavigate();
  const { store, dispatch } = useLocalData();
  const cookieUser = cookie.get("user");

  const onFinish = async (values) => {
    const payload = {
        email: values.email,
        password: values.password,
    };
    try {
        console.log("Sending data:", payload);
        const response = await fetch("http://localhost:5000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        const result = await response.json();
        console.log("Response:", result);

        if (response.ok) {
            console.log("Login successful:", result);
            const userData = result.data.data; // Ambil data user
            const accessToken = result.data.access_token; // Ambil access token
            const refreshToken = result.data.refresh_token; // Ambil refresh token

            // Simpan user data di cookie
            cookie.set("user", JSON.stringify(userData), { path: "/", expires: 7 });

            // Simpan access token dan refresh token di cookie
            cookie.set("access_token", accessToken, { path: "/", expires: 7, secure: true, sameSite: "Strict" });
            cookie.set("refresh_token", refreshToken, { path: "/", expires: 7, secure: true, sameSite: "Strict" });

            if (cookieUser) {
                dispatch({
                    type: "update",
                    name: "userData",
                    value: JSON.parse(cookieUser),
                });
            }

            if (userData.user_id == 1) {
                navigate("/admin");
            } else {
                navigate("/dashboard");
            }
        } else {
            console.error("Login failed:", result);
            alert(result.message || "Login failed!");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong. Please try again.");
    }
  };


  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };

  return (
    <div style={{ display: "flex", flexWrap: "wrap", minHeight: "100vh" }}>
      <div style={{ flex: 1, backgroundColor: "#F2F9FF", padding: "50px", display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", minWidth: "300px" }}>
        <Title level={2}>Welcome back</Title>
        <p>Please enter your details</p>

        <Form name="login" layout="vertical" initialValues={{ remember: true }} onFinish={onFinish} onFinishFailed={onFinishFailed} style={{ width: "100%", maxWidth: "350px" }}>
          <Form.Item label="Email address" name="email" rules={[{ required: true, message: "Please input your email!" }, { type: "email", message: "Please enter a valid email!" }]}>
            <Input placeholder="Enter your email" />
          </Form.Item>

          <Form.Item label="Password" name="password" rules={[{ required: true, message: "Please input your password!" }]}>
            <Input.Password placeholder="Enter your password" />
          </Form.Item>

          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
            <Link>Forgot password</Link>
          </div>

          <Form.Item>
            <Button type="primary" htmlType="submit" block style={{ marginBottom: "16px" }}>
              Sign in
            </Button>
          </Form.Item>
        </Form>

        <p style={{ marginTop: "16px" }}>
          Don’t have an account? <a href="/register">Sign up</a>
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

export default Login;