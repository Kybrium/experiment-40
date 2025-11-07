'use client';

import { locales } from '@/lib/constants';
import React from 'react';
import { useTranslation } from 'react-i18next';

const LanguageSwitcher: React.FC = () => {
    const { i18n } = useTranslation();

    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const newLang = e.target.value;
        i18n.changeLanguage(newLang);
        localStorage.setItem('lang', newLang);
    };

    return (
        <div className="relative inline-block">
            <select value={i18n.language} onChange={handleChange} className="input w-auto px-5 py-2 font-mono text-sm border-primary-accent text-primary-accent bg-surface-card/70 rounded-xl cursor-pointer glow-pulse hover:brightness-110 focus:border-primary-accent transition-all duration-200 appearance-none">
                {Object.entries(locales).map(([code, name]) => (
                    <option key={code} value={code} className="bg-surface-card text-text-primary">{name}</option>
                ))}
            </select>

            <div className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-primary-accent">▼</div>
        </div>
    );
};

export default LanguageSwitcher;