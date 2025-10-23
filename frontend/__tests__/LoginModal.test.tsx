import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { renderWithRQ, createTestClient, flushTimers } from '../src/lib/tests/test-utils';
import LoginModal from '@/components/auth/LoginModal';
import { toast } from 'react-toastify';

jest.mock('@/endpoints/auth', () => ({
    __esModule: true,
    loginUser: jest.fn(),
    fetchCurrentUser: jest.fn().mockResolvedValue({ username: 'john' }),
}));
import { loginUser } from '@/endpoints/auth';

const { __router: router } = jest.requireMock('next/navigation');

describe('LoginModal', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('shows client-side validation messages on empty submit', async () => {
        const setIsLogin = jest.fn();
        renderWithRQ(<LoginModal setIsLogin={setIsLogin} />);

        const user = userEvent.setup();
        await user.click(screen.getByRole('button', { name: /login/i }));

        expect(await screen.findByText(/username is required\./i)).toBeInTheDocument();
        expect(await screen.findByText(/password is required\./i)).toBeInTheDocument();
    });

    test('successful login: toast, invalidate & prefetch "me", then router.push', async () => {
        const setIsLogin = jest.fn();
        (loginUser as jest.Mock).mockResolvedValue({ access: 'a', refresh: 'r' });

        jest.useFakeTimers();

        const qc = createTestClient();
        const invalidateSpy = jest.spyOn(qc, 'invalidateQueries');
        const prefetchSpy = jest.spyOn(qc, 'prefetchQuery' as any);

        renderWithRQ(<LoginModal setIsLogin={setIsLogin} />, qc);

        const user = userEvent.setup({ advanceTimers: jest.advanceTimersByTime });
        await user.type(screen.getByPlaceholderText(/username/i), 'alice');
        await user.type(screen.getByPlaceholderText(/password/i), 'Password1');
        await user.click(screen.getByRole('button', { name: /login/i }));

        await waitFor(() => {
            expect(toast.success).toHaveBeenCalled();
            expect(invalidateSpy).toHaveBeenCalledWith({ queryKey: ['me'] });
            expect(prefetchSpy).toHaveBeenCalledWith({ queryKey: ['me'], queryFn: expect.any(Function) });
        });

        await Promise.resolve();
        await flushTimers(1500);

        await waitFor(() => {
            expect(router.push).toHaveBeenCalledWith('/dashboard');
        });
    });

    test('failed login: shows toast.error and does not redirect', async () => {
        const setIsLogin = jest.fn();
        (loginUser as jest.Mock).mockRejectedValue(new Error('Invalid credentials'));

        renderWithRQ(<LoginModal setIsLogin={setIsLogin} />);

        const user = userEvent.setup();
        await user.type(screen.getByPlaceholderText(/username/i), 'bob');
        await user.type(screen.getByPlaceholderText(/password/i), 'wrongpass1');
        await user.click(screen.getByRole('button', { name: /login/i }));

        await waitFor(() => {
            expect(toast.error).toHaveBeenCalledWith(expect.stringMatching(/invalid/i));
        });

        expect(router.push).not.toHaveBeenCalled();
    });

    test('clicking Register switches to registration view via setIsLogin(false)', async () => {
        const setIsLogin = jest.fn();
        renderWithRQ(<LoginModal setIsLogin={setIsLogin} />);

        const user = userEvent.setup();
        await user.click(screen.getByRole('button', { name: /register/i }));

        expect(setIsLogin).toHaveBeenCalledWith(false);
    });
});
