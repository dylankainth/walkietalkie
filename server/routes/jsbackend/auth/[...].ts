import { NuxtAuthHandler } from '#auth'
import GoogleProvider from 'next-auth/providers/google'

export default NuxtAuthHandler({
    // A secret string you define, to ensure correct encryption
    secret: process.env.AUTH_SECRET,
    providers: [
        // @ts-expect-error Use .default here for it to work during SSR.
        GoogleProvider.default({
            clientId: process.env.GOOGLE_CLIENT_ID,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET
        })
    ]
})