import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'MyGO!!!!! タイピング | JLPT N2 Plan',
  description: 'MyGO!!!!! 歌詞タイピング練習',
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
