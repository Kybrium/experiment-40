import type { Metadata } from "next";
import "./globals.css";
import ConsoleStartup from "@/components/tests/ConsoleStartup";
import Providers from "./providers";

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
      <Providers>
        <body>{children}</body>
      </Providers>
    </html>
  );
}