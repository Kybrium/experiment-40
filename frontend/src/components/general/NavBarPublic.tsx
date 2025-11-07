'use client';

import Link from "next/link";
import { usePathname } from "next/navigation";
import { publicNav } from "@/lib/constants";
import LanguageSwitcher from "@/components/general/LanguageSwitcher";
import { useTranslation } from "react-i18next";
import { IoMdMenu } from "react-icons/io";
import React, { useEffect, useState } from "react";
import { AnimatePresence } from "framer-motion";
import { motion } from "framer-motion";

const NavBarPublic: React.FC = () => {
    const pathname = usePathname();
    const { t } = useTranslation('translation', { keyPrefix: 'NavBarPublic' });

    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState<boolean>(false);

    useEffect(() => {
        const handleResize = () => {
            if (window.innerWidth >= 1024) {
                setIsMobileMenuOpen(false);
            }
        };
        window.addEventListener('resize', handleResize);
        if (isMobileMenuOpen) { document.body.style.overflow = 'hidden'; } else { document.body.style.overflow = 'auto'; }
        return () => {
            window.removeEventListener('resize', handleResize);
            document.body.style.overflow = 'auto';
        };
    }, [isMobileMenuOpen])

    return (
        <>
            {/* DESKTOP NAV */}
            <nav className="w-full z-50 sticky top-0 border-b bg-surface-card/85 border-primary-accent/30 lg:flex hidden items-center justify-between px-6 py-3 shadow-[0_0_20px_rgba(157,0,255,0.5)]">
                <Link href={publicNav.home} className="text-2xl font-bold text-primary-accent">
                    <img src='/logo.png' alt='Experiment-40 Logo' className='w-8' />
                </Link>

                {/* NAV LINKS */}
                <div className="flex items-center gap-6">
                    <Link href={publicNav.home} className={`nav-link ${pathname === publicNav.home ? 'text-primary-accent' : 'hover:underline'}`}>
                        {t('home')}
                    </Link>
                    <Link href={publicNav.wiki} className={`nav-link ${pathname === publicNav.wiki ? 'text-primary-accent' : 'hover:underline'}`}>
                        {t('wiki')}
                    </Link>
                    <Link href={publicNav.auth} className={`nav-link ${pathname === publicNav.auth ? 'text-primary-accent' : 'hover:underline'}`}>
                        {t('play')}
                    </Link>
                </div>

                <LanguageSwitcher />
            </nav>

            {/* MOBILE NAV */}
            <nav className="lg:hidden flex w-full z-50 sticky top-0 border-b bg-surface-card/85 border-primary-accent/30 items-center justify-between px-6 py-3 shadow-[0_0_20px_rgba(157,0,255,0.5)]">
                <Link href={publicNav.home} className="text-2xl font-bold text-primary-accent">
                    <img src='/logo.png' alt='Experiment-40 Logo' className='w-8' />
                </Link>
                <IoMdMenu className="text-3xl" onClick={() => setIsMobileMenuOpen((prev) => !prev)} />

            </nav>

            <AnimatePresence>
                {isMobileMenuOpen && (
                    <motion.div
                        className="flex flex-col min-h-screen items-center justify-center fixed inset-0 z-40 bg-surface-card/95"
                        initial={{ y: '-100%' }}
                        animate={{ y: 0 }}
                        exit={{ y: '-100%' }}
                        transition={{ duration: 0.4, ease: 'easeInOut' }}
                    >

                        {/* NAV LINKS */}
                        <div className="flex w-full flex-col items-center justify-center gap-6 min-h-screen">
                            <Link href={publicNav.home} className={`nav-link ${pathname === publicNav.home ? 'bg-primary-accent/80 p-2 w-full text-center' : 'hover:underline'}`}>
                                {t('home')}
                            </Link>
                            <Link href={publicNav.wiki} className={`nav-link ${pathname === publicNav.wiki ? 'bg-primary-accent/80 p-2 w-full text-center' : 'hover:underline'}`}>
                                {t('wiki')}
                            </Link>
                            <Link href={publicNav.auth} className={`nav-link ${pathname === publicNav.auth ? 'bg-primary-accent/80 p-2 w-full text-center' : 'hover:underline'}`}>
                                {t('play')}
                            </Link>
                            <div className="mt-36">
                                <LanguageSwitcher mobile />
                            </div>
                        </div>

                    </motion.div>
                )}
            </AnimatePresence>
        </>
    );
};

export default NavBarPublic;