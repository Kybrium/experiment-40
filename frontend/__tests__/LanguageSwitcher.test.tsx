import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import LanguageSwitcher from '@/components/general/LanguageSwitcher';

// ---- Mocks ----
jest.mock('@/lib/constants', () => ({
    locales: { en: 'English', uk: 'Українська' },
}));

let mockI18n: { language: string; changeLanguage: jest.Mock };

jest.mock('react-i18next', () => ({
    useTranslation: () => ({ i18n: mockI18n }),
}));

describe('LanguageSwitcher', () => {
    const user = userEvent.setup();

    beforeEach(() => {
        mockI18n = {
            language: 'en',
            changeLanguage: jest.fn(),
        };
        localStorage.clear();
        jest.clearAllMocks();
    });

    describe('Desktop mode (default)', () => {
        test('renders a <select> with options from locales and initial value from i18n.language', () => {
            render(<LanguageSwitcher />);

            expect(screen.getByRole('option', { name: 'English' })).toBeInTheDocument();
            expect(screen.getByRole('option', { name: 'Українська' })).toBeInTheDocument();

            const select = screen.getByRole('combobox') as HTMLSelectElement;
            expect(select.value).toBe('en');
        });

        test('on first mount without stored lang, writes i18n.language to localStorage', async () => {
            render(<LanguageSwitcher />);
            await waitFor(() => {
                expect(localStorage.getItem('lang')).toBe('en');
            });
        });

        test('if stored lang differs, switches i18n and updates select value', async () => {
            localStorage.setItem('lang', 'uk');
            render(<LanguageSwitcher />);

            await waitFor(() => {
                expect(mockI18n.changeLanguage).toHaveBeenCalledWith('uk');
            });

            const select = screen.getByRole('combobox') as HTMLSelectElement;
            await waitFor(() => expect(select.value).toBe('uk'));
        });

        test('changing the select calls i18n.changeLanguage, updates localStorage and value', async () => {
            render(<LanguageSwitcher />);

            const select = screen.getByRole('combobox');
            await user.selectOptions(select, 'uk');

            expect(mockI18n.changeLanguage).toHaveBeenCalledWith('uk');
            expect(localStorage.getItem('lang')).toBe('uk');

            await waitFor(() => {
                const el = screen.getByRole('combobox') as HTMLSelectElement;
                expect(el.value).toBe('uk');
            });
        });
    });

    describe('Mobile mode', () => {
        test('renders a button with current language code (uppercase) and toggles the menu', async () => {
            render(<LanguageSwitcher mobile />);

            expect(screen.getByRole('button', { name: /EN/i })).toBeInTheDocument();

            expect(screen.queryByRole('button', { name: 'English' })).not.toBeInTheDocument();

            await user.click(screen.getByRole('button', { name: /EN/i }));
            expect(screen.getByRole('button', { name: 'English' })).toBeInTheDocument();
            expect(screen.getByRole('button', { name: 'Українська' })).toBeInTheDocument();
        });

        test('clicking a language changes i18n, persists to localStorage, updates button, and closes menu', async () => {
            render(<LanguageSwitcher mobile />);

            await user.click(screen.getByRole('button', { name: /EN/i }));

            await user.click(screen.getByRole('button', { name: 'Українська' }));

            expect(mockI18n.changeLanguage).toHaveBeenCalledWith('uk');
            expect(localStorage.getItem('lang')).toBe('uk');

            await waitFor(() => {
                expect(screen.queryByRole('button', { name: 'English' })).not.toBeInTheDocument();
            });

            expect(screen.getByRole('button', { name: /UK/i })).toBeInTheDocument();
        });

        test('highlights the currently active language option', async () => {
            mockI18n.language = 'uk';
            render(<LanguageSwitcher mobile />);

            await user.click(screen.getByRole('button', { name: /UK/i }));

            const active = screen.getByRole('button', { name: 'Українська' });

            expect(active.className).toMatch(/text-primary-accent/);
            expect(active.className).toMatch(/font-semibold/);

            const inactive = screen.getByRole('button', { name: 'English' });
            expect(inactive.className).not.toMatch(/text-primary-accent/);
        });

        test('on first mount without stored lang, writes i18n.language to localStorage', async () => {
            render(<LanguageSwitcher mobile />);
            await waitFor(() => {
                expect(localStorage.getItem('lang')).toBe('en');
            });
        });

        test('if stored lang differs, switches i18n and updates button label', async () => {
            localStorage.setItem('lang', 'uk');
            render(<LanguageSwitcher mobile />);

            await waitFor(() => {
                expect(mockI18n.changeLanguage).toHaveBeenCalledWith('uk');
            });

            expect(screen.getByRole('button', { name: /UK/i })).toBeInTheDocument();
        });
    });
});