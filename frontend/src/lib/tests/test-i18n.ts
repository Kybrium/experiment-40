'use client';

import i18next, { i18n as I18nType } from 'i18next';
import { initReactI18next } from 'react-i18next';

import en from '@/i18n/locales/en.json';

export function createTestI18n(): I18nType {
    const instance = i18next.createInstance();

    instance.use(initReactI18next).init({
        resources: {
            en: { translation: en }
        },
        lng: 'en',
        fallbackLng: 'en',
        interpolation: { escapeValue: false }
    });

    return instance;
}