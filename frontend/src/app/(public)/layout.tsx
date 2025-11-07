'use client';

import NavBarPublic from "@/components/general/NavBarPublic";

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <>
            <NavBarPublic />
            {children}
        </>
    );
}