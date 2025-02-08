// server/api/readData.js
import { MongoClient } from 'mongodb';

let cachedClient = null;

async function connectToDatabase() {
    if (cachedClient) {
        return cachedClient;
    }

    const uri = process.env.MONGODB_URI;
    const dbName = process.env.MONGODB_NAME;

    if (!uri || !dbName) {
        throw new Error('Missing MONGODB_URI or MONGODB_NAME environment variables');
    }

    const client = new MongoClient(uri, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
    });

    await client.connect();
    cachedClient = client;
    return client.db(dbName);
}

export default defineEventHandler(async (event) => {
    try {
        const db = await connectToDatabase();
        const collection = db.collection('questions');

        const data = await collection.find({}).toArray();
        return { success: true, data };
    } catch (error) {
        console.error('Error fetching data:', error);
        return { success: false, message: 'Error fetching data' };
    }
});
