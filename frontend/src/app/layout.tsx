import type { Metadata } from "next";
import "./globals.css";
import ConsoleStartup from "@/components/tests/ConsoleStartup";

export const metadata: Metadata = {
  title: "Experiment 40",
  description: "Minecraft Project",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <ConsoleStartup />
      <body>{children}</body>
    </html>
  );
}