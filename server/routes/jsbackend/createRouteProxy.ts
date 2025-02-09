// forward request to /api/createRoute
import { getToken } from '#auth'

export default eventHandler(async (event) => {
    const token = await getToken({ event })

    const body = await readBody(event)

    const response = await fetch('https://localhost:8000/api/createRoute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(body)
    })


    if (!response.ok) {
        throw new Error('Failed to create route');
    }

    const result = await response.json();
    return result;
});