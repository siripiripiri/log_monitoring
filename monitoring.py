import os
import asyncio
import websockets

file_path = 'logfile.txt'

# def get_last_10_lines(file_path):
#     with open(file_path, 'r') as file:
#         file.seek(0, os.SEEK_END)
#         lines = file.readlines()
#         return lines[-10:]

def get_last_10_lines(file_path):
    with open(file_path, 'r') as file:
        file.seek(0, os.SEEK_END)

        end_position = file.tell()
        lines = []
        position = end_position
        
        while position > 0 and len(lines)-1 < 10:
            file.seek(position - 1)
            char = file.read(1)
            
            if char == '\n':
                if lines:
                    lines.append('\n')
                else:
                    lines.append('\n')
            else:
                if lines:
                    lines[-1] = char + lines[-1]
                else:
                    lines.append(char)
            position -= 1

        return lines[::-1][-10:]


async def tail_log_file(websocket):
    last_10_lines = get_last_10_lines(file_path)
    await websocket.send(''.join(last_10_lines))
    
    with open(file_path, 'r') as file:
        file.seek(0, os.SEEK_END)
        last_read_position = file.tell()
        last_modified = os.path.getmtime(file_path)
        
        while True:
            """has the file been modified?"""
            new_modified = os.path.getmtime(file_path)
            if new_modified != last_modified:
                last_modified = new_modified
                
                """moving to the last read position and start reading new lines"""
                file.seek(last_read_position)
                lines = file.readlines()
                
                """if there are new lines, send them to the client"""
                if lines:
                    last_read_position = file.tell()
                    await websocket.send(''.join(lines))
            
            await asyncio.sleep(1)

async def websocket_server():
    server = await websockets.serve(tail_log_file, "localhost", 8765)
    await server.wait_closed()

asyncio.run(websocket_server())
