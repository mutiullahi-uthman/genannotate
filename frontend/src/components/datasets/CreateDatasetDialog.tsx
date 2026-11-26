"use client";

import { useState, type FormEvent } from "react";
import { Plus } from "lucide-react";
import { toast } from "sonner";
import { useCreateDataset } from "@/hooks/useCreateDataset";

export default function CreateDatasetDialog() {
  const [name, setName] = useState("");
  const mutation = useCreateDataset();

  function handleCreate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    mutation.mutate(
      { name: name.trim(), language_coverage: ["ENGLISH"] },
      {
        onSuccess: () => {
          setName("");
          toast.success("Dataset created.");
        },
      },
    );
  }

  return (
    <form
      onSubmit={handleCreate}
      className="flex w-full flex-col gap-2 sm:w-auto sm:flex-row"
    >
      <input
        required
        maxLength={255}
        value={name}
        onChange={(event) => setName(event.target.value)}
        placeholder="Name your dataset"
        aria-label="Dataset name"
        className="h-11 min-w-0 flex-1 px-3 text-sm sm:w-56"
      />
      <button
        type="submit"
        disabled={mutation.isPending}
        className="button-primary w-full sm:w-auto"
      >
        <Plus size={17} aria-hidden="true" />
        {mutation.isPending ? "Creating…" : "New dataset"}
      </button>
    </form>
  );
}