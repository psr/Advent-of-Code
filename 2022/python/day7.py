from pathlib import Path
import re
from functools import cached_property


command_line = re.compile(r'^\$ (\S+)\s?(.*)$')
dir_line = re.compile(r'^dir (.+)$')
file_line = re.compile(r'^(\d+) (.+)$')


class Directory:

    def __init__(self, name):
        self.name = name
        self.subdirectories = {}
        self.files = {}

    @cached_property
    def total_size(self):
        return (sum(self.files.values()) 
            + sum(d.total_size for d in self.subdirectories.values()))


    def __iter__(self):
        """Depth first traversal, yielding directories"""
        for dir in self.subdirectories.values():
            yield from dir
            yield dir


class TraversalState:

    def __init__(self, root):
        self.path = [root]

    def cd(self, arg):
        if arg == '..':
            self.path.pop()
        elif arg == '/':
            del self.path[1:]
        else:
            self.path.append(self.path[-1].subdirectories[arg])

    def ls(self, arg):
        pass

    def file(self, size, name):
        files = self.path[-1].files
        assert name not in files
        files[name] = size

    def dir(self, name):
        dirs = self.path[-1].subdirectories
        assert name not in dirs
        dirs[name] = Directory(name)


root = Directory('/')

input_path = Path(__file__).parent / '..' / 'inputs' / 'day7.txt'
with input_path.open('r', encoding='utf-8') as input_file:
    state = TraversalState(root)
    for line in input_file:
        if (match := command_line.match(line)):
            command, arg = match.groups()
            getattr(state, command)(arg)
        elif (match := dir_line.match(line)):
            name, = match.groups()
            state.dir(name)
        elif (match := file_line.match(line)):
            size, name = match.groups()
            state.file(int(size), name)
        else:
            breakpoint()

print(sum(d.total_size for d in root if d.total_size <= 100000))
fs_size = 70_000_000
used = root.total_size
free = fs_size - used
needed = 30000000
must_delete = needed - free
big_enough = (d for d in root if d.total_size >= must_delete)
to_delete = min(big_enough, key=lambda d: d.total_size)
print(to_delete.name, to_delete.total_size)