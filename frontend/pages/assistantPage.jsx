import { useEffect, useState } from 'react'
import axios from 'axios'

export default function AssistantPage() {
    const [healthStatus, setHealthStatus] = useState('Checking API...')

    useEffect(() => {
        axios
            .get('health')
            .then((response) => {
                setHealthStatus(`API status: ${response.data.status}`)
            })
            .catch(() => {
                setHealthStatus('Unable to reach API')
            })
    }, [])

    return (
        <div>
            <h1>Assistant Page</h1>
            <p>{healthStatus}</p>
        </div>
    );
}
