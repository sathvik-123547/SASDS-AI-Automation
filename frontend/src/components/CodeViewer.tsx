import { useState, useEffect } from "react";
import Editor from "@monaco-editor/react";
import { FileNode } from "./FileExplorer";
import { Button } from "@/components/ui/button";
import { refineCode } from "@/api/client";
import { Loader2, Wand2, Save } from "lucide-react";

interface CodeViewerProps {
    file: FileNode | null;
    onUpdate: (path: string, newContent: string) => void;
}

export function CodeViewer({ file, onUpdate }: CodeViewerProps) {
    const [instructions, setInstructions] = useState("");
    const [isRefining, setIsRefining] = useState(false);
    const [showRefineInput, setShowRefineInput] = useState(false);
    const [editorContent, setEditorContent] = useState("");

    // Reset state when file changes
    useEffect(() => {
        setInstructions("");
        setShowRefineInput(false);
        setEditorContent(file?.content || "");
    }, [file?.path, file?.content]);

    if (!file) {
        return (
            <div className="flex-1 flex flex-col items-center justify-center text-muted-foreground bg-muted/10">
                <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center mb-4">
                    <div className="w-8 h-8 border-2 border-muted-foreground/30 rounded" />
                </div>
                <p>Select a file to view content</p>
            </div>
        );
    }

    const handleRefine = async () => {
        if (!editorContent || !instructions.trim()) return;

        setIsRefining(true);
        try {
            const result = await refineCode(file.path, editorContent, instructions);
            onUpdate(result.path, result.new_content);
            setEditorContent(result.new_content);
            setShowRefineInput(false);
            setInstructions("");
        } catch (error) {
            console.error("Refinement failed:", error);
            // Ideally show a toast here
        } finally {
            setIsRefining(false);
        }
    };

    // Determine language based on file extension
    const getLanguage = (path: string) => {
        if (path.endsWith(".py")) return "python";
        if (path.endsWith(".js") || path.endsWith(".jsx")) return "javascript";
        if (path.endsWith(".ts") || path.endsWith(".tsx")) return "typescript";
        if (path.endsWith(".html")) return "html";
        if (path.endsWith(".css")) return "css";
        if (path.endsWith(".json")) return "json";
        if (path.endsWith(".md")) return "markdown";
        return "plaintext";
    };

    return (
        <div className="flex-1 flex flex-col h-full bg-[#1e1e1e]">
            {/* Toolbar */}
            <div className="h-12 border-b border-[#333] flex items-center justify-between px-4 bg-[#252526] text-white">
                <div className="flex items-center gap-2">
                    <span className="font-mono text-sm text-[#9cdcfe]">{file.path}</span>
                    {editorContent !== file.content && (
                        <span className="text-xs text-yellow-500 italic">(modified)</span>
                    )}
                </div>
                <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowRefineInput(!showRefineInput)}
                    className={`hover:bg-[#333] hover:text-white ${showRefineInput ? "bg-[#3e3e42] text-white" : "text-[#cccccc]"}`}
                >
                    <Wand2 className="w-4 h-4 mr-2" />
                    Refine with AI
                </Button>
            </div>

            {/* Refine Input Area */}
            {showRefineInput && (
                <div className="border-b border-[#333] p-4 bg-[#252526] animate-in slide-in-from-top-2">
                    <textarea
                        className="w-full h-20 p-3 text-sm border border-[#3e3e42] rounded-md resize-none mb-2 bg-[#1e1e1e] text-[#d4d4d4] focus:outline-none focus:ring-1 focus:ring-[#007fd4]"
                        placeholder="Describe how to refine this code..."
                        value={instructions}
                        onChange={(e) => setInstructions(e.target.value)}
                        disabled={isRefining}
                        autoFocus
                    />
                    <div className="flex justify-end gap-2">
                        <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => setShowRefineInput(false)}
                            disabled={isRefining}
                            className="text-[#cccccc] hover:bg-[#333] hover:text-white"
                        >
                            Cancel
                        </Button>
                        <Button
                            size="sm"
                            onClick={handleRefine}
                            disabled={isRefining || !instructions.trim()}
                            className="bg-[#007fd4] hover:bg-[#0060a0] text-white"
                        >
                            {isRefining ? (
                                <>
                                    <Loader2 className="w-3 h-3 mr-2 animate-spin" />
                                    Refining...
                                </>
                            ) : (
                                "Apply Changes"
                            )}
                        </Button>
                    </div>
                </div>
            )}

            {/* Monaco Editor */}
            <div className="flex-1 overflow-hidden">
                <Editor
                    height="100%"
                    language={getLanguage(file.path)}
                    value={editorContent}
                    theme="vs-dark"
                    onChange={(value) => setEditorContent(value || "")}
                    options={{
                        minimap: { enabled: true },
                        fontSize: 14,
                        wordWrap: "on",
                        scrollBeyondLastLine: false,
                        padding: { top: 16 },
                    }}
                />
            </div>

            {/* Status Bar */}
            <div className="h-6 bg-[#007acc] text-white px-3 flex items-center justify-end text-xs gap-4">
                <span>Ln {editorContent.split('\n').length}</span>
                <span>UTF-8</span>
                <span>{getLanguage(file.path).toUpperCase()}</span>
            </div>
        </div>
    );
}
