import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [url, setUrl] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const checkURL = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await axios.post('http://localhost:8000/predict', {
        url: url
      })
      setResult(response.data)
    } catch (err) {
      setError('Failed to connect to the API. Make sure the backend is running.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="App">
      <div className="container">
        <h1>🛡️ Phishing URL Detector</h1>
        <p className="subtitle">AI-Powered Security Analysis</p>
        
        <form onSubmit={checkURL} className="form">
          <input
            type="text"
            placeholder="Enter URL to check (e.g., http://example.com)"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="input"
            required
          />
          <button type="submit" className="button" disabled={loading}>
            {loading ? 'Analyzing...' : 'Check URL'}
          </button>
        </form>

        {error && <div className="error">{error}</div>}

        {result && (
          <div className={`result ${result.prediction === 'Phishing' ? 'danger' : 'safe'}`}>
            <h2>Analysis Result</h2>
            <div className="result-content">
              <div className="prediction">
                <span className="label">Prediction:</span>
                <span className="value">{result.prediction}</span>
              </div>
              <div className="confidence">
                <span className="label">Confidence:</span>
                <span className="value">{result.confidence}%</span>
              </div>
              <div className="url-display">
                <span className="label">URL:</span>
                <span className="value">{result.url}</span>
              </div>
            </div>
            
            <div className="features">
              <h3>Extracted Features:</h3>
              <div className="features-grid">
                {Object.entries(result.features).map(([key, value]) => (
                  <div key={key} className="feature-item">
                    <span>{key.replace(/_/g, ' ').toUpperCase()}:</span>
                    <span>{value}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App