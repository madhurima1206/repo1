import { useState } from "react";
import axios from "axios";
import { ShieldAlert } from "lucide-react";
import { motion } from "framer-motion";

function App() {

  const [message, setMessage] = useState("");

  const [prediction, setPrediction] = useState("");

  const [loading, setLoading] = useState(false);

  const checkSpam = async () => {

    if(message.trim() === ""){
      alert("Please enter a message");
      return;
    }

    try {

      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:5000/predict",
        {
          message: message
        }
      );

      setPrediction(response.data.prediction);

      setLoading(false);

    } catch(error) {

      console.log(error);

      alert("Backend connection error");

      setLoading(false);
    }
  };

  return (

    <div style={styles.page}>

      <motion.div
        initial={{ opacity:0, y:50 }}
        animate={{ opacity:1, y:0 }}
        transition={{ duration:0.7 }}
        style={styles.card}
      >

        <div style={styles.header}>

          <ShieldAlert size={45} color="#38bdf8" />

          <h1 style={styles.title}>
            AI Spam Detector
          </h1>

        </div>

        <p style={styles.subtitle}>
          Detect spam emails instantly using Machine Learning & NLP
        </p>

        <textarea
          rows="10"
          placeholder="Paste your email content here..."
          value={message}
          onChange={(e)=>setMessage(e.target.value)}
          style={styles.textarea}
        />

        <button
          onClick={checkSpam}
          style={styles.button}
        >

          {
            loading ? "Analyzing..." : "Detect Spam"
          }

        </button>

        {
          prediction &&

          <motion.div
            initial={{ opacity:0 }}
            animate={{ opacity:1 }}
            style={styles.resultBox}
          >

            <h2 style={styles.result}>
              {prediction}
            </h2>

          </motion.div>
        }

      </motion.div>

    </div>
  );
}

const styles = {

  page: {
    minHeight: "100vh",
    background: "linear-gradient(to bottom right, #020617, #0f172a)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    padding: "20px",
    fontFamily: "Arial"
  },

  card: {
    width: "100%",
    maxWidth: "800px",
    background: "#111827",
    borderRadius: "25px",
    padding: "40px",
    boxShadow: "0px 0px 40px rgba(0,0,0,0.5)",
    border: "1px solid #1e293b"
  },

  header: {
    display: "flex",
    alignItems: "center",
    gap: "15px",
    justifyContent: "center"
  },

  title: {
    color: "white",
    fontSize: "42px",
    margin: 0
  },

  subtitle: {
    color: "#94a3b8",
    textAlign: "center",
    marginTop: "15px",
    fontSize: "18px"
  },

  textarea: {
    width: "100%",
    marginTop: "35px",
    background: "#020617",
    color: "white",
    border: "1px solid #334155",
    borderRadius: "20px",
    padding: "20px",
    fontSize: "17px",
    outline: "none",
    resize: "none",
    boxSizing: "border-box"
  },

  button: {
    width: "100%",
    marginTop: "25px",
    background: "#38bdf8",
    color: "black",
    border: "none",
    padding: "18px",
    borderRadius: "18px",
    fontSize: "20px",
    fontWeight: "bold",
    cursor: "pointer"
  },

  resultBox: {
    marginTop: "30px",
    textAlign: "center"
  },

  result: {
    color: "white",
    fontSize: "34px"
  }
};

export default App;