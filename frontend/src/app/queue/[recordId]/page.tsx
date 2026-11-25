"use client";

import { useParams } from "next/navigation";

import AnnotationForm from "@/components/annotations/AnnotationForm";
import TranscriptPanel from "@/components/annotations/TranscriptPanel";

export default function AnnotationWorkspacePage() {
  const params =
    useParams();

  const recordId =
    params.recordId as string;

  return (
    <div className="grid min-h-[65vh] grid-cols-1 gap-4 lg:grid-cols-[minmax(0,1.15fr)_minmax(20rem,0.85fr)]">
      <TranscriptPanel
        transcript="Transcript data will render here."
      />

      <AnnotationForm
        recordId={recordId}
      />
    </div>
  );
}