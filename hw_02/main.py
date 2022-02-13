import os
from functools import reduce


def generate_begin(title, author):
    return "\\documentclass{article}\n\\usepackage[utf8]{inputenc}\n" + \
           f"\\title{{{title}}}\n\\author{{{author}}}\n" + \
           "\\begin{document}\n\\maketitle\n\\begin{center}"


def generate_end():
    return "\\end{center}\\end{document}"


def generate_table(table):
    if len(list(filter(lambda line: len(line) == len(table[0]), table))) < len(table):
        raise Exception("Incorrect table")
    return ''.join([
        "\\begin{tabular}{",
        ''.join(["c"] * len(table[0])),
        "}\n",
        reduce(lambda lines, new_line: lines + "\\\\\n" + new_line,
               map(
                   lambda line: reduce(lambda cur_line, new_elem: cur_line + " & " + new_elem, line),
                   table)
               ),
        "\n\\end{tabular}\n"
    ])


def generate_full_file_content(title, author, table):
    return ''.join([
        generate_begin(title, author),
        generate_table(table),
        generate_end()
    ])


def make_file(title, author, table):
    with open("artifacts/table.tex", "w") as file:
        file.write(generate_full_file_content(title, author, table))
    os.system(f"pdflatex -output-directory=artifacts artifacts/table.tex")
    os.system(f"rm artifacts/table.aux artifacts/table.log")


if __name__ == '__main__':
    # l = ["aaa", "bbbb", "cccc"]
    # l2 = reduce(lambda lines, new_line: lines + "\\\\\n" + new_line, l)
    # print(l2)
    l3 = [["1", "2", "3"], ["13", "14", "14"], ["15", "16", "17"]]
    make_file("aaa", "jane", l3)
    # print(generate_full_file_content("aaa", "jane", l3))
