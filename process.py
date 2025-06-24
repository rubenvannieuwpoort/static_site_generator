import os
import json
import importlib
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


template_env = None
renderers_path = None


def load_template(template_name: str):
    return template_env.get_template(template_name)


def load_renderer(renderer_name: str):
    global renderers_path
    file_path = os.path.join(renderers_path, renderer_name)

    spec = importlib.util.spec_from_file_location(renderer_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return getattr(module, 'render')


def process_file(input_path: Path, output_path: Path):
    with open(input_path, 'r', encoding='utf-8') as f:
        input = f.read()

    metadata, idx = json.JSONDecoder().raw_decode(input)
    input = input[idx:].lstrip('\n')

    template = load_template(metadata['template'])
    render = load_renderer(metadata['renderer'])

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template.render({
            'metadata': metadata,
            'content': render(input),
        }))


def process_dir(input_path: Path, output_path: Path, extensions: str):
    for dirpath, _, filenames in input_path.walk(top_down=False):
        target_folder = Path(output_path, *dirpath.parts[1:])
        target_folder.mkdir()
        for filename in filenames:
            process_file(dirpath / filename, target_folder / filename)


def process(input_path: Path, output_path: Path, templates_path: Path, _renderers_path: Path, extensions: str) -> None:
    if not input_path.exists():
        print('input does not exist!')  # TODO: better error message
        exit(1)

    if not templates_path.exists():
        print('templates folder does not exist!')  # TODO: better error message
        exit(1)

    if not _renderers_path.exists():
        print('renderers folder does not exist!')  # TODO: better error message
        exit(1)

    if output_path.exists():
        print('output already exists!')  # TODO: better error message
        exit(1)

    global template_env
    template_env = Environment(loader=FileSystemLoader(templates_path))

    global renderers_path
    renderers_path = _renderers_path

    if input_path.is_file():
        process_file(input_path, output_path)
    elif input_path.is_dir():
        process_dir(input_path, output_path, extensions)
