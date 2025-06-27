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
    print(file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return getattr(module, 'render')


def process_file(input_path: Path, output_path: Path, context):
    with open(input_path, 'r', encoding='utf-8') as f:
        input = f.read()

    metadata, idx = json.JSONDecoder().raw_decode(input)
    input = input[idx:].lstrip('\n')

    template = load_template(metadata['template'])
    render = load_renderer(metadata['renderer'])

    data = { 'metadata': metadata, 'content': render(input), 'context': context }
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template.render(data))
    
    return metadata


def process_dir(input_path: Path, output_path: Path, extensions: str):
    output_path.mkdir()

    dir_results = {}
    for child_dir in filter(lambda f: f.is_dir(), input_path.iterdir()):
        dir_results[child_dir.name] = process_dir(child_dir, output_path / child_dir.relative_to(input_path), extensions)

    file_results = {}
    for child_file in filter(lambda f: f.is_file() and f.suffix in extensions, input_path.iterdir()):
        file_results[child_file.name] = process_file(child_file, output_path / child_file.relative_to(input_path), dir_results)

    return {**dir_results, **file_results}


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
