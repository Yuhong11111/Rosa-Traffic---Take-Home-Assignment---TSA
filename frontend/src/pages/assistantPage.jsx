import { useState } from 'react'
import axios from 'axios'

export default function AssistantPage() {
    const [query, setQuery] = useState('')
    const [messages, setMessages] = useState([
        {
            role: 'ai',
            content: 'Welcome! Ask any question and a placeholder AI will respond.',
        },
    ])
    const [result, setResult] = useState(null)

    async function handleSubmit(event) {
        event.preventDefault()
        const trimmed = query.trim()
        if (!trimmed) {
            return
        }
        const userMessage = { role: 'user', content: trimmed }
        setMessages((current) => [...current, userMessage])
        try {
            const response = await axios.post('/api/assistant', { question: trimmed });
            const data = response.data.result;
            setResult(data);

            // Format the result for display
            let aiResponse = ''
            if (typeof data === 'object' && data !== null) {
                if (data.count !== undefined) {
                    aiResponse = `Found ${data.count} vehicle(s) matching your criteria.`
                } else if (data.average_speed !== undefined) {
                    aiResponse = `The average speed is ${data.average_speed} km/h.`
                } else if (data.max_speed !== undefined) {
                    aiResponse = `The maximum speed is ${data.max_speed} km/h.`
                } else if (Array.isArray(data)) {
                    aiResponse = `Found ${data.length} record(s). See details in the Results panel.`
                } else {
                    aiResponse = JSON.stringify(data)
                }
            } else {
                aiResponse = `Result: ${data}`
            }

            const mockAiMessage = {
                role: 'ai',
                content: aiResponse,
            }
            setMessages((current) => [...current, mockAiMessage])
        } catch (error) {
            console.error('Error sending message:', error)
            const errorMessage = {
                role: 'ai',
                content: `Sorry, there was an error processing your request: ${error.message}`,
            }
            setMessages((current) => [...current, errorMessage])
        }
        setQuery('')
    }

    return (
        <div className="assistant-page">
            <div className="assistant-layout">
                <section className="assistant-box">
                    <header className="assistant-header">
                        <h1>Assistant</h1>
                        <p>Prototype UI — responses are mocked locally.</p>
                    </header>

                    <div className="messages" aria-live="polite">
                        {messages.map((message, index) => (
                            <div
                                key={`${message.role}-${index}`}
                                className={`message ${message.role}`}
                            >
                                <span className="message-role">
                                    {message.role === 'user' ? 'You' : 'AI'}
                                </span>
                                <p>{message.content}</p>
                            </div>
                        ))}
                    </div>

                    <form className="query-form" onSubmit={handleSubmit}>
                        <textarea
                            className="query-input"
                            placeholder="Type your question..."
                            value={query}
                            onChange={(event) => setQuery(event.target.value)}
                            rows={4}
                        />
                        <button className="query-button" type="submit">
                            Ask
                        </button>
                    </form>
                </section>

                <section className="result-box">
                    <h2>Results</h2>
                    {result ? (
                        <div className="result-content">
                            {typeof result === 'object' && result !== null ? (
                                Array.isArray(result) ? (
                                    <table className="result-table">
                                        <thead>
                                            <tr>
                                                <th>Collection Time</th>
                                                <th>Direction</th>
                                                <th>Lane</th>
                                                <th>Speed (km/h)</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {result.map((record, index) => (
                                                <tr key={index}>
                                                    <td>{record.CollectionTime}</td>
                                                    <td>{record.Direction}</td>
                                                    <td>{record.Lane}</td>
                                                    <td>{record.Speed}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                ) : (
                                    <table className="result-table result-summary-table">
                                        <thead>
                                            <tr>
                                                <th>Metric</th>
                                                <th>Value</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {Object.entries(result).map(([key, value]) => (
                                                <tr key={key}>
                                                    <td>{key.replace(/_/g, ' ')}</td>
                                                    <td>{String(value)}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                )
                            ) : (
                                <p>{result}</p>
                            )}
                        </div>
                    ) : (
                        <p>
                            Placeholder area to display summaries, tables, or other AI output.
                            Current data is mocked locally. Future implementation will integrate with a backend AI.
                        </p>
                    )}
                </section>
            </div>
        </div>
    );
}
