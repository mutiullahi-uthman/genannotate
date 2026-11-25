"use client";

import { useState } from "react";

import {
  saveDraft,
  submitAnnotation,
} from "@/services/annotations";

export default function AnnotationForm({
  recordId,
}: {
  recordId: string;
}) {
  const [construct, setConstruct] =
    useState("");

  const [evidenceSpan, setEvidenceSpan] =
    useState("");

  async function draft() {
    await saveDraft({
      record_id: recordId,
      construct: construct,
      evidence_span: evidenceSpan,
      frequency: "NOT_STATED",
      risk_level: "NONE",
    });
  }

  async function submit() {
    await submitAnnotation({
      record_id: recordId,
      construct: construct,
      evidence_span: evidenceSpan,
      frequency: "NOT_STATED",
      risk_level: "NONE",
    });
  }

  return (
    <div className="space-y-4 rounded border p-4">
      <h3 className="font-semibold">
        Annotation
      </h3>

      <input
        value={construct}
        onChange={(e) =>
          setConstruct(e.target.value)
        }
        placeholder="Construct"
        className="w-full border p-2"
      />

      <textarea
        value={evidenceSpan}
        onChange={(e) =>
          setEvidenceSpan(
            e.target.value
          )
        }
        rows={6}
        className="w-full border p-2"
      />

      <div className="flex gap-2">
        <button
          onClick={draft}
          className="rounded border px-4 py-2"
        >
          Save Draft
        </button>

        <button
          onClick={submit}
          className="rounded bg-black px-4 py-2 text-white"
        >
          Submit
        </button>
      </div>
    </div>
  );
}