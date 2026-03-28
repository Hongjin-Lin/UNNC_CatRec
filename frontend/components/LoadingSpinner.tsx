export default function LoadingSpinner({ text = '加载中…' }: { text?: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-16">
      <div className="w-10 h-10 rounded-full border-4 border-orange-200 border-t-brand animate-spin" />
      <p className="text-sm text-paw-soft">{text}</p>
    </div>
  );
}
