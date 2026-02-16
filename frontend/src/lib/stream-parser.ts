export interface ParsedFile {
    path: string;
    content: string;
    isComplete: boolean;
}

export function parseStreamBuffer(buffer: string): ParsedFile[] {
    const files: ParsedFile[] = [];

    // Regex to match completed files
    // ### FILE: path
    // content
    // ### END FILE ###
    const fileRegex = /### FILE: \s*(.+?)\s*[\r\n]+([\s\S]*?)### END FILE ###/g;

    let match;
    let lastIndex = 0;

    // Find all completed files
    while ((match = fileRegex.exec(buffer)) !== null) {
        files.push({
            path: match[1].trim(),
            content: match[2], // Content usually starts with newline, maybe trimStart? Prompt says "Output the files... format". We can trim empty lines.
            isComplete: true
        });
        lastIndex = match.index + match[0].length;
    }

    // Check for incomplete file at the end
    const remaining = buffer.slice(lastIndex);
    const startMatch = /### FILE: \s*(.+?)\s*[\r\n]+([\s\S]*)$/.exec(remaining);

    if (startMatch) {
        files.push({
            path: startMatch[1].trim(),
            content: startMatch[2],
            isComplete: false
        });
    }

    return files;
}
