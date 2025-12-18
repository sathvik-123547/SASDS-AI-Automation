import {
  CodeGenerationResponse,
  GeneratedFile,
  GithubSyncResponse,
  RequirementAnalysisResponse,
  ReviewFile,
  CodeReviewResponse,
  TestGenerationResponse,
  ProjectsResponse,
  RunsResponse
} from "../types";

export const API_BASE =
  (import.meta.env.VITE_API_BASE_URL as string) || "http://localhost:8000";

async function apiFetch<T>(path: string, init: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Request to ${path} failed with ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export async function analyzeRequirements(
  requirements_text: string
): Promise<RequirementAnalysisResponse> {
  return apiFetch<RequirementAnalysisResponse>("/requirements/analyze", {
    method: "POST",
    body: JSON.stringify({ requirements_text })
  });
}

export async function generateCode(
  requirements_text: string,
  analysis?: RequirementAnalysisResponse
): Promise<CodeGenerationResponse> {
  return apiFetch<CodeGenerationResponse>("/code/generate", {
    method: "POST",
    body: JSON.stringify({ requirements_text, analysis: analysis ?? null })
  });
}

export async function writeCodeToDisk(
  payload?: CodeGenerationResponse
): Promise<{ message: string; project_id: string; project_path: string }> {
  if (!payload) {
    throw new Error("No generated code to write. Generate code first.");
  }

  return apiFetch("/code/write", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export async function generateTests(
  requirements_text: string,
  files: GeneratedFile[]
): Promise<TestGenerationResponse> {
  return apiFetch<TestGenerationResponse>("/tests/generate", {
    method: "POST",
    body: JSON.stringify({ requirements_text, files })
  });
}

export async function runSelfFix(
  project_path: string,
  max_attempts = 3
): Promise<Record<string, unknown>> {
  return apiFetch<Record<string, unknown>>("/self/fix", {
    method: "POST",
    body: JSON.stringify({ project_path, max_attempts })
  });
}

export async function reviewCode(
  files: ReviewFile[],
  requirements_text?: string
): Promise<CodeReviewResponse> {
  if (!files.length) {
    throw new Error("Provide at least one file to review.");
  }
  return apiFetch<CodeReviewResponse>("/review", {
    method: "POST",
    body: JSON.stringify({ files, requirements_text: requirements_text ?? null })
  });
}

export async function syncGithub(project_path: string, commit_message?: string): Promise<GithubSyncResponse> {
  return apiFetch<GithubSyncResponse>("/github/sync", {
    method: "POST",
    body: JSON.stringify({ project_path, commit_message })
  });
}

export async function listProjects(): Promise<ProjectsResponse> {
  return apiFetch<ProjectsResponse>("/projects", { method: "GET" });
}

export async function listRuns(limit = 50): Promise<RunsResponse> {
  return apiFetch<RunsResponse>(`/runs?limit=${limit}`, { method: "GET" });
}

