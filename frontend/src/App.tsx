import { useEffect, useMemo, useState, type ReactNode } from "react";
import {
  analyzeRequirements,
  generateCode,
  generateTests,
  runSelfFix,
  writeCodeToDisk,
  reviewCode,
  syncGithub,
  listProjects,
  listRuns,
  API_BASE
} from "./api/client";
import {
  CodeGenerationResponse,
  RequirementAnalysisResponse,
  TestGenerationResponse,
  CodeReviewResponse,
  ProjectsResponse,
  RunsResponse
} from "./types";

type LoadState = "idle" | "loading" | "error" | "success";

function StepBadge({ step }: { step: number }) {
  return <span className="step-badge">Step {step}</span>;
}

function Section(props: {
  id?: string;
  step: number;
  title: string;
  description?: string;
  children: ReactNode;
}) {
  return (
    <section className="card" id={props.id}>
      <header className="card__header">
        <div className="card__title-wrap">
          <StepBadge step={props.step} />
          <div>
            <p className="eyebrow small">workflow</p>
            <h2>{props.title}</h2>
          </div>
        </div>
      </header>
      {props.description ? (
        <p className="card__description">{props.description}</p>
      ) : null}
      <div className="card__body">{props.children}</div>
    </section>
  );
}

function JsonBlock<T>({ data }: { data: T | undefined }) {
  if (!data) return null;
  return <pre className="json-block">{JSON.stringify(data, null, 2)}</pre>;
}

export default function App() {
  const [backendStatus, setBackendStatus] = useState<string>("Checking...");

  const [requirementsText, setRequirementsText] = useState<string>(
    "Build a simple task manager API with projects and tasks."
  );

  const [analysisResult, setAnalysisResult] = useState<RequirementAnalysisResponse>();
  const [analysisState, setAnalysisState] = useState<LoadState>("idle");
  const [analysisError, setAnalysisError] = useState<string>("");

  const [codeResult, setCodeResult] = useState<CodeGenerationResponse>();
  const [codeState, setCodeState] = useState<LoadState>("idle");
  const [codeError, setCodeError] = useState<string>("");

  const [testsResult, setTestsResult] = useState<TestGenerationResponse>();
  const [testsState, setTestsState] = useState<LoadState>("idle");
  const [testsError, setTestsError] = useState<string>("");

  const [writeState, setWriteState] = useState<LoadState>("idle");
  const [writeMessage, setWriteMessage] = useState<string>("");
  const [writeError, setWriteError] = useState<string>("");
  const [lastProjectId, setLastProjectId] = useState<string>("");
  const [lastProjectPath, setLastProjectPath] = useState<string>("");

  const [reviewState, setReviewState] = useState<LoadState>("idle");
  const [reviewError, setReviewError] = useState<string>("");
  const [reviewResult, setReviewResult] = useState<CodeReviewResponse>();

  const [githubState, setGithubState] = useState<LoadState>("idle");
  const [githubMsg, setGithubMsg] = useState<string>("");
  const [githubError, setGithubError] = useState<string>("");

  const [selfFixPath, setSelfFixPath] = useState<string>("generated_projects");
  const [selfFixAttempts, setSelfFixAttempts] = useState<number>(3);
  const [selfFixState, setSelfFixState] = useState<LoadState>("idle");
  const [selfFixResult, setSelfFixResult] = useState<Record<string, unknown>>();
  const [selfFixError, setSelfFixError] = useState<string>("");

  const [projectsState, setProjectsState] = useState<LoadState>("idle");
  const [projectsData, setProjectsData] = useState<ProjectsResponse>();
  const [projectsError, setProjectsError] = useState<string>("");

  const [runsState, setRunsState] = useState<LoadState>("idle");
  const [runsData, setRunsData] = useState<RunsResponse>();
  const [runsError, setRunsError] = useState<string>("");

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"}/ping`)
      .then((res) => {
        if (!res.ok) throw new Error("Unavailable");
        return res.json();
      })
      .then((data) => setBackendStatus(data.message || "OK"))
      .catch(() =>
        setBackendStatus("Backend is not reachable. Is it running on port 8000?")
      );
  }, []);

  const generatedFilesPreview = useMemo(() => {
    if (!codeResult?.files?.length) return "No files generated yet.";
    return codeResult.files
      .map((f, idx) => `${idx + 1}. ${f.path}${f.description ? ` – ${f.description}` : ""}`)
      .join("\n");
  }, [codeResult]);

  async function onAnalyzeRequirements() {
    setAnalysisState("loading");
    setAnalysisError("");
    try {
      const result = await analyzeRequirements(requirementsText);
      setAnalysisResult(result);
      setAnalysisState("success");
    } catch (err) {
      setAnalysisState("error");
      setAnalysisError(
        err instanceof Error ? err.message : "Failed to analyze requirements."
      );
    }
  }

  async function onGenerateCode() {
    setCodeState("loading");
    setCodeError("");
    try {
      const result = await generateCode(requirementsText, analysisResult);
      setCodeResult(result);
      setCodeState("success");
    } catch (err) {
      setCodeState("error");
      setCodeError(err instanceof Error ? err.message : "Failed to generate code.");
    }
  }

  async function onGenerateTests() {
    setTestsState("loading");
    setTestsError("");
    try {
      const files = codeResult?.files ?? [];
      const result = await generateTests(requirementsText, files);
      setTestsResult(result);
      setTestsState("success");
    } catch (err) {
      setTestsState("error");
      setTestsError(err instanceof Error ? err.message : "Failed to generate tests.");
    }
  }

  async function onWriteCode() {
    setWriteState("loading");
    setWriteError("");
    setWriteMessage("");
    try {
      const response = await writeCodeToDisk(codeResult);
      setWriteMessage(
        `Project saved at ${response.project_path} (id: ${response.project_id})`
      );
      setLastProjectId(response.project_id);
      setLastProjectPath(response.project_path);
      setWriteState("success");
    } catch (err) {
      setWriteState("error");
      setWriteError(err instanceof Error ? err.message : "Failed to write code to disk.");
    }
  }

  async function onReviewCode() {
    setReviewState("loading");
    setReviewError("");
    try {
      const files =
        (codeResult?.files ?? []).map((f) => ({
          path: f.path,
          content: f.content,
          description: f.description ?? undefined
        })) ?? [];

      const testFiles =
        (testsResult?.tests ?? []).map((t) => ({
          path: t.path,
          content: t.content,
          description: "Generated test"
        })) ?? [];

      const allFiles = [...files, ...testFiles];
      if (!allFiles.length) {
        throw new Error("Generate code or tests first to run a review.");
      }

      const result = await reviewCode(allFiles, requirementsText);
      setReviewResult(result);
      setReviewState("success");
    } catch (err) {
      setReviewState("error");
      setReviewError(err instanceof Error ? err.message : "Review failed.");
    }
  }

  async function onSyncGithub() {
    setGithubState("loading");
    setGithubError("");
    setGithubMsg("");
    try {
      const result = await syncGithub(selfFixPath, "Sync generated project");
      setGithubState("success");
      setGithubMsg(result.reason || (result.synced ? "Synced" : "Completed"));
    } catch (err) {
      setGithubState("error");
      setGithubError(err instanceof Error ? err.message : "GitHub sync failed.");
    }
  }

  async function onRunSelfFix() {
    setSelfFixState("loading");
    setSelfFixError("");
    try {
      const result = await runSelfFix(selfFixPath, selfFixAttempts);
      setSelfFixResult(result);
      setSelfFixState("success");
    } catch (err) {
      setSelfFixState("error");
      setSelfFixError(err instanceof Error ? err.message : "Self-correction failed.");
    }
  }

  async function onLoadProjects() {
    setProjectsState("loading");
    setProjectsError("");
    try {
      const res = await listProjects();
      setProjectsData(res);
      setProjectsState("success");
    } catch (err) {
      setProjectsState("error");
      setProjectsError(err instanceof Error ? err.message : "Failed to load projects.");
    }
  }

  async function onLoadRuns() {
    setRunsState("loading");
    setRunsError("");
    try {
      const res = await listRuns(50);
      setRunsData(res);
      setRunsState("success");
    } catch (err) {
      setRunsState("error");
      setRunsError(err instanceof Error ? err.message : "Failed to load runs.");
    }
  }

  return (
    <div className="page">
      <header className="topbar">
        <div className="brand">
          <div className="logo-dot" />
          <div>
            <p className="eyebrow">SASDS</p>
            <strong>Single Agent SDS</strong>
          </div>
        </div>
        <nav className="nav">
          <a href="#requirements">Requirements</a>
          <a href="#code-generation">Code</a>
          <a href="#tests">Tests</a>
          <a href="#self-correction">Self-Fix</a>
          <a href="#review">Review</a>
          <a href="#projects">Projects</a>
          <a href="#runs">History</a>
          <a href="#github">Sync</a>
        </nav>
        <div className="status">
          <span className="badge">Backend</span>
          <span>{backendStatus}</span>
        </div>
      </header>

      <section className="hero">
        <div className="hero__content">
          <div className="eyebrow">Production-ready AI Delivery</div>
          <h1>
            Build, test, review, and ship with a single autonomous agent.
          </h1>
          <p className="subtitle">
            Analyze requirements, generate code, create tests, self-correct failures, and
            review quality—all in one streamlined experience.
          </p>
          <div className="actions">
            <button onClick={onAnalyzeRequirements} disabled={analysisState === "loading"}>
              {analysisState === "loading" ? "Analyzing..." : "Analyze Now"}
            </button>
            <button
              className="secondary"
              onClick={() => {
                const el = document.getElementById("code-generation");
                if (el) el.scrollIntoView({ behavior: "smooth" });
              }}
            >
              Jump to Code
            </button>
          </div>
          <div className="statbar">
            <div className="stat">
              <span className="stat__label">Auto Tests</span>
              <span className="stat__value">Pytest suites</span>
            </div>
            <div className="stat">
              <span className="stat__label">Self-heal</span>
              <span className="stat__value">LLM-powered fixes</span>
            </div>
            <div className="stat">
              <span className="stat__label">Reviews</span>
              <span className="stat__value">Structured issues</span>
            </div>
          </div>
        </div>
        <div className="hero__panel">
          <div className="panel">
            <div className="panel__title">Pipeline</div>
            <ul className="timeline">
              <li>Analyze requirements</li>
              <li>Generate code</li>
              <li>Generate tests</li>
              <li>Self-correct failures</li>
              <li>Review & ship</li>
            </ul>
            <div className="panel__status">
              <span className="badge">Backend</span>
              <span>{backendStatus}</span>
            </div>
          </div>
        </div>
      </section>

      <main className="layout">
        <div className="flow">
          <Section
            id="requirements"
            step={1}
            title="Requirements Intake"
            description="Capture the vision. Analyze natural language and derive structured modules, entities, APIs, and gaps."
          >
            <label className="label">
              Requirements Text
              <textarea
                value={requirementsText}
                onChange={(e) => setRequirementsText(e.target.value)}
                rows={6}
                placeholder="Describe the project requirements..."
              />
            </label>
            <div className="actions">
              <button onClick={onAnalyzeRequirements} disabled={analysisState === "loading"}>
                {analysisState === "loading" ? "Analyzing..." : "Analyze Requirements"}
              </button>
              {analysisState === "error" && <span className="error">{analysisError}</span>}
            </div>
            <JsonBlock data={analysisResult} />
          </Section>

          <Section
            id="code-generation"
            step={2}
            title="Code Generation"
            description="Generate FastAPI projects with structured files, then persist them to disk."
          >
            <p className="hint">
              Uses the requirements (and optional analysis) to generate project files.
            </p>
            <div className="actions">
              <button onClick={onGenerateCode} disabled={codeState === "loading"}>
                {codeState === "loading" ? "Generating..." : "Generate Code"}
              </button>
              {codeState === "error" && <span className="error">{codeError}</span>}
            </div>
            <label className="label">
              Generated Files (summary)
              <textarea value={generatedFilesPreview} readOnly rows={6} />
            </label>
            <JsonBlock data={codeResult} />
            {codeResult?.files?.length ? (
              <div className="actions">
                <button onClick={onWriteCode} disabled={writeState === "loading"}>
                  {writeState === "loading" ? "Saving..." : "Write to Disk"}
                </button>
                {writeState === "error" && <span className="error">{writeError}</span>}
                {writeState === "success" && <span className="success">{writeMessage}</span>}
              </div>
            ) : null}
          </Section>

          <Section
            id="tests"
            title="Test Generation"
            description="Create pytest suites from requirements and generated code."
            step={3}
          >
            <p className="hint">
              Provide requirements and the generated files to create pytest suites.
            </p>
            <div className="actions">
              <button
                onClick={onGenerateTests}
                disabled={testsState === "loading" || !codeResult?.files?.length}
                title={!codeResult?.files?.length ? "Generate code first" : ""}
              >
                {testsState === "loading" ? "Generating..." : "Generate Tests"}
              </button>
              {testsState === "error" && <span className="error">{testsError}</span>}
            </div>
            <JsonBlock data={testsResult} />
          </Section>

          <Section
            id="self-correction"
            title="Self Correction"
            description="Run pytest, detect failing files, and loop fixes with Gemini until green."
            step={4}
          >
            <p className="hint">
              Point at a generated project folder (after writing code to disk) to run the
              self-correction loop.
            </p>
            <div className="form-grid">
              <label className="label">
                Project Path
                <input
                  value={selfFixPath}
                  onChange={(e) => setSelfFixPath(e.target.value)}
                  placeholder="generated_projects/project_xxxx"
                />
              </label>
              <label className="label">
                Max Attempts
                <input
                  type="number"
                  min={1}
                  max={10}
                  value={selfFixAttempts}
                  onChange={(e) => setSelfFixAttempts(Number(e.target.value))}
                />
              </label>
            </div>
            <div className="actions">
              <button onClick={onRunSelfFix} disabled={selfFixState === "loading"}>
                {selfFixState === "loading" ? "Running..." : "Run Self-Correction"}
              </button>
              {selfFixState === "error" && <span className="error">{selfFixError}</span>}
            </div>
            <JsonBlock data={selfFixResult} />
          </Section>

          <Section
            id="review"
            title="Code Review"
            description="LLM-assisted review for readability, correctness, security, and best practices."
            step={5}
          >
            <div className="actions">
              <button
                onClick={onReviewCode}
                disabled={
                  reviewState === "loading" ||
                  (!codeResult?.files?.length && !testsResult?.tests?.length)
                }
                title={
                  !codeResult?.files?.length && !testsResult?.tests?.length
                    ? "Generate code/tests first"
                    : ""
                }
              >
                {reviewState === "loading" ? "Reviewing..." : "Run Code Review"}
              </button>
              {reviewState === "error" && <span className="error">{reviewError}</span>}
            </div>
            {reviewResult && (
              <>
                <p className="hint">{reviewResult.summary}</p>
                <JsonBlock data={reviewResult} />
              </>
            )}
          </Section>

          <Section
            id="projects"
            title="Generated Projects"
            description="Browse generated projects, set one for self-fix, or download an archive."
            step={6}
          >
            <div className="actions">
              <button onClick={onLoadProjects} disabled={projectsState === "loading"}>
                {projectsState === "loading" ? "Loading..." : "Refresh List"}
              </button>
              {projectsState === "error" && <span className="error">{projectsError}</span>}
            </div>
            {projectsData?.projects?.length ? (
              <ul className="list">
                {projectsData.projects.map((p) => (
                  <li key={p.project_id} className="list-item">
                    <div>
                      <div className="list-title">{p.project_id}</div>
                      <div className="list-subtitle">{p.project_path}</div>
                      <div className="list-meta">Created: {p.created_at}</div>
                    </div>
                    <div className="actions">
                      <button onClick={() => setSelfFixPath(p.project_path)}>
                        Use for Self-Fix
                      </button>
                      <a
                        className="ghost-link"
                        href={`${API_BASE}/projects/${encodeURIComponent(p.project_id)}/download`}
                        target="_blank"
                        rel="noreferrer"
                      >
                        Download
                      </a>
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="hint">No generated projects yet.</p>
            )}
          </Section>

          <Section
            id="runs"
            title="Run History"
            description="Recent pipeline events (analysis, codegen, tests, write, self-fix, review)."
            step={7}
          >
            <div className="actions">
              <button onClick={onLoadRuns} disabled={runsState === "loading"}>
                {runsState === "loading" ? "Loading..." : "Refresh Runs"}
              </button>
              {runsState === "error" && <span className="error">{runsError}</span>}
            </div>
            <JsonBlock data={runsData} />
          </Section>

          <Section
            id="github"
            title="Version Sync (GitHub stub)"
            description="Optional: call the GitHub sync stub for the generated project path. Configure GITHUB_TOKEN and GITHUB_REPO on the backend to enable real sync."
            step={8}
          >
            <div className="actions">
              <button onClick={onSyncGithub} disabled={githubState === "loading"}>
                {githubState === "loading" ? "Syncing..." : "Sync Project"}
              </button>
              {githubState === "error" && <span className="error">{githubError}</span>}
              {githubState === "success" && <span className="success">{githubMsg}</span>}
            </div>
          </Section>
        </div>
      </main>

      <footer className="footer">
        <div className="footer__brand">
          <div className="logo-dot" />
          <div>
            <div className="footer__title">SASDS</div>
            <div className="footer__subtitle">AI-powered software delivery</div>
          </div>
        </div>
        <div className="footer__links">
          <a href="#requirements">Requirements</a>
          <a href="#code-generation">Code</a>
          <a href="#tests">Tests</a>
          <a href="#self-correction">Self-Fix</a>
          <a href="#review">Review</a>
          <a href="#projects">Projects</a>
          <a href="#runs">History</a>
          <a href="#github">Sync</a>
        </div>
        <div className="footer__note">
          Ready for publishing: polished structure, responsive layout, and full flow in one place.
        </div>
      </footer>
    </div>
  );
}

