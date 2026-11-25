export default function TranscriptPanel({
  transcript,
}: {
  transcript: string;
}) {
  return (
    <div className="h-full rounded border p-4">
      <h3 className="mb-4 font-semibold">
        Transcript
      </h3>

      <p>{transcript}</p>
    </div>
  );
}