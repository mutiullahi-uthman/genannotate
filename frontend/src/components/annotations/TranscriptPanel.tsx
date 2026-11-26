export default function TranscriptPanel({
  transcript,
  itemText,
  audioLink,
}: {
  transcript: string;
  itemText: string | null;
  audioLink: string | null;
}) {
  return (
    <section className="surface-card min-h-64 p-5 sm:p-6">
      <h2 className="mb-4 text-base font-semibold">
        Transcript
      </h2>

      {itemText && (
        <div className="mb-4 rounded-xl bg-surface-muted p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
            Prompt
          </p>
          <p className="mt-2 whitespace-pre-wrap text-sm leading-6">{itemText}</p>
        </div>
      )}
      <p className="whitespace-pre-wrap text-sm leading-7 text-slate-700 dark:text-slate-300">
        {transcript}
      </p>
      {audioLink && (
        <div className="mt-5 border-t border-border pt-4">
          <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
            Audio
          </p>
          <audio controls preload="none" className="w-full" src={audioLink}>
            Your browser does not support audio playback.
          </audio>
        </div>
      )}
    </section>
  );
}