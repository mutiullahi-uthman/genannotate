"use client";

import { useState, type FormEvent } from "react";
import { toast } from "sonner";
import DataTable, {
  type DataTableColumn,
} from "@/components/ui/DataTable";
import RoleGuard from "@/components/auth/RoleGuard";
import {
  useCodebooks,
  useCreateCodebook,
  useCreateCodebookLabel,
  useDeleteCodebookLabel,
  useUpdateCodebook,
  useUpdateCodebookLabel,
} from "@/hooks/useCodebooks";
import type {
  Codebook,
  CodebookLabel,
} from "@/services/codebooks";

const fieldClass =
  "w-full rounded border border-slate-300 bg-white px-3 py-2 dark:border-slate-700 dark:bg-slate-900";
const buttonClass =
  "rounded-lg bg-slate-900 px-3 py-2 text-sm font-medium text-white disabled:opacity-50 dark:bg-white dark:text-slate-900";

export default function CodebooksPage() {
  const { data: codebooks, isLoading, isError } = useCodebooks();
  const createCodebook = useCreateCodebook();
  const [name, setName] = useState("");
  const [version, setVersion] = useState("");

  function submitCodebook(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    createCodebook.mutate(
      { name, version },
      {
        onSuccess: () => {
          setName("");
          setVersion("");
          toast.success("Codebook created.");
        },
      },
    );
  }

  const columns: DataTableColumn<Codebook>[] = [
    {
      key: "name",
      header: "Codebook",
      render: (book) => (
        <CodebookEditor
          key={`${book.id}-${book.name}-${book.version}`}
          codebook={book}
          onSaved={() => toast.success("Codebook updated.")}
        />
      ),
    },
    {
      key: "version",
      header: "Version",
      render: (book) => book.version,
    },
    {
      key: "status",
      header: "Status",
      render: (book) => (
        <CodebookStatusControl
          codebook={book}
          onSaved={() => toast.success("Codebook status updated.")}
        />
      ),
    },
    {
      key: "labels",
      header: "Labels",
      render: (book) => (
        <CodebookLabels
          codebook={book}
          onSaved={() => toast.success("Codebook labels updated.")}
        />
      ),
    },
  ];

  return (
    <RoleGuard roles={["ADMIN", "SUPERVISOR", "RESEARCH_LEAD"]}>
      <div className="space-y-6">
        <header>
          <h1 className="text-3xl font-bold">Codebook management</h1>
          <p className="mt-2 text-sm text-slate-500">
            Create codebooks, maintain their label definitions, and publish versions.
          </p>
        </header>

        <form
          onSubmit={submitCodebook}
          className="grid gap-3 rounded-lg border border-slate-200 p-4 sm:grid-cols-[1fr_12rem_auto] dark:border-slate-700"
        >
          <label className="space-y-1 text-sm">
            <span>Codebook name</span>
            <input
              required
              maxLength={255}
              value={name}
              onChange={(event) => setName(event.target.value)}
              className={fieldClass}
            />
          </label>
          <label className="space-y-1 text-sm">
            <span>Version</span>
            <input
              required
              maxLength={50}
              value={version}
              onChange={(event) => setVersion(event.target.value)}
              className={fieldClass}
            />
          </label>
          <button
            type="submit"
            disabled={createCodebook.isPending}
            className={`${buttonClass} self-end`}
          >
            {createCodebook.isPending ? "Creating…" : "Create codebook"}
          </button>
        </form>

        <DataTable
          rows={codebooks}
          columns={columns}
          rowKey={(book) => book.id}
          isLoading={isLoading}
          hasError={isError}
          emptyMessage="No codebooks yet. Create one to get started."
        />
      </div>
    </RoleGuard>
  );
}

function CodebookEditor({
  codebook,
  onSaved,
}: {
  codebook: Codebook;
  onSaved: () => void;
}) {
  const update = useUpdateCodebook();
  const [name, setName] = useState(codebook.name);
  const [version, setVersion] = useState(codebook.version);
  const editable = codebook.status === "DRAFT";

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    update.mutate(
      { codebookId: codebook.id, name, version },
      { onSuccess: onSaved },
    );
  }

  return (
    <details className="min-w-52">
      <summary className="cursor-pointer font-medium">{codebook.name}</summary>
      {editable && (
        <form onSubmit={submit} className="mt-3 space-y-2">
          <label className="block space-y-1 text-xs">
            <span>Name</span>
            <input
              required
              value={name}
              onChange={(event) => setName(event.target.value)}
              className={fieldClass}
            />
          </label>
          <label className="block space-y-1 text-xs">
            <span>Version</span>
            <input
              required
              value={version}
              onChange={(event) => setVersion(event.target.value)}
              className={fieldClass}
            />
          </label>
          <button className={buttonClass} disabled={update.isPending}>
            Save details
          </button>
        </form>
      )}
    </details>
  );
}

function CodebookStatusControl({
  codebook,
  onSaved,
}: {
  codebook: Codebook;
  onSaved: () => void;
}) {
  const update = useUpdateCodebook();
  return (
    <select
      aria-label={`Status for ${codebook.name}`}
      value={codebook.status}
      disabled={update.isPending || codebook.status === "ARCHIVED"}
      onChange={(event) =>
        update.mutate(
          {
            codebookId: codebook.id,
            status: event.target.value as Codebook["status"],
          },
          { onSuccess: onSaved },
        )
      }
      className="rounded border border-slate-300 bg-white px-2 py-1 dark:border-slate-700 dark:bg-slate-900"
    >
      <option value="DRAFT" disabled={codebook.status !== "DRAFT"}>
        Draft
      </option>
      <option
        value="PUBLISHED"
        disabled={
          codebook.status === "ARCHIVED" ||
          codebook.labels.length === 0
        }
      >
        Published
      </option>
      <option value="ARCHIVED">Archived</option>
    </select>
  );
}

function CodebookLabels({
  codebook,
  onSaved,
}: {
  codebook: Codebook;
  onSaved: () => void;
}) {
  const [labelName, setLabelName] = useState("");
  const [definition, setDefinition] = useState("");
  const create = useCreateCodebookLabel();
  const editable = codebook.status === "DRAFT";

  function addLabel(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    create.mutate(
      { codebookId: codebook.id, label_name: labelName, definition },
      {
        onSuccess: () => {
          setLabelName("");
          setDefinition("");
          onSaved();
        },
      },
    );
  }

  return (
    <details className="min-w-52">
      <summary className="cursor-pointer">
        {codebook.labels.length} label{codebook.labels.length === 1 ? "" : "s"}
      </summary>
      <div className="mt-3 space-y-3">
        {codebook.labels.map((label) => (
          <LabelEditor
            key={`${label.id}-${label.label_name}-${label.definition}`}
            codebookId={codebook.id}
            label={label}
            editable={editable}
            onSaved={onSaved}
          />
        ))}
        {editable && (
          <form onSubmit={addLabel} className="space-y-2 border-t pt-3 dark:border-slate-700">
            <input
              required
              maxLength={255}
              placeholder="Label name"
              value={labelName}
              onChange={(event) => setLabelName(event.target.value)}
              className={fieldClass}
            />
            <textarea
              required
              placeholder="Definition"
              value={definition}
              onChange={(event) => setDefinition(event.target.value)}
              className={fieldClass}
              rows={2}
            />
            <button className={buttonClass} disabled={create.isPending}>
              Add label
            </button>
          </form>
        )}
      </div>
    </details>
  );
}

function LabelEditor({
  codebookId,
  label,
  editable,
  onSaved,
}: {
  codebookId: string;
  label: CodebookLabel;
  editable: boolean;
  onSaved: () => void;
}) {
  const update = useUpdateCodebookLabel();
  const remove = useDeleteCodebookLabel();
  const [labelName, setLabelName] = useState(label.label_name);
  const [definition, setDefinition] = useState(label.definition);

  if (!editable) {
    return (
      <div className="rounded bg-slate-50 p-2 dark:bg-slate-800">
        <p className="font-medium">{label.label_name}</p>
        <p className="mt-1 whitespace-pre-wrap text-xs text-slate-600 dark:text-slate-300">
          {label.definition}
        </p>
      </div>
    );
  }

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        update.mutate(
          { codebookId, labelId: label.id, label_name: labelName, definition },
          { onSuccess: onSaved },
        );
      }}
      className="space-y-2 rounded bg-slate-50 p-2 dark:bg-slate-800"
    >
      <input
        required
        value={labelName}
        onChange={(event) => setLabelName(event.target.value)}
        className={fieldClass}
      />
      <textarea
        required
        value={definition}
        onChange={(event) => setDefinition(event.target.value)}
        className={fieldClass}
        rows={2}
      />
      <div className="flex gap-2">
        <button className={buttonClass} disabled={update.isPending}>
          Save
        </button>
        <button
          type="button"
          disabled={remove.isPending}
          onClick={() =>
            remove.mutate(
              { codebookId, labelId: label.id },
              { onSuccess: onSaved },
            )
          }
          className="rounded-lg border border-red-300 px-3 py-2 text-sm text-red-700 dark:border-red-800 dark:text-red-300"
        >
          Delete
        </button>
      </div>
    </form>
  );
}
