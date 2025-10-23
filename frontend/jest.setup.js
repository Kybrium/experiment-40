import '@testing-library/jest-dom/extend-expect';

// --- Stable, shared router mock ---
const router = {
    push: jest.fn(),
    replace: jest.fn(),
    refresh: jest.fn(),
    prefetch: jest.fn(),
};

jest.mock('next/navigation', () => ({
    __esModule: true,
    useRouter: () => router,
    __router: router,
}));

jest.mock('react-toastify', () => ({
    __esModule: true,
    toast: {
        success: jest.fn(),
        error: jest.fn(),
    },
}));

afterEach(() => {
    jest.useRealTimers();
    jest.clearAllMocks();
});