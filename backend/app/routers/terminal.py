import asyncio
import os
import pty
import select
import struct
import fcntl
import termios
import logging
from typing import Dict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()
logger = logging.getLogger("sasds-backend")

@router.websocket("/terminal/ws")
async def terminal_websocket(websocket: WebSocket):
    await websocket.accept()
    
    # Create PTY
    (master_fd, slave_fd) = pty.openpty()
    
    # Set non-blocking
    fl = fcntl.fcntl(master_fd, fcntl.F_GETFL)
    fcntl.fcntl(master_fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    # Fork shell process
    pid = os.fork()
    if pid == 0:
        # Child process
        os.setsid()
        os.dup2(slave_fd, 0)
        os.dup2(slave_fd, 1)
        os.dup2(slave_fd, 2)
        os.close(master_fd)
        os.close(slave_fd)
        
        # Determine shell
        shell = os.environ.get("SHELL", "/bin/bash")
        os.execv(shell, [shell])
    else:
        # Parent process (FastAPI)
        os.close(slave_fd)
        logger.info(f"Started terminal session PID: {pid}")

        async def read_from_pty():
            while True:
                await asyncio.sleep(0.01)
                try:
                    data = os.read(master_fd, 1024)
                    if not data:
                        break
                    await websocket.send_text(data.decode(errors="ignore"))
                except BlockingIOError:
                    continue
                except OSError:
                     break
                except Exception as e:
                    logger.error(f"Error reading from PTY: {e}")
                    break

        async def write_to_pty():
            try:
                while True:
                    data = await websocket.receive_text()
                    # Parse JSON or raw text?
                    # The frontend sends JSON {type: "input", data: "..."} or {type: "resize", ...}
                    import json
                    try:
                        message = json.loads(data)
                        if message["type"] == "input":
                            os.write(master_fd, message["data"].encode())
                        elif message["type"] == "resize":
                            cols = message["cols"]
                            rows = message["rows"]
                            # Set terminal window size
                            winsize = struct.pack("HHHH", rows, cols, 0, 0)
                            fcntl.ioctl(master_fd, termios.TIOCSWINSZ, winsize)
                    except json.JSONDecodeError:
                        # Fallback for raw input if any
                        os.write(master_fd, data.encode())
            except WebSocketDisconnect:
                logger.info("WebSocket disconnected")
            except Exception as e:
                logger.error(f"Error writing to PTY: {e}")

        # Run tasks concurrently
        task_read = asyncio.create_task(read_from_pty())
        task_write = asyncio.create_task(write_to_pty())

        done, pending = await asyncio.wait(
            [task_read, task_write],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

        os.close(master_fd)
        # Kill zombie process if needed
        try:
             os.kill(pid, 9)
             os.waitpid(pid, 0)
        except OSError:
             pass
        logger.info(f"Terminal session PID {pid} closed")
