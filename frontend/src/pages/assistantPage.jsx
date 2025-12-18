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
            console.log(response.data.filter);
        } catch (error) {
            console.error('Error sending message:', error)
        }
        const mockAiMessage = {
            role: 'ai',
            content: `AI (mock): I'm still in training, but I heard "${trimmed}".`,
        }

        setMessages((current) => [...current, mockAiMessage])
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
                    <p>
                        Placeholder area to display summaries, tables, or other AI output.
                        Design this section however you like once real data is available.
                    </p>
                </section>
            </div>
        </div>
    );
}
