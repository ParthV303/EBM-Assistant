import { useState } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/ask",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question,
          }),
        }
      );

      const data = await response.json();

      setAnswer(data.answer);
    } catch (error) {
      setAnswer(
        "❌ Error: Unable to get response from backend."
      );
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "30px", textAlign: "center" }}>
      <h1>EBM Assistant</h1>

      <textarea
        rows="4"
        cols="60"
        placeholder="Ask a medical question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <br />
      <br />

      <button
        onClick={askQuestion}
        disabled={loading}
        style={{
          padding: "10px 20px",
          cursor: loading ? "not-allowed" : "pointer",
        }}
      >
        {loading ? "Processing..." : "Send"}
      </button>

      <hr />

      <h3>Answer:</h3>

      {loading ? (
        <div
          style={{
            marginTop: "20px",
            fontSize: "16px",
            color: "#007bff",
            fontWeight: "bold",
            lineHeight: "1.8",
          }}
        >
          🔬 Searching oncology research papers...<br />
          🤖 Generating evidence-based answer...<br />
          <span style={{ fontSize: "13px", color: "#888", fontWeight: "normal" }}>
            ⏳ The AI model may take up to 2 minutes. Please wait.
          </span>
        </div>
      ) : (
        <pre
          style={{
            whiteSpace: "pre-wrap",
            textAlign: "left",
            maxWidth: "1200px",
            margin: "20px auto",
            padding: "15px",
            border: "1px solid #ddd",
            borderRadius: "10px",
            backgroundColor: "#f8f9fa",
            fontSize: "16px",
          }}
        >
          {answer}
        </pre>
      )}
    </div>
  );
}

export default App;