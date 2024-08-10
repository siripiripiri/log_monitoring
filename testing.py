import os

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
                    lines.append('')
                else:
                    lines.append('')
            else:
                if lines:
                    lines[-1] = char + lines[-1]
                else:
                    lines.append(char)
            position -= 1

        return lines[::-1][-10:]

file_path = 'logfile.txt'
last_10_lines = get_last_10_lines(file_path)
