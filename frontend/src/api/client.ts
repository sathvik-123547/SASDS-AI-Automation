import {
  CodeGenerationResponse,
  GeneratedFile,
  GithubSyncResponse,
  RequirementAnalysisResponse,
  ReviewFile,
  CodeReviewResponse,
  TestGenerationResponse,
  ProjectsResponse,
  RunsResponse,
  RefinementResponse,
  AutoPilotResponse
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

export async function generateCodeStream(
  requirements_text: string,
  analysis: RequirementAnalysisResponse | undefined,
  onChunk: (chunk: string) => void
): Promise<void> {
  const response = await fetch(`${API_BASE}/code/generate/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ requirements_text, analysis: analysis ?? null })
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with ${response.status}`);
  }

  const reader = response.body?.getReader();
  if (!reader) throw new Error("No response body");

  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    onChunk(decoder.decode(value, { stream: true }));
  }
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
export async function refineCode(
  path: string,
  content: string,
  instructions: string
): Promise<RefinementResponse> {
  return apiFetch<RefinementResponse>("/refine/", {
    method: "POST",
    body: JSON.stringify({ path, content, instructions })
  });
}

export async function createFile(
  path: string,
  content: string = "",
  is_directory: boolean = false
): Promise<{ message: string }> {
  return apiFetch<{ message: string }>("/files/create", {
    method: "POST",
    body: JSON.stringify({ path, content, is_directory })
  });
}

export async function deleteFile(path: string): Promise<{ message: string }> {
  return apiFetch<{ message: string }>("/files/delete", {
    method: "DELETE",
    body: JSON.stringify({ path })
  });
}

export async function renameFile(
  old_path: string,
  new_path: string
): Promise<{ message: string }> {
  return apiFetch<{ message: string }>("/files/rename", {
    method: "PUT",
    body: JSON.stringify({ old_path, new_path })
  });
}

export async function runAutoPilot(project_id: string): Promise<AutoPilotResponse> {
  return apiFetch<AutoPilotResponse>("/autopilot/analyze", {
    method: "POST",
    body: JSON.stringify({ project_id })
  });
}

export type ChatMessage = {
  role: "user" | "model";
  content: string;
};

export async function sendChatMessage(
  message: string,
  history: ChatMessage[],
  context?: { selected_file_path?: string, selected_file_content?: string, project_structure?: string }
): Promise<ChatMessage> {
  return apiFetch<ChatMessage>("/chat/send", {
    method: "POST",
    body: JSON.stringify({ message, history, context })
  });
}
