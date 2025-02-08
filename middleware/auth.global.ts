// middleware/auth.global.ts
import { defineNuxtRouteMiddleware, navigateTo } from '#app';

export default defineNuxtRouteMiddleware(async (to) => {
    const { status } = useAuth(); // Use useAuth() instead of useSession()

    // Allow access to the /signin page without redirection
    if (to.path === '/auth/login') return;

    // Redirect unauthenticated users to /signin
    if (status.value !== 'authenticated') {
        return navigateTo('/auth/login');
    }
});