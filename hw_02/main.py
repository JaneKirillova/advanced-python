import os
import logging
from functools import reduce
from thebestastlibrary.main import vizualize_ast


def generate_begin(title, author):
    return "\\documentclass{article}\n\\usepackage{graphicx}\\usepackage[utf8]{inputenc}\n" + \
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


def generate_image(image_location):
    vizualize_ast(image_location)
    return f"\\includegraphics[width=\\textwidth]{{{image_location}}}\n"


def generate_full_file_content(title, author, table, image_location):
    return ''.join([
        generate_begin(title, author),
        generate_table(table),
        generate_image(image_location),
        generate_end()
    ])


def make_file(title, author, table, image_location):
    with open("artifacts/table.tex", "w") as file:
        file.write(generate_full_file_content(title, author, table, image_location))
    os.system(f"pdflatex -output-directory=artifacts artifacts/table.tex")
    os.system(f"rm artifacts/table.aux artifacts/table.log")


if __name__ == '__main__':
    table = [["1", "2", "3", "4"], ["hello", "from", "python", "script"], ["1111111", "longlonglonglong", "12", "34"]]
    try:
        make_file("Python task", "Evgeniia Kirillova", table, "artifacts/ast.png")
    except Exception as e:
        logging.error("Execution failed: " + str(e))
