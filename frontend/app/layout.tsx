import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "348차원",
  description: "소설 세계관 체험 시스템",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko" className="h-full">
      <body className="min-h-full" style={{ animation: "flicker 8s infinite" }}>
        {children}
      </body>
    </html>
  );
}
