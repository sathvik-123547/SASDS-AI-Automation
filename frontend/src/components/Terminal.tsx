import { useEffect, useRef } from "react";
import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import "xterm/css/xterm.css";

interface TerminalComponentProps {
    className?: string;
}

export function TerminalComponent({ className }: TerminalComponentProps) {
    const terminalRef = useRef<HTMLDivElement>(null);
    const wsRef = useRef<WebSocket | null>(null);
    const xtermRef = useRef<Terminal | null>(null);
    const fitAddonRef = useRef<FitAddon | null>(null);

    useEffect(() => {
        if (!terminalRef.current) return;

        // Initialize xterm.js
        const term = new Terminal({
            cursorBlink: true,
            theme: {
                background: "#1e1e1e",
                foreground: "#d4d4d4",
                cursor: "#d4d4d4",
                black: "#000000",
                red: "#cd3131",
                green: "#0dbc79",
                yellow: "#e5e510",
                blue: "#2472c8",
                magenta: "#bc3fbc",
                cyan: "#11a8cd",
                white: "#e5e5e5",
                brightBlack: "#666666",
                brightRed: "#f14c4c",
                brightGreen: "#23d18b",
                brightYellow: "#f5f543",
                brightBlue: "#3b8eea",
                brightMagenta: "#d670d6",
                brightCyan: "#29b8db",
                brightWhite: "#e5e5e5",
            },
            fontFamily: 'Menlo, Monaco, "Courier New", monospace',
            fontSize: 14,
        });

        const fitAddon = new FitAddon();
        term.loadAddon(fitAddon);
        term.open(terminalRef.current);
        fitAddon.fit();

        xtermRef.current = term;
        fitAddonRef.current = fitAddon;

        // Connect to WebSocket
        const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
        const host = import.meta.env.VITE_API_BASE_URL
            ? import.meta.env.VITE_API_BASE_URL.replace(/^http(s)?:\/\//, "")
            : "localhost:8000";

        const wsUrl = `${protocol}//${host}/terminal/ws`;
        console.log("Connecting to terminal WebSocket:", wsUrl);

        const ws = new WebSocket(wsUrl);
        wsRef.current = ws;

        ws.onopen = () => {
            console.log("Terminal WebSocket connected");
            term.write("\r\n\x1b[32m$ Connected to backend terminal\x1b[0m\r\n");
            // Send initial resize
            ws.send(JSON.stringify({ type: "resize", cols: term.cols, rows: term.rows }));
        };

        ws.onmessage = (event) => {
            term.write(event.data);
        };

        ws.onclose = () => {
            term.write("\r\n\x1b[31m$ Connection closed\x1b[0m\r\n");
        };

        ws.onerror = (error) => {
            console.error("Terminal WebSocket error:", error);
            term.write("\r\n\x1b[31m$ Connection error\x1b[0m\r\n");
        };

        // Send input to backend
        term.onData((data) => {
            if (ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ type: "input", data }));
            }
        });

        // Handle resize
        const handleResize = () => {
            fitAddon.fit();
            if (ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ type: "resize", cols: term.cols, rows: term.rows }));
            }
        };
        window.addEventListener("resize", handleResize);

        return () => {
            window.removeEventListener("resize", handleResize);
            ws.close();
            term.dispose();
        };
    }, []);

    // Re-fit when container size changes (if possible to detect via ResizeObserver)
    useEffect(() => {
        if (!terminalRef.current || !fitAddonRef.current) return;

        const observer = new ResizeObserver(() => {
            fitAddonRef.current?.fit();
        });
        observer.observe(terminalRef.current);

        return () => observer.disconnect();
    }, []);

    return (
        <div className={`h-full w-full bg-[#1e1e1e] p-2 overflow-hidden ${className}`}>
            <div ref={terminalRef} className="h-full w-full" />
        </div>
    );
}
