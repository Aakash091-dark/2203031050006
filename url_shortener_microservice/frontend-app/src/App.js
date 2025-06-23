import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [url, setUrl] = useState("");
  const [validity, setValidity] = useState(30);
  const [shortcode, setShortcode] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResponse(null);

    try {
      const res = await axios.post("http://127.0.0.1:8000/shorturls", {
        url,
        validity,
        shortcode: shortcode || undefined,
      });
      setResponse(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong!");
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.heading}>🔗 URL Shortener</h2>

        <form onSubmit={handleSubmit} style={styles.form}>
          <label style={styles.label}>🔍 Long URL</label>
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter your long URL"
            required
            style={styles.input}
          />

          <label style={styles.label}>🕒 Validity (in minutes)</label>
          <input
            type="number"
            value={validity}
            onChange={(e) => setValidity(e.target.value)}
            style={styles.input}
          />

          <label style={styles.label}>✏️ Custom Shortcode (optional)</label>
          <input
            type="text"
            value={shortcode}
            onChange={(e) => setShortcode(e.target.value)}
            style={styles.input}
          />

          <button type="submit" style={styles.button}>Generate Short URL</button>
        </form>

        {response && (
          <div style={styles.resultBox}>
            <p><strong>✅ Short Link:</strong></p>
            <a href={response.shortLink} target="_blank" rel="noreferrer" style={styles.link}>
              {response.shortLink}
            </a>
            <p><strong>⏳ Expires At:</strong> {response.expiry}</p>
          </div>
        )}

        {error && (
          <div style={styles.error}>
            ⚠️ {error}
          </div>
        )}
      </div>
    </div>
  );
};

const styles = {
  container: {
    background: "#f4f6f8",
    height: "100vh",
    padding: "40px 20px",
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
  },
  card: {
    maxWidth: "500px",
    background: "#fff",
    margin: "0 auto",
    padding: "30px 25px",
    borderRadius: "12px",
    boxShadow: "0 4px 16px rgba(0, 0, 0, 0.1)",
  },
  heading: {
    textAlign: "center",
    marginBottom: "20px",
    color: "#333",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "15px",
  },
  label: {
    fontWeight: "bold",
    marginBottom: "4px",
  },
  input: {
    padding: "10px",
    borderRadius: "6px",
    border: "1px solid #ccc",
    fontSize: "1rem",
  },
  button: {
    marginTop: "10px",
    padding: "12px",
    fontSize: "1rem",
    border: "none",
    borderRadius: "6px",
    backgroundColor: "#4CAF50",
    color: "white",
    cursor: "pointer",
    transition: "background-color 0.2s ease",
  },
  resultBox: {
    marginTop: "25px",
    background: "#e9fbe7",
    padding: "15px",
    borderRadius: "8px",
    color: "#256029",
  },
  link: {
    color: "#2a65f7",
    wordBreak: "break-all",
  },
  error: {
    marginTop: "20px",
    padding: "12px",
    backgroundColor: "#ffe5e5",
    border: "1px solid #ff8b8b",
    color: "#a70000",
    borderRadius: "6px",
  },
};

export default App;
