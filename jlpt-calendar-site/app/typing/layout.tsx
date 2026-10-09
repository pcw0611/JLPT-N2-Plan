import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'タイピング | JLPT N2 Plan',
  description: '日本語 歌詞・文章タイピング練習',
};

export default function TypingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <script src="/auth-gate.js" />
      {children}
    </>
  );
}
