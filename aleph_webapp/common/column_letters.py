
def get_column_letters(max_col=10):
    aux = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    seq_count = int(max_col / len(aux))
    column_letters = []
    for i in range(-1, seq_count):

        # Get prefix
        if i == -1: prefix = ""
        else: prefix = aux[i]

        # Add column letter
        for a in aux:
            column_letters.append(prefix + a)
            if len(column_letters) == max_col: return column_letters

    return column_letters
