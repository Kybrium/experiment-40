'use client';

import { locales } from '@/lib/constants';
import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { IoLanguage } from 'react-icons/io5';

interface LanguageSwitcherProps {
    mobile?: boolean;
}

const LanguageSwitcher: React.FC<LanguageSwitcherProps> = ({ mobile = false }) => {
    const { i18n } = useTranslation();
    const [currentLang, setCurrentLang] = useState(i18n.language);
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        const storedLang = localStorage.getItem('lang');
        if (storedLang && storedLang !== i18n.language) {
            i18n.changeLanguage(storedLang);
            setCurrentLang(storedLang);
        } else {
            localStorage.setItem('lang', i18n.language);
            setCurrentLang(i18n.language);
        }
    }, [i18n]);

    const changeLang = (newLang: string) => {
        i18n.changeLanguage(newLang);
        setCurrentLang(newLang);
        localStorage.setItem('lang', newLang);
        setIsOpen(false);
    };

    // Desktop version
    if (!mobile) {
        return (
            <div className="relative inline-block">
                <select
                    value={currentLang}
                    onChange={(e) => changeLang(e.target.value)}
                    className="input !py-1 cursor-pointer bg-surface-card/70 text-primary-accent border-primary-accent rounded-xl hover:brightness-110 transition-all"
                >
                    {Object.entries(locales).map(([code, name]) => (
                        <option key={code} value={code} className="bg-surface-card text-text-primary">
                            {name}
                        </option>
                    ))}
                </select>
            </div>
        );
    }

    // Mobile version
    return (
        <div className="relative">
            <button
                onClick={() => setIsOpen((prev) => !prev)}
                className="flex items-center gap-2 px-3 py-2 rounded-xl border border-primary-accent text-primary-accent bg-surface-card/70 hover:brightness-110 transition-all"
            >
                <IoLanguage className="text-xl" />
                <span className="uppercase font-semibold">{currentLang}</span>
            </button>

            {isOpen && (
                <div className="absolute text-center left-1/2 transform -translate-x-1/2 mt-2 w-32 bg-surface-card border border-primary-accent rounded-xl shadow-lg z-50">
                    {Object.entries(locales).map(([code, name]) => (
                        <button
                            key={code}
                            onClick={() => changeLang(code)}
                            className={`block w-full text-left px-4 py-2 hover:bg-primary-accent/20 transition ${currentLang === code ? 'text-primary-accent font-semibold' : 'text-text-primary'
                                }`}
                        >
                            {name}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
};

export default LanguageSwitcher;