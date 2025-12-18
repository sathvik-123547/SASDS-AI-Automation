export type ModuleItem = {
  name: string;
  description?: string | null;
};

export type EntityItem = {
  name: string;
  attributes: string[];
};

export type APIItem = {
  name: string;
  method: string;
  path: string;
  description?: string | null;
};

export type RequirementAnalysisResponse = {
  modules: ModuleItem[];
  entities: EntityItem[];
  apis: APIItem[];
  non_functional_requirements: string[];
  tech_stack_suggestions: string[];
  missing_information: string[];
};

export type GeneratedFile = {
  path: string;
  description?: string | null;
  content: string;
};

export type CodeGenerationResponse = {
  files: GeneratedFile[];
};

export type GeneratedTestFile = {
  path: string;
  content: string;
};

export type TestGenerationResponse = {
  tests: GeneratedTestFile[];
};

export type ReviewFile = {
  path: string;
  content: string;
  description?: string | null;
};

export type ReviewIssue = {
  severity: string;
  file?: string | null;
  line?: number | null;
  summary: string;
  recommendation: string;
};

export type CodeReviewResponse = {
  summary: string;
  issues: ReviewIssue[];
};

export type GithubSyncResponse = {
  synced: boolean;
  reason?: string;
  repo?: string;
  branch?: string;
  project_path?: string;
  commit_message?: string;
};

export type ProjectInfo = {
  project_id: string;
  project_path: string;
  created_at: string;
};

export type ProjectsResponse = {
  projects: ProjectInfo[];
};

export type RunLogItem = {
  id: number;
  created_at: string;
  run_id: string | null;
  kind: string;
  note?: string | null;
};

export type RunsResponse = {
  runs: RunLogItem[];
};

