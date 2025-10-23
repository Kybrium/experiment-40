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
    const res = await fetch(`${baseUrl}/api/accounts/register/`, {
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
    const res = await fetch(`${baseUrl}/api/accounts/token/`, {
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