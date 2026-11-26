"use client";

import { useParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import {
  useEffect,
  useRef,
  useState,
  type CSSProperties,
  type PointerEvent,
} from "react";

import AnnotationForm from "@/components/annotations/AnnotationForm";
import TranscriptPanel from "@/components/annotations/TranscriptPanel";
import { PageSkeleton } from "@/components/ui/Skeleton";
import { getRecord } from "@/services/records";

export default function AnnotationWorkspacePage() {
  const params = useParams();
  const recordId = params.recordId as string;
  const workspaceRef = useRef<HTMLDivElement>(null);
  const [leftPanelRatio, setLeftPanelRatio] = useState(() => {
    if (typeof window === "undefined") return 56;
    const savedRatio = Number(
      window.localStorage.getItem("annotation-workspace-left-ratio"),
    );
    return Number.isFinite(savedRatio) && savedRatio >= 35 && savedRatio <= 65
      ? savedRatio
      : 56;
  });
  const { data: record, isLoading, isError } = useQuery({
    queryKey: ["record", recordId],
    queryFn: () => getRecord(recordId),
    enabled: Boolean(recordId),
  });

  useEffect(() => {
    window.localStorage.setItem(
      "annotation-workspace-left-ratio",
      String(leftPanelRatio),
    );
  }, [leftPanelRatio]);

  if (isLoading) return <PageSkeleton />;
  if (isError || !record) {
    return (
      <p role="alert" className="surface-card p-5 text-red-700 dark:text-red-300">
        This record could not be loaded or is not assigned to your account.
      </p>
    );
  }

  function resizePanel(event: PointerEvent<HTMLButtonElement>) {
    const bounds = workspaceRef.current?.getBoundingClientRect();
    if (!bounds || bounds.width === 0) return;
    const ratio = ((event.clientX - bounds.left) / bounds.width) * 100;
    setLeftPanelRatio(Math.min(65, Math.max(35, ratio)));
  }

  const workspaceStyle = {
    "--workspace-left": `${leftPanelRatio}fr`,
    "--workspace-right": `${100 - leftPanelRatio}fr`,
  } as CSSProperties;

  return (
    <div className="space-y-4">
      <header className="page-header">
        <h1 className="page-title">{record.record_id}</h1>
        <p className="page-description">
          {record.language} <span aria-hidden="true">·</span> {record.instrument}
          <span aria-hidden="true">·</span> Item {record.item_id}
        </p>
      </header>
      <div
        ref={workspaceRef}
        className="annotation-workspace grid min-h-[65vh] gap-4"
        style={workspaceStyle}
      >
        <TranscriptPanel
          transcript={record.transcript}
          itemText={record.item_text}
          audioLink={record.audio_link}
        />
        <button
          type="button"
          role="separator"
          aria-label="Resize transcript and annotation panels"
          aria-orientation="vertical"
          aria-valuemin={35}
          aria-valuemax={65}
          aria-valuenow={Math.round(leftPanelRatio)}
          onPointerDown={(event) => {
            event.currentTarget.setPointerCapture(event.pointerId);
            resizePanel(event);
          }}
          onPointerMove={(event) => {
            if (event.currentTarget.hasPointerCapture(event.pointerId)) {
              resizePanel(event);
            }
          }}
          onPointerUp={(event) => {
            if (event.currentTarget.hasPointerCapture(event.pointerId)) {
              event.currentTarget.releasePointerCapture(event.pointerId);
            }
          }}
          onKeyDown={(event) => {
            if (event.key === "ArrowLeft") {
              event.preventDefault();
              setLeftPanelRatio((ratio) => Math.max(35, ratio - 2));
            } else if (event.key === "ArrowRight") {
              event.preventDefault();
              setLeftPanelRatio((ratio) => Math.min(65, ratio + 2));
            }
          }}
          className="workspace-resize-handle"
        />
        <AnnotationForm recordId={recordId} />
      </div>
    </div>
  );
}