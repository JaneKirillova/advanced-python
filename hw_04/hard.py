import codecs
import datetime
import time
from multiprocessing import Queue, Process


def process_a(input_queue, output_queue):
    while True:
        if not input_queue.empty():
            output_queue.put(input_queue.get().lower())
            time.sleep(5)


def process_b(input_queue, output_queue):
    while True:
        if not input_queue.empty():
            output_queue.put(codecs.encode(input_queue.get(), 'rot_13'))


if __name__ == '__main__':
    main_to_a = Queue()
    a_to_b = Queue()
    b_to_stdout = Queue()
    Process(target=process_a, args=(main_to_a, a_to_b), daemon=True).start()
    Process(target=process_b, args=(a_to_b, b_to_stdout), daemon=True).start()
    with open('artifacts/hard_dialogue.txt', "w") as file:
        while True:
            while not b_to_stdout.empty():
                b_output = b_to_stdout.get()
                file.write(f'{datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")}, output: {b_output}\n')
                print("<<< " + b_output)
            stdin_input = input('>>> ')
            if stdin_input == 'exit':
                while not main_to_a.empty() or not a_to_b.empty() or not b_to_stdout.empty():
                    b_output = b_to_stdout.get()
                    file.write(f'{datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")}, output: {b_output}\n')
                    print("<<< " + b_output)
                file.write(f'{datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")}, END CONVERSATION\n')
                break
            main_to_a.put(stdin_input)
            file.write(f'{datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")}, input: {stdin_input}\n')