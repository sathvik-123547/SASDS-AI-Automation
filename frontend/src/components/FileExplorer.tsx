import React, { useState } from 'react';
import { ChevronRight, ChevronDown, File, Folder, Plus, Trash, Edit } from 'lucide-react';
import { cn } from '@/lib/utils';
import {
    ContextMenu,
    ContextMenuContent,
    ContextMenuItem,
    ContextMenuTrigger,
    ContextMenuSeparator,
} from "@/components/ui/context-menu";

export interface FileNode {
    name: string;
    type: 'file' | 'folder';
    children?: FileNode[];
    content?: string;
    path: string;
}

interface FileExplorerProps {
    data: FileNode[];
    onFileSelect: (file: FileNode) => void;
    className?: string;
    onCreateFile?: (parentPath: string) => void;
    onCreateFolder?: (parentPath: string) => void;
    onDelete?: (path: string) => void;
    onRename?: (path: string) => void;
}

const FileTreeNode: React.FC<{
    node: FileNode;
    onSelect: (node: FileNode) => void;
    depth?: number;
    actions: {
        onCreateFile?: (path: string) => void;
        onCreateFolder?: (path: string) => void;
        onDelete?: (path: string) => void;
        onRename?: (path: string) => void;
    }
}> = ({
    node,
    onSelect,
    depth = 0,
    actions
}) => {
        const [isOpen, setIsOpen] = useState(false);

        const handleToggle = (e: React.MouseEvent) => {
            e.stopPropagation();
            if (node.type === 'folder') {
                setIsOpen(!isOpen);
            } else {
                onSelect(node);
            }
        };

        return (
            <div>
                <ContextMenu>
                    <ContextMenuTrigger>
                        <div
                            className={cn(
                                "flex items-center py-1 px-2 cursor-pointer hover:bg-accent hover:text-accent-foreground text-sm select-none",
                                depth > 0 && `pl-[${(depth * 12) + 8}px]`
                            )}
                            style={{ paddingLeft: `${depth * 12 + 8}px` }}
                            onClick={handleToggle}
                            onContextMenu={(e) => {
                                // Select on right click too if it's a file
                                if (node.type === 'file') onSelect(node);
                            }}
                        >
                            <span className="mr-1 opacity-70">
                                {node.type === 'folder' ? (
                                    isOpen ? <ChevronDown size={16} /> : <ChevronRight size={16} />
                                ) : (
                                    <File size={16} />
                                )}
                            </span>

                            <span className="flex items-center gap-2">
                                {node.type === 'folder' && <Folder size={16} className="text-blue-500 fill-blue-500/20" />}
                                {node.name}
                            </span>
                        </div>
                    </ContextMenuTrigger>
                    <ContextMenuContent className="w-48">
                        {node.type === 'folder' && (
                            <>
                                <ContextMenuItem onClick={() => actions.onCreateFile?.(node.path)}>
                                    <Plus className="mr-2 h-4 w-4" /> New File
                                </ContextMenuItem>
                                <ContextMenuItem onClick={() => actions.onCreateFolder?.(node.path)}>
                                    <Folder className="mr-2 h-4 w-4" /> New Folder
                                </ContextMenuItem>
                                <ContextMenuSeparator />
                            </>
                        )}
                        <ContextMenuItem onClick={() => actions.onRename?.(node.path)}>
                            <Edit className="mr-2 h-4 w-4" /> Rename
                        </ContextMenuItem>
                        <ContextMenuItem onClick={() => actions.onDelete?.(node.path)} className="text-red-500 focus:text-red-500">
                            <Trash className="mr-2 h-4 w-4" /> Delete
                        </ContextMenuItem>
                    </ContextMenuContent>
                </ContextMenu>

                {isOpen && node.children && (
                    <div>
                        {node.children.map((child) => (
                            <FileTreeNode
                                key={child.path}
                                node={child}
                                onSelect={onSelect}
                                depth={depth + 1}
                                actions={actions}
                            />
                        ))}
                    </div>
                )}
            </div>
        );
    };

export const FileExplorer: React.FC<FileExplorerProps> = ({
    data,
    onFileSelect,
    className,
    onCreateFile,
    onCreateFolder,
    onDelete,
    onRename
}) => {
    return (
        <div className={cn("h-full overflow-y-auto border-r bg-card", className)}>
            <div className="p-4 font-semibold text-sm text-muted-foreground border-b mb-2 flex justify-between items-center group">
                EXPLORER
                {/* Root level actions could go here */}
            </div>
            {data.map((node) => (
                <FileTreeNode
                    key={node.path}
                    node={node}
                    onSelect={onFileSelect}
                    actions={{ onCreateFile, onCreateFolder, onDelete, onRename }}
                />
            ))}
        </div>
    );
};

