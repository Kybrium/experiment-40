import { apiFetch } from "@/lib/apiFetch";
import { baseUrl } from "@/lib/constants"
import { getCookie } from "@/lib/cookies";
import { flattenDrfErrors } from "@/lib/endpoints";
import { LoginForm, RegistrationForm } from "@/types/auth";



/**
 * Sends a registration request to the API to create a new user.
 *
 * @param data - User registration data (username, email, password, etc.)
 * @returns The API response as JSON if the request is successful.
 * @throws Error if the registration fails or the server returns a non-OK response.
 */
export const registerUser = async (data: RegistrationForm) => {
    const csrftoken = getCookie("csrftoken");
    const res = await apiFetch(`${baseUrl}/api/accounts/register/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken || ""
        },
        body: JSON.stringify(data),
        credentials: "include",
    });

    if (!res.ok) {
        const raw = await res.text();
        let message = "Registration failed";
        try {
            const json = raw ? JSON.parse(raw) : null;
            message = json ? flattenDrfErrors(json) : (raw || message);
        } catch {
            message = raw || message;
        }
        throw new Error(message);
    }

    return res.json();
};


/**
 * Sends a login request to the API.
 *
 * @param data - User login data (username, password)
 * @returns The API response as JSON if the request is successful.
 * @throws Error if the login fails or the server returns a non-OK response.
 */
export const loginUser = async (data: LoginForm) => {
    const csrftoken = getCookie("csrftoken");
    const res = await apiFetch(`${baseUrl}/api/accounts/token/`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken || ""
        },
        body: JSON.stringify(data),
        credentials: "include",
    });

    if (!res.ok) {
        const raw = await res.text();
        let message = "Login failed";
        try {
            const json = raw ? JSON.parse(raw) : null;
            message = json ? flattenDrfErrors(json) : (raw || message);
        } catch {
            message = raw || message;
        }
        throw new Error(message);
    }

    return res.json();
}




/**
 * Fetches the currently authenticated user's information.
 *
 * This function calls the `/api/accounts/me/` endpoint, which returns
 * the profile data of the user associated with the current session
 * (based on the stored HTTP-only authentication cookies).
 *
 * - Returns `null` if the user is not authenticated (401 response).
 * - Throws an error if any other request failure occurs.
 *
 * @returns The current user object as JSON, or `null` if not logged in.
 * @throws Error if the request fails for any non-401 reason.
 */
export async function fetchCurrentUser() {
    const res = await apiFetch(`${baseUrl}/api/accounts/me/`, {
        method: 'GET',
        credentials: "include",
    });

    if (res.status === 401) return null;
    if (!res.ok) throw new Error("Failed to fetch user");

    return res.json();
}