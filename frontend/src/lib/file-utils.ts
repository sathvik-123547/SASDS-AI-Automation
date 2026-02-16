import { FileNode } from "@/components/FileExplorer";
import { CodeGenerationResponse } from "@/types";

export function buildFileTree(files: { path: string; content: string }[]): FileNode[] {
    const root: FileNode[] = [];

    files.forEach((file) => {
        const parts = file.path.split('/');
        let currentLevel = root;

        parts.forEach((part, index) => {
            const isFile = index === parts.length - 1;
            const path = parts.slice(0, index + 1).join('/');

            let existingNode = currentLevel.find((node) => node.path === path);

            if (!existingNode) {
                const newNode: FileNode = {
                    name: part,
                    type: isFile ? 'file' : 'folder',
                    path: path,
                    children: isFile ? undefined : [],
                    content: isFile ? file.content : undefined,
                };
                currentLevel.push(newNode);
                existingNode = newNode;
            }

            if (!isFile && existingNode.children) {
                currentLevel = existingNode.children;
            }
        });
    });

    return root;
}
