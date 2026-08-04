interface HeaderProps {
  title?: string;
}

export default function Header({
  title = "Financial Intelligence Dashboard",
}: HeaderProps) {
  return (
    <header className="mb-6">
      <h1 className="text-3xl font-bold text-white">
        {title}
      </h1>

      <p className="text-slate-400 mt-2">
        Real-time market analytics and machine learning predictions
      </p>
    </header>
  );
}