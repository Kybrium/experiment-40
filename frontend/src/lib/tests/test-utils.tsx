import { ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render } from '@testing-library/react';
import { act } from 'react';

export function createTestClient() {
    return new QueryClient({
        defaultOptions: {
            queries: { retry: false, gcTime: 0 },
            mutations: { retry: false },
        },
    });
}

export function renderWithRQ(ui: ReactNode, client = createTestClient()) {
    return render(<QueryClientProvider client={client}>{ui}</QueryClientProvider>);
}

export async function flushTimers(ms = 0) {

    await Promise.resolve();
    await act(async () => {
        jest.advanceTimersByTime(ms);
        jest.runOnlyPendingTimers();
    });

    await Promise.resolve();
}