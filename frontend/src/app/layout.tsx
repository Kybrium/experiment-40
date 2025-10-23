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
      <body>
        <ConsoleStartup />
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}