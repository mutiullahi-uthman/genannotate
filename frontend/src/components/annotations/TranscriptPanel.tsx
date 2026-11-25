export default function TranscriptPanel({
  transcript,
}: {
  transcript: string;
}) {
  return (
    <section className="surface-card min-h-64 p-5 sm:p-6">
      <h2 className="mb-4 text-base font-semibold">
        Transcript
      </h2>

      <p className="whitespace-pre-wrap text-sm leading-7 text-slate-700 dark:text-slate-300">
        {transcript}
      </p>
    </section>
  );
}