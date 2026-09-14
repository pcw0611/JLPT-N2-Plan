import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  metadataBase: new URL('http://localhost:3001'),
  title: 'JLPT N2 문법 026~035 확인시험',
  description: '문법 026~035 강의 직후 12문항 확인시험',
  openGraph: {
    title: 'JLPT N2 文法 026〜035 確認試験',
    description: '2026.08.31 · 講義直後 12問',
    type: 'website',
    images: [{ url: '/og.png', width: 1200, height: 630, alt: 'JLPT N2 文法 026〜035 確認試験' }],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'JLPT N2 文法 026〜035 確認試験',
    description: '2026.08.31 · 講義直後 12問',
    images: ['/og.png'],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
