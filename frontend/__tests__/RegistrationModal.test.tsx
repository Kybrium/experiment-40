import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { renderWithRQ, createTestClient, flushTimers } from '../src/lib/tests/test-utils';
import RegistrationModal from '@/components/auth/RegistrationModal';
import { toast } from 'react-toastify';

jest.mock('@/endpoints/auth', () => ({
    __esModule: true,
    registerUser: jest.fn(),
    fetchCurrentUser: jest.fn().mockResolvedValue({ username: 'john' }),
}));
import { registerUser } from '@/endpoints/auth';

const { __router: router } = jest.requireMock('next/navigation');

describe('RegistrationModal', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('shows client-side validation on empty submit', async () => {
        const setIsLogin = jest.fn();
        renderWithRQ(<RegistrationModal setIsLogin={setIsLogin} />);

        const user = userEvent.setup();
        await user.click(screen.getByRole('button', { name: /register/i }));

        await screen.findByText(/^Username is required\.$/i);
        await screen.findByText(/^Email is required\.$/i);
        await screen.findByText(/^Password is required\.$/i);
        await screen.findByText(/^Repeating your password is required\.$/i);
    });

    test('password mismatch shows "Passwords do not match."', async () => {
        const setIsLogin = jest.fn();
        renderWithRQ(<RegistrationModal setIsLogin={setIsLogin} />);

        const user = userEvent.setup();
        await user.type(screen.getByPlaceholderText(/username/i), 'alice');
        await user.type(screen.getByPlaceholderText(/email/i), 'alice@example.com');
        await user.type(screen.getByPlaceholderText(/^password$/i), 'Password1');
        await user.type(screen.getByPlaceholderText(/repeat password/i), 'Password2');

        await user.click(screen.getByRole('button', { name: /register/i }));

        expect(await screen.findByText(/passwords do not match\./i)).toBeInTheDocument();
        expect(router.push).not.toHaveBeenCalled();
    });

    test('invalid email shows validation message', async () => {
        const setIsLogin = jest.fn();
        renderWithRQ(<RegistrationModal setIsLogin={setIsLogin} />);

        const user = userEvent.setup();
        await user.type(screen.getByPlaceholderText(/username/i), 'bob');
        await user.type(screen.getByPlaceholderText(/email/i), 'not-an-email');
        await user.type(screen.getByPlaceholderText(/^password$/i), 'Password1');
        await user.type(screen.getByPlaceholderText(/repeat password/i), 'Password1');

        await user.click(screen.getByRole('button', { name: /register/i }));

        expect(await screen.findByText(/please enter a valid email address\./i)).toBeInTheDocument();
    });

    test('successful register: toast, invalidate & prefetch "me", then router.push', async () => {
        const setIsLogin = jest.fn();
        (registerUser as jest.Mock).mockResolvedValue({ ok: true });

        jest.useFakeTimers();

        const qc = createTestClient();
        const invalidateSpy = jest.spyOn(qc, 'invalidateQueries');
        const prefetchSpy = jest.spyOn(qc, 'prefetchQuery' as any);

        renderWithRQ(<RegistrationModal setIsLogin={setIsLogin} />, qc);

        const user = userEvent.setup({ advanceTimers: jest.advanceTimersByTime });
        await user.type(screen.getByPlaceholderText(/username/i), 'carol');
        await user.type(screen.getByPlaceholderText(/email/i), 'carol@example.com');
        await user.type(screen.getByPlaceholderText(/^password$/i), 'Password1');
        await user.type(screen.getByPlaceholderText(/repeat password/i), 'Password1');
        await user.click(screen.getByRole('button', { name: /register/i }));

        await waitFor(() => {
            expect(toast.success).toHaveBeenCalledWith(expect.stringMatching(/registration success/i));
            expect(invalidateSpy).toHaveBeenCalledWith({ queryKey: ['me'] });
            expect(prefetchSpy).toHaveBeenCalledWith({ queryKey: ['me'], queryFn: expect.any(Function) });
        });

        await Promise.resolve();
        await flushTimers(1500);

        await waitFor(() => {
            expect(router.push).toHaveBeenCalledWith('/dashboard');
        });
    });

    test('failed register: shows toast.error and does not redirect', async () => {
        const setIsLogin = jest.fn();
        (registerUser as jest.Mock).mockRejectedValue(new Error('Email already used'));

        renderWithRQ(<RegistrationModal setIsLogin={setIsLogin} />);

        const user = userEvent.setup();
        await user.type(screen.getByPlaceholderText(/username/i), 'dave');
        await user.type(screen.getByPlaceholderText(/email/i), 'dave@example.com');
        await user.type(screen.getByPlaceholderText(/^password$/i), 'Password1');
        await user.type(screen.getByPlaceholderText(/repeat password/i), 'Password1');
        await user.click(screen.getByRole('button', { name: /register/i }));

        await waitFor(() => {
            expect(toast.error).toHaveBeenCalledWith(expect.stringMatching(/email already used/i));
        });

        expect(router.push).not.toHaveBeenCalled();
    });

    test('Back to Login button calls setIsLogin(true)', async () => {
        const setIsLogin = jest.fn();
        renderWithRQ(<RegistrationModal setIsLogin={setIsLogin} />);

        const user = userEvent.setup();
        await user.click(screen.getByRole('button', { name: /back to login/i }));

        expect(setIsLogin).toHaveBeenCalledWith(true);
    });
});