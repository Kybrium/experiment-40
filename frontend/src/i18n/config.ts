'use client';

import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

import en from './locales/en.json';
import uk from './locales/uk.json';


const DEFAULT_LANG = 'uk';
const SUPPORTED_LANGS = ['en', 'uk'] as const;

let savedLang: string | null = null;
if (typeof window !== 'undefined') {
    savedLang = localStorage.getItem('lang');

    if (!savedLang || !SUPPORTED_LANGS.includes(savedLang as any)) {
        localStorage.setItem('lang', DEFAULT_LANG);
        savedLang = DEFAULT_LANG;
    }
}

i18n.use(initReactI18next).init({
    resources: {
        en: { translation: en },
        uk: { translation: uk },
    },
    lng: savedLang ?? DEFAULT_LANG,
    fallbackLng: DEFAULT_LANG,
    interpolation: { escapeValue: false },
});

if (savedLang && savedLang !== i18n.language) {
    i18n.changeLanguage(savedLang);
}

export default i18n;