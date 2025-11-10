"use client";

import { AnimatePresence, motion } from "framer-motion";
import StarsBg from "@/components/bg/StarsBg";
import LoginModal from "@/components/auth/LoginModal";
import RegistrationModal from "@/components/auth/RegistrationModal";
import { useEffect, useState } from "react";
import { useCurrentUser } from "@/hooks/useCurrentUser";
import { useRouter } from "next/navigation";

export default function Auth() {
    const [isLogin, setIsLogin] = useState(true);
    const router = useRouter();
    const { hasCachedUser } = useCurrentUser({ skip: true });

    useEffect(() => {
        if (hasCachedUser()) {
            router.replace("/dashboard");
        }
    }, [hasCachedUser, router]);

    return (
        <main className="relative min-h-screen centered-display py-8 overflow-hidden">
            <StarsBg />

            <AnimatePresence mode="wait">
                {!isLogin && (
                    <motion.div
                        key="register"
                        initial={{ opacity: 0, y: 40, scale: 0.97 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: -40, scale: 0.97 }}
                        transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
                        className="absolute z-10 w-full centered-display"
                    >
                        <RegistrationModal setIsLogin={setIsLogin} />
                    </motion.div>
                )}

                {isLogin && (
                    <motion.div
                        key="login"
                        initial={{ opacity: 0, y: 40, scale: 0.97 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: -40, scale: 0.97 }}
                        transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
                        className="absolute z-10 w-full centered-display"
                    >
                        <LoginModal setIsLogin={setIsLogin} />
                    </motion.div>
                )}
            </AnimatePresence>
        </main>
    );
}