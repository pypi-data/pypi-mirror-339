from openvariant import Annotation, Variant

dataset_file_linux = "/home/fbrando/Desktop/bgtools/openvariant/tests/data/dataset/KRAS_linux.txt"
dataset_file_windows = "/home/fbrando/Desktop/bgtools/openvariant/tests/data/dataset/KRAS_windows.txt"

annotation_file = "/home/fbrando/Desktop/bgtools/openvariant/tests/data/protein.yaml"

annotation = Annotation(annotation_path=annotation_file)
result_linux = Variant(path=dataset_file_linux, annotation=annotation)
result_windows = Variant(path=dataset_file_windows, annotation=annotation)

for n_line, line in enumerate(result_linux.read()):
    print(f'Line (linux) {n_line}: {line}')
    if n_line == 9:
        break

for n_line, line in enumerate(result_windows.read()):
    print(f'Line (windows) {n_line}: {line}')
    if n_line == 9:
        break