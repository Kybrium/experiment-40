const pushMock = jest.fn();

jest.mock('next/navigation', () => {
    return {
        __esModule: true,
        useRouter: () => ({ push: pushMock }),
    };
});

jest.mock('react-toastify', () => {
    const actual = jest.requireActual('react-toastify');
    return {
        ...actual,
        toast: {
            success: jest.fn(),
            error: jest.fn(),
        },
    };
});

jest.mock('@/endpoints/auth', () => ({
    __esModule: true,
    loginUser: jest.fn(),
    fetchCurrentUser: jest.fn().mockResolvedValue({ username: 'john' }),
}));

import { screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { renderWithAll, createTestClient } from '../src/lib/tests/test-utils';
import LoginModal from '@/components/auth/LoginModal';
import { toast } from 'react-toastify';
import { loginUser } from '@/endpoints/auth';

describe('LoginModal', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    afterEach(() => {
        jest.useRealTimers();
    });

    test('shows client-side validation messages on empty submit', async () => {
        const setIsLogin = jest.fn();
        renderWithAll(<LoginModal setIsLogin={setIsLogin} />);

        const user = userEvent.setup();
        await user.click(screen.getByRole('button', { name: /login/i }));

        expect(await screen.findByText(/username is required\./i)).toBeInTheDocument();
        expect(await screen.findByText(/password is required\./i)).toBeInTheDocument();
    });

    test('successful login: toast, invalidate & prefetch "me", then router.push', async () => {
        const setIsLogin = jest.fn();

        jest.useFakeTimers();

        (loginUser as jest.Mock).mockResolvedValue({
            access: 'a',
            refresh: 'r',
        });

        const qc = createTestClient();

        const invalidateSpy = jest
            .spyOn(qc, 'invalidateQueries')
            .mockResolvedValue(undefined as any);

        const prefetchSpy = jest
            .spyOn(qc, 'prefetchQuery' as any)
            .mockResolvedValue(undefined);

        renderWithAll(<LoginModal setIsLogin={setIsLogin} />, qc);

        const user = userEvent.setup({
            advanceTimers: jest.advanceTimersByTime,
        });

        await user.type(screen.getByPlaceholderText(/username/i), 'alice');
        await user.type(screen.getByPlaceholderText(/password/i), 'Password1');

        await user.click(screen.getByRole('button', { name: /login/i }));

        await waitFor(() => {
            expect(toast.success).toHaveBeenCalled();
            expect(invalidateSpy).toHaveBeenCalledWith({ queryKey: ['me'] });
            expect(prefetchSpy).toHaveBeenCalledWith({
                queryKey: ['me'],
                queryFn: expect.any(Function),
            });
        });

        await act(async () => {
            jest.runAllTimers();
            await Promise.resolve();
        });

        expect(pushMock).toHaveBeenCalledWith('/dashboard');
    });

    test('failed login: shows toast.error and does not redirect', async () => {
        const setIsLogin = jest.fn();

        (loginUser as jest.Mock).mockRejectedValue(new Error('Invalid credentials'));

        renderWithAll(<LoginModal setIsLogin={setIsLogin} />);

        const user = userEvent.setup();
        await user.type(screen.getByPlaceholderText(/username/i), 'bob');
        await user.type(screen.getByPlaceholderText(/password/i), 'wrongpass1');
        await user.click(screen.getByRole('button', { name: /login/i }));

        await waitFor(() => {
            expect(toast.error).toHaveBeenCalledWith(expect.stringMatching(/invalid/i));
        });

        expect(pushMock).not.toHaveBeenCalled();
    });

    test('clicking Register switches to registration view via setIsLogin(false)', async () => {
        const setIsLogin = jest.fn();
        renderWithAll(<LoginModal setIsLogin={setIsLogin} />);

        const user = userEvent.setup();
        await user.click(screen.getByRole('button', { name: /register/i }));

        expect(setIsLogin).toHaveBeenCalledWith(false);
    });
});