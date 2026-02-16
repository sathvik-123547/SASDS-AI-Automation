import { useEffect, useMemo, useState, useRef } from "react";
import { Terminal as TerminalIcon, PanelBottom, Bot, X, AlertTriangle, CheckCircle, Lightbulb, MessageSquare, FileText } from "lucide-react";
import { TerminalComponent } from "./components/Terminal";
import {
  analyzeRequirements,
  generateCode,
  generateCodeStream,
  writeCodeToDisk,
  createFile,
  deleteFile,
  renameFile,
  runAutoPilot,
  sendChatMessage,
  ChatMessage
} from "./api/client";
import {
  CodeGenerationResponse,
  RequirementAnalysisResponse,
  AutoPilotResponse
} from "./types";
import { parseStreamBuffer } from "./lib/stream-parser";
import { FileExplorer, FileNode } from "./components/FileExplorer";
import { buildFileTree } from "./lib/file-utils";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

import { CodeViewer } from "./components/CodeViewer";
import { ChatInterface } from "./components/ChatInterface";

type LoadState = "idle" | "loading" | "error" | "success";
type SidebarMode = "requirements" | "chat";

export default function App() {
  const [backendStatus, setBackendStatus] = useState<string>("Checking...");
  const [requirementsText, setRequirementsText] = useState<string>("Build a simple task manager API...");
  const [showTerminal, setShowTerminal] = useState(true);

  // Pipeline States
  const [analysisResult, setAnalysisResult] = useState<RequirementAnalysisResponse>();
  const [analysisState, setAnalysisState] = useState<LoadState>("idle");

  const [codeResult, setCodeResult] = useState<CodeGenerationResponse>();
  const [codeState, setCodeState] = useState<LoadState>("idle");
  const [projectId, setProjectId] = useState<string | null>(null);

  const [selectedFile, setSelectedFile] = useState<FileNode | null>(null);

  // Streaming Buffer
  const streamBuffer = useRef("");

  // Auto-Pilot State
  const [autoPilotResult, setAutoPilotResult] = useState<AutoPilotResponse | null>(null);
  const [autoPilotState, setAutoPilotState] = useState<LoadState>("idle");
  const [showAutoPilotModal, setShowAutoPilotModal] = useState(false);

  // Sidebar State
  const [sidebarMode, setSidebarMode] = useState<SidebarMode>("requirements");
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [isChatLoading, setIsChatLoading] = useState(false);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"}/ping`)
      .then((res) => res.ok ? res.json() : Promise.reject("Unavailable"))
      .then((data) => setBackendStatus(data.message || "OK"))
      .catch(() => setBackendStatus("Offline"));
  }, []);

  const fileTree = useMemo(() => {
    if (!codeResult?.files) return [];
    return buildFileTree(codeResult.files.map(f => ({ path: f.path, content: f.content })));
  }, [codeResult]);

  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // --- Requirements Logic ---
  async function onAnalyzeRequirements() {
    setAnalysisState("loading");
    setErrorMessage(null);
    try {
      const result = await analyzeRequirements(requirementsText);
      setAnalysisResult(result);
      setAnalysisState("success");
    } catch (err: any) {
      setAnalysisState("error");
      setErrorMessage(err.message || "Analysis failed");
    }
  }

  async function onGenerateCode() {
    setCodeState("loading");
    setErrorMessage(null);
    streamBuffer.current = "";
    setCodeResult({ files: [] }); // Clear previous result
    setSelectedFile(null);

    try {
      // Stream!
      await generateCodeStream(requirementsText, analysisResult, (chunk) => {
        streamBuffer.current += chunk;
        const parsedFiles = parseStreamBuffer(streamBuffer.current);

        setCodeResult({
          files: parsedFiles.map(pf => ({
            path: pf.path,
            content: pf.content,
            description: pf.isComplete ? "Generated" : "Generating..."
          }))
        });

        // Auto-select latest file
        if (parsedFiles.length > 0) {
          const lastFile = parsedFiles[parsedFiles.length - 1];
          if (lastFile.path) {
            setSelectedFile({
              name: lastFile.path.split('/').pop() || lastFile.path,
              path: lastFile.path,
              content: lastFile.content,
              type: 'file'
            });
          }
        }
      });

      setCodeState("success");

      // Finalize and Write
      const finalFiles = parseStreamBuffer(streamBuffer.current);
      const output = { files: finalFiles.map(f => ({ path: f.path, content: f.content })) };

      // Auto-save
      try {
        const writeResult = await writeCodeToDisk(output);
        setProjectId(writeResult.project_id);
        console.log("Project written to:", writeResult.project_path);
      } catch (writeErr) {
        console.error("Failed to write to disk:", writeErr);
      }

    } catch (err: any) {
      setCodeState("error");
      setErrorMessage(err.message || "Code generation failed");
    }
  }

  // --- Auto-Pilot Logic ---
  async function onRunAutoPilot() {
    if (!projectId) {
      alert("Project must be generated and saved first.");
      return;
    }
    setAutoPilotState("loading");
    setShowAutoPilotModal(true);
    try {
      const result = await runAutoPilot(projectId);
      setAutoPilotResult(result);
      setAutoPilotState("success");
    } catch (err: any) {
      setAutoPilotState("error");
      alert(`Auto-Pilot failed: ${err.message}`);
    }
  }

  // --- Chat Logic ---
  const handleSendMessage = async (message: string) => {
    const newUserMsg: ChatMessage = { role: "user", content: message };
    setChatMessages(prev => [...prev, newUserMsg]);
    setIsChatLoading(true);

    try {
      // Prepare context
      const context: any = {};
      if (selectedFile) {
        context.selected_file_path = selectedFile.path;
        context.selected_file_content = selectedFile.content;
      }
      if (codeResult) {
        context.project_structure = codeResult.files.map(f => f.path).join("\n");
      }

      const response = await sendChatMessage(message, [...chatMessages, newUserMsg], context);
      setChatMessages(prev => [...prev, response]);
    } catch (err: any) {
      const errorMsg: ChatMessage = { role: "model", content: `Error: ${err.message}` };
      setChatMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsChatLoading(false);
    }
  };

  // --- File Operations ---
  const handleFileUpdate = (path: string, newContent: string) => {
    if (!codeResult) return;

    const updatedFiles = codeResult.files.map(f =>
      f.path === path ? { ...f, content: newContent } : f
    );

    setCodeResult({ ...codeResult, files: updatedFiles });

    if (selectedFile && selectedFile.path === path) {
      setSelectedFile({ ...selectedFile, content: newContent });
    }
  };

  const handleCreateFile = async (parentPath: string) => {
    if (!projectId) {
      alert("Project must be generated and saved first.");
      return;
    }
    const fileName = prompt("Enter file name:");
    if (!fileName) return;

    const newPath = parentPath ? `${parentPath}/${fileName}` : fileName;
    const cleanPath = newPath.replace(/^\//, "");

    try {
      await createFile(`${projectId}/${cleanPath}`, "", false);
      // Update local state is tricky with streaming result, but we can append
      const newFile = { path: cleanPath, content: "", description: "New file" };
      const newFiles = [...(codeResult?.files || []), newFile];
      setCodeResult({ ...codeResult!, files: newFiles });
    } catch (err: any) {
      alert(`Failed to create file: ${err.message}`);
    }
  };

  const handleCreateFolder = async (parentPath: string) => {
    if (!projectId) {
      alert("Project must be generated and saved first.");
      return;
    }
    const folderName = prompt("Enter folder name:");
    if (!folderName) return;

    const newPath = parentPath ? `${parentPath}/${folderName}` : folderName;
    const cleanPath = newPath.replace(/^\//, "");

    try {
      await createFile(`${projectId}/${cleanPath}`, "", true);
    } catch (err: any) {
      alert(`Failed to create folder: ${err.message}`);
    }
  };

  const handleDelete = async (path: string) => {
    if (!projectId) return;
    if (!confirm(`Delete ${path}?`)) return;
    try {
      await deleteFile(`${projectId}/${path}`);
      const newFiles = (codeResult?.files || []).filter(f => !f.path.startsWith(path) && f.path !== path);
      setCodeResult({ ...codeResult!, files: newFiles });
      if (selectedFile && (selectedFile.path === path || selectedFile.path.startsWith(path))) {
        setSelectedFile(null);
      }
    } catch (err: any) {
      alert(`Failed to delete: ${err.message}`);
    }
  };

  const handleRename = async (path: string) => {
    if (!projectId) return;
    const parts = path.split('/');
    const currentName = parts.pop();
    const newName = prompt("Enter new name:", currentName);
    if (!newName || newName === currentName) return;

    const oldPathDir = parts.join('/');
    const newPath = oldPathDir ? `${oldPathDir}/${newName}` : newName;

    try {
      await renameFile(`${projectId}/${path}`, `${projectId}/${newPath}`);

      const newFiles = (codeResult?.files || []).map(f => {
        if (f.path === path) return { ...f, path: newPath };
        if (f.path.startsWith(path + "/")) {
          return { ...f, path: f.path.replace(path, newPath) };
        }
        return f;
      });
      setCodeResult({ ...codeResult!, files: newFiles });

      if (selectedFile && selectedFile.path === path) {
        setSelectedFile({ ...selectedFile, path: newPath, name: newName || "" });
      }
    } catch (err: any) {
      alert(`Failed to rename: ${err.message}`);
    }
  };

  return (
    <div className="h-screen w-full flex flex-col bg-background text-foreground overflow-hidden relative">
      {/* Header */}
      <header className="h-14 border-b flex items-center px-6 justify-between bg-card shrink-0">
        <div className="flex items-center gap-2 font-bold text-lg">
          <div className="w-3 h-3 rounded-full bg-primary" />
          SASDS <span className="text-muted-foreground font-normal text-sm ml-1">AI Automation</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <Button
            variant="ghost"
            size="sm"
            onClick={onRunAutoPilot}
            className="text-purple-500 hover:text-purple-600 hover:bg-purple-500/10"
            disabled={!projectId}
            title={!projectId ? "Generate a project first" : "Run Auto-Pilot Analysis"}
          >
            <Bot className="w-4 h-4 mr-2" />
            Auto-Pilot
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowTerminal(!showTerminal)}
            className={showTerminal ? "bg-accent" : ""}
            title="Toggle Terminal"
          >
            <PanelBottom className="w-4 h-4 mr-2" />
            Terminal
          </Button>
          <span className={cn("flex items-center gap-2 px-3 py-1 rounded-full border bg-muted/50 ml-2", backendStatus === "OK" ? "text-green-500 border-green-500/20" : "text-red-500 border-red-500/20")}>
            <div className={cn("w-2 h-2 rounded-full", backendStatus === "OK" ? "bg-green-500 animate-pulse" : "bg-red-500")} />
            {backendStatus}
          </span>
        </div>
      </header>

      {/* Main Content - Split Pane */}
      <div className="flex-1 flex overflow-hidden">

        {/* Left Sidebar - Tabs: Requirements / Chat */}
        <div className="w-[400px] border-r flex flex-col bg-card/10 shrink-0">
          {/* Tabs Header */}
          <div className="flex border-b">
            <button
              className={cn(
                "flex-1 py-2 text-xs font-medium uppercase tracking-wider flex items-center justify-center gap-2 transition-colors",
                sidebarMode === "requirements" ? "bg-background border-b-2 border-primary text-foreground" : "text-muted-foreground hover:bg-muted/50"
              )}
              onClick={() => setSidebarMode("requirements")}
            >
              <FileText className="w-3 h-3" /> Requirements
            </button>
            <button
              className={cn(
                "flex-1 py-2 text-xs font-medium uppercase tracking-wider flex items-center justify-center gap-2 transition-colors",
                sidebarMode === "chat" ? "bg-background border-b-2 border-primary text-foreground" : "text-muted-foreground hover:bg-muted/50"
              )}
              onClick={() => setSidebarMode("chat")}
            >
              <MessageSquare className="w-3 h-3" /> Agent Chat
            </button>
          </div>

          {/* Tab Content */}
          <div className="flex-1 overflow-hidden flex flex-col">
            {sidebarMode === "requirements" ? (
              <>
                <div className="p-4 border-b space-y-4">
                  <div>
                    <textarea
                      className="w-full h-32 p-3 rounded-md border bg-background text-sm resize-none focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all font-sans"
                      value={requirementsText}
                      onChange={(e) => setRequirementsText(e.target.value)}
                      placeholder="Describe your project requirements here..."
                    />
                  </div>
                  <div className="flex gap-2">
                    <Button
                      onClick={onAnalyzeRequirements}
                      disabled={analysisState === "loading"}
                      variant="outline"
                      className="flex-1"
                    >
                      {analysisState === "loading" ? "Analyzing..." : "1. Analyze"}
                    </Button>
                    <Button
                      onClick={onGenerateCode}
                      disabled={codeState === "loading"}
                      className="flex-1"
                    >
                      {codeState === "loading" ? "Generating..." : "2. Generate"}
                    </Button>
                  </div>
                </div>

                <div className="flex-1 overflow-y-auto p-4 space-y-6">
                  {analysisResult && (
                    <div className="space-y-3">
                      <h3 className="text-xs font-semibold text-muted-foreground uppercase">Requirement Summary</h3>
                      <div className="bg-muted/50 p-3 rounded-md text-xs border space-y-2">
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Modules:</span>
                          <span>{analysisResult.modules?.length || 0}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Entities:</span>
                          <span>{analysisResult.entities?.length || 0}</span>
                        </div>
                      </div>
                    </div>
                  )}

                  {codeResult && (
                    <div className="space-y-3">
                      <h3 className="text-xs font-semibold text-muted-foreground uppercase">Project Structure</h3>
                      <div className="text-sm bg-primary/10 p-3 border border-primary/20 rounded-md text-primary font-medium">
                        {codeResult.files.length} Files Generated
                        <div className="text-xs text-muted-foreground mt-1">
                          {projectId ? `Project ID: ${projectId}` : "Streaming..."}
                        </div>
                      </div>
                    </div>
                  )}

                  {errorMessage && (
                    <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-md text-destructive text-sm space-y-2 animate-in fade-in slide-in-from-top-1">
                      <div className="font-bold flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-destructive" />
                        Request Failed
                      </div>
                      <div className="text-xs opacity-90 break-words leading-relaxed">
                        {errorMessage}
                      </div>
                    </div>
                  )}
                </div>
              </>
            ) : (
              <div className="flex-1 flex flex-col h-full">
                <ChatInterface
                  messages={chatMessages}
                  onSendMessage={handleSendMessage}
                  isLoading={isChatLoading}
                  currentFile={selectedFile?.path}
                />
              </div>
            )}
          </div>
        </div>

        {/* Middle - File Explorer (Keep same) */}
        <div className="w-[280px] border-r flex flex-col bg-card/5 shrink-0">
          <div className="h-10 border-b flex items-center px-4 bg-muted/30">
            <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">Explorer</span>
          </div>
          <FileExplorer
            data={fileTree}
            onFileSelect={setSelectedFile}
            className="flex-1"
            onCreateFile={handleCreateFile}
            onCreateFolder={handleCreateFolder}
            onDelete={handleDelete}
            onRename={handleRename}
          />
        </div>

        {/* Right - Code Preview & Terminal */}
        <div className="flex-1 flex flex-col bg-background relative overflow-hidden">
          <div className="flex-1 flex flex-col min-h-0">
            {selectedFile ? (
              <CodeViewer
                file={selectedFile}
                onUpdate={handleFileUpdate}
              />
            ) : (
              <div className="flex-1 flex flex-col items-center justify-center text-muted-foreground bg-grid-slate-900/[0.04]">
                <div className="w-12 h-12 rounded-2xl bg-muted flex items-center justify-center mb-4">
                  <div className="w-6 h-6 border-2 border-muted-foreground/30 rounded" />
                </div>
                <p className="text-sm font-medium">Select a file to preview code</p>
                <p className="text-xs opacity-60 mt-1">Generate code or browse the explorer</p>
              </div>
            )}
          </div>

          {/* Terminal Panel */}
          {showTerminal && (
            <div className="h-[30%] border-t bg-[#1e1e1e] flex flex-col shrink-0">
              <div className="h-8 flex items-center px-4 border-b border-[#333] bg-[#252526] text-white select-none">
                <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wider text-[#cccccc]">
                  <TerminalIcon className="w-3 h-3" />
                  Terminal
                </div>
              </div>
              <div className="flex-1 min-h-0">
                <TerminalComponent />
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Auto-Pilot Modal */}
      {showAutoPilotModal && (
        <div className="absolute inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
          <div className="bg-background border rounded-lg shadow-xl w-full max-w-3xl max-h-[80vh] flex flex-col animate-in zoom-in-95">
            <div className="flex items-center justify-between p-4 border-b">
              <h2 className="text-lg font-bold flex items-center gap-2">
                <Bot className="w-5 h-5 text-purple-500" /> Auto-Pilot Analysis
              </h2>
              <Button variant="ghost" size="sm" onClick={() => setShowAutoPilotModal(false)}>
                <X className="w-4 h-4" />
              </Button>
            </div>
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              {autoPilotState === "loading" ? (
                <div className="flex flex-col items-center justify-center h-40 space-y-4">
                  <div className="w-8 h-8 rounded-full border-2 border-primary border-t-transparent animate-spin" />
                  <p className="text-muted-foreground">Analyzing project structure and code...</p>
                </div>
              ) : autoPilotResult ? (
                <>
                  <div className="bg-muted p-4 rounded-md text-sm">
                    <h3 className="font-semibold mb-2">Summary</h3>
                    <p className="text-muted-foreground">{autoPilotResult.summary}</p>
                  </div>

                  <div>
                    <h3 className="font-semibold flex items-center gap-2 mb-3">
                      <AlertTriangle className="w-4 h-4 text-orange-500" />
                      Issues Found ({autoPilotResult.issues.length})
                    </h3>
                    <div className="space-y-3">
                      {autoPilotResult.issues.map((issue, idx) => (
                        <div key={idx} className="border p-3 rounded-md text-sm bg-card">
                          <div className="flex items-center gap-2 font-medium">
                            <span className={cn(
                              "uppercase text-[10px] px-1.5 py-0.5 rounded border",
                              issue.severity === "high" ? "bg-red-500/10 text-red-500 border-red-500/20" :
                                issue.severity === "medium" ? "bg-orange-500/10 text-orange-500 border-orange-500/20" : "bg-blue-500/10 text-blue-500 border-blue-500/20"
                            )}>{issue.severity}</span>
                            <span>{issue.file}</span>
                            {issue.line && <span className="text-muted-foreground text-xs">:L{issue.line}</span>}
                          </div>
                          <p className="mt-1 text-muted-foreground">{issue.description}</p>
                          <div className="mt-2 bg-muted/50 p-2 rounded text-xs">
                            <span className="font-semibold text-primary">Suggestion: </span>
                            {issue.suggestion}
                          </div>
                        </div>
                      ))}
                      {autoPilotResult.issues.length === 0 && (
                        <p className="text-sm text-muted-foreground">No critical issues found.</p>
                      )}
                    </div>
                  </div>

                  <div>
                    <h3 className="font-semibold flex items-center gap-2 mb-3">
                      <Lightbulb className="w-4 h-4 text-yellow-500" />
                      Suggested Improvements ({autoPilotResult.improvements.length})
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {autoPilotResult.improvements.map((imp, idx) => (
                        <div key={idx} className="border p-3 rounded-md text-sm bg-card/50">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-xs bg-secondary px-1.5 py-0.5 rounded text-secondary-foreground">{imp.type}</span>
                            {imp.file && <span className="text-xs text-muted-foreground font-mono">{imp.file}</span>}
                          </div>
                          <p className="text-muted-foreground">{imp.description}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </>
              ) : (
                <div className="text-center text-red-500">Failed to load analysis.</div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
