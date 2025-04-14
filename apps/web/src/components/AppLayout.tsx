

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
      <div className="flex w-full">
        <main className="flex-1">{children}</main>
      </div>
  );
}
