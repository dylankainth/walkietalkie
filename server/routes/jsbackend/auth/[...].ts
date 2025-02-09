import { NuxtAuthHandler } from '#auth'
import GoogleProvider from 'next-auth/providers/google'
import { MongoClient } from 'mongodb'; // Import MongoDB client

// MongoDB connection setup (do this outside the handler for efficiency)
const uri = process.env.MONGODB_URI; // Your MongoDB connection string
if (!uri) {
    console.error('MONGODB_URI is not set');
    process.exit(1);
}


export default NuxtAuthHandler({
    // A secret string you define, to ensure correct encryption
    secret: process.env.AUTH_SECRET,
    providers: [
        // @ts-expect-error Use .default here for it to work during SSR.
        GoogleProvider.default({
            clientId: process.env.GOOGLE_CLIENT_ID,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET
        })
    ],
    callbacks: {
        async signIn({ user, account, profile }) {
            let mongoClient: MongoClient | null = null;
            try {
                mongoClient = new MongoClient(uri);
                await mongoClient.connect();
                console.log('Connected to MongoDB');
            } catch (error) {
                console.error('Error connecting to MongoDB:', error);
                // Handle the error appropriately, perhaps exit the process
                process.exit(1); // Or throw the error if you want it to bubble up.
            }
            const db = mongoClient?.db(process.env.MONGODB_NAME)
            const usersCollection = db?.collection('users'); // Your user collection

            // This is the crucial callback where you interact with MongoDB
            if (usersCollection) { // Only on the first signup with the provider
                try {
                    // Check if user already exists (e.g. if logging in with different provider)
                    const existingUser = await usersCollection.findOne({ email: user.email });

                    if (!existingUser) {
                        await usersCollection.insertOne({
                            name: user.name, // Or profile.name if available
                            email: user.email,
                            providerId: user.id // The provider ID
                        });
                    }
                } catch (error) {
                    console.error('Error inserting user into MongoDB:', error);
                    // Handle the error (e.g., log it, display a message)
                }
            }
            return true; // Important: Return true to allow the sign-in to proceed
        }
    }
})