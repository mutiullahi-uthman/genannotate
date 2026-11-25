"use client";

import {
  useState,
} from "react";

import { useCreateDataset }
from "@/hooks/useCreateDataset";

export default function CreateDatasetDialog() {
  const [name, setName] =
    useState("");

  const version = "v1";

  const mutation =
    useCreateDataset();

  const handleCreate = () => {
    mutation.mutate({
      name,
      version,
      language_coverage: [
        "ENGLISH",
      ],
    });
  };

  return (
    <div className="mb-6 flex gap-2">
      <input
        value={name}
        onChange={(e) =>
          setName(e.target.value)
        }
        placeholder="Dataset Name"
        className="border p-2"
      />

      <button
        onClick={handleCreate}
        className="rounded bg-black px-4 py-2 text-white"
      >
        Create Dataset
      </button>
    </div>
  );
}