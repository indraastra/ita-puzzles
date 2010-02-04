from strawberry_fields import StrawberryField

def read_puzzles(file):
    state = "N"
    N = None
    field = []
    for line in open(file):
        line = line.rstrip()
        if state == "N":
            if line:
                N = int(line)
                field = []
                state = "field"
        elif state == "field":
            if line:
                field.append(line.rstrip())
            else:
                state = "N"
                yield N, StrawberryField(field)

