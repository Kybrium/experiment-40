import { baseUrl } from "@/lib/constants"
import { RegistrationForm } from "@/types/auth";


/**
 * Sends a registration request to the API to create a new user.
 *
 * @param data - User registration data (username, email, password, etc.)
 * @returns The API response as JSON if the request is successful.
 * @throws Error if the registration fails or the server returns a non-OK response.
 */
export const registerUser = async (data: RegistrationForm) => {
    const res = await fetch(`${baseUrl}/api/accounts/register/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    if (!res.ok) {
        const text = await res.text();
        throw new Error(`Registration failed: ${res.status} ${text}`);
    }

    return res.json();
};