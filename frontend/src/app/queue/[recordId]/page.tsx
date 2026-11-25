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
    <div className="grid min-h-screen grid-cols-2 gap-4">
      <TranscriptPanel
        transcript="Transcript data will render here."
      />

      <AnnotationForm
        recordId={recordId}
      />
    </div>
  );
}