import { render } from '@testing-library/react';
import { I18nextProvider } from 'react-i18next';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ToastContainer } from 'react-toastify';
import { createTestI18n } from './test-i18n';

export function createTestClient() {
    return new QueryClient({
        defaultOptions: {
            queries: {
                retry: false
            }
        }
    });
}

export async function flushTimers(ms: number) {
    jest.advanceTimersByTime(ms);
    await Promise.resolve();
}

export function renderWithAll(ui: React.ReactElement, client?: QueryClient) {
    const queryClient = client ?? createTestClient();
    const i18n = createTestI18n();

    return render(
        <I18nextProvider i18n={i18n}>
            <QueryClientProvider client={queryClient}>
                {ui}
                <ToastContainer theme="dark" />
            </QueryClientProvider>
        </I18nextProvider>
    );
}