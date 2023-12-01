from itertools import takewhile
from pathlib import Path

input_path = Path(__file__).parent / '..' / 'inputs' / 'day1.txt'
with input_path.open('r', encoding='utf-8') as input_file:
    elves = []
    add_up_elf_food = lambda: sum(int(l) for l in takewhile(str.strip, input_file)) 
    elf_food = add_up_elf_food()
    while elf_food:
        elves.append(elf_food)
        elf_food = add_up_elf_food()

elves.sort(reverse=True)

print(elves[0])
print(sum(elves[:3]))