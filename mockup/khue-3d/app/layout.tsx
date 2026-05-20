import type { Metadata } from "next";
import { Cormorant_Garamond, Be_Vietnam_Pro, Montserrat } from "next/font/google";
import "./globals.css";

const display = Cormorant_Garamond({
  variable: "--font-display",
  weight: ["400", "500", "600", "700"],
  style: ["normal", "italic"],
  subsets: ["latin", "latin-ext", "vietnamese"],
});

const sans = Be_Vietnam_Pro({
  variable: "--font-sans",
  weight: ["300", "400", "500", "600"],
  subsets: ["latin", "latin-ext", "vietnamese"],
});

const montserrat = Montserrat({
  variable: "--font-montserrat",
  weight: ["400", "500", "600", "700", "800"],
  subsets: ["latin", "latin-ext", "vietnamese"],
});

export const metadata: Metadata = {
  title: "Khuê · Văn Miếu — Quốc Tử Giám",
  description: "Sao Khuê toả sáng trên bầu trời văn hiến.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="vi"
      className={`${display.variable} ${sans.variable} ${montserrat.variable}`}
    >
      <body className="bg-ink text-paper antialiased">{children}</body>
    </html>
  );
}
