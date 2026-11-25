import { api } from "./api";

export type AnnotationPayload = {
  record_id: string;
  construct: string;
  evidence_span: string;
  frequency:
    | "DAILY"
    | "SEVERAL_DAYS"
    | "MORE_THAN_HALF_THE_DAYS"
    | "NEARLY_EVERY_DAY"
    | "NOT_STATED"
    | "NOT_APPLICABLE";
  cultural_flag?: "NONE" | "PRESENT" | "NEEDS_REVIEW";
  cultural_note?: string | null;
  risk_level: "NONE" | "NEEDS_REVIEW" | "HIGH";
  risk_rationale?: string | null;
};

export type AnnotationResponse = AnnotationPayload & {
  id: string;
  annotator_id: string;
  status: string;
  created_at: string;
  updated_at: string;
};

export async function saveDraft(
  payload: AnnotationPayload
) {
  const response = await api.post<AnnotationResponse>(
    "/annotations/draft",
    payload
  );

  return response.data;
}

export async function submitAnnotation(
  payload: AnnotationPayload
) {
  const response = await api.post<AnnotationResponse>(
    "/annotations/submit",
    payload
  );

  return response.data;
}