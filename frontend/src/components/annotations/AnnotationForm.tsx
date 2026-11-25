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
    <section className="surface-card space-y-5 p-5 sm:p-6">
      <div>
        <h2 className="text-base font-semibold">Annotation</h2>
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
          Add a construct and the supporting evidence from the transcript.
        </p>
      </div>

      <label className="block space-y-2 text-sm font-medium">
        <span>Construct</span>
        <input
          value={construct}
          onChange={(e) =>
            setConstruct(e.target.value)
          }
          placeholder="e.g. Social support"
          className="w-full px-3 py-2.5"
        />
      </label>

      <label className="block space-y-2 text-sm font-medium">
        <span>Evidence span</span>
        <textarea
          value={evidenceSpan}
          onChange={(e) =>
            setEvidenceSpan(
              e.target.value
            )
          }
          placeholder="Quote the evidence that supports this annotation."
          rows={7}
          className="w-full px-3 py-2.5 text-sm leading-6"
        />
      </label>

      <div className="flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
        <button
          type="button"
          onClick={draft}
          className="min-h-11 rounded-xl border border-border px-4 py-2 text-sm font-medium transition hover:bg-surface-muted"
        >
          Save Draft
        </button>

        <button
          type="button"
          onClick={submit}
          className="button-primary"
        >
          Submit
        </button>
      </div>
    </section>
  );
}