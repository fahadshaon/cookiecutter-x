import os
import json
import argh
import logging
import shutil
import hashlib
import re
from collections import OrderedDict

from cookiecutter_modified import cookiecutter

app_name_rx = re.compile('^[a-zA-Z][a-zA-Z0-9_]*$')


def boolean(b):
    return b in ['True', 'T', 'true', 't', 'Yes', 'Y', 'yes', 'y', '1', True]


def read_json(p):
    """
    Read a JSON file

    :param p: Path of the json file to read
    :return: JSON object read from the file
    """
    with open(p) as f:
        return json.load(f)


def mkdirs(p):
    """
    Create a directory at provided path if it doesn't already exists.

    :param p: Path to create
    """
    if not os.path.exists(p):
        logging.info('Path does not exit, creating: {}'.format(os.path.normpath(p)))
        os.makedirs(p)


def gen_file_path(base_dir, src_file, dst_dir):
    """
    Generate source, destination directory and destination file path from
    ``src_file`` relative to ``base_dir`` and ``dst_dir`` destination directory.

    :param base_dir: Base directory
    :param src_file: Source file path
    :param dst_dir: Destination base path
    :return: Tuple of (source file, destination directory, and destination file)
    """
    dst_file = os.path.join(dst_dir, src_file)
    src_file = os.path.join(base_dir, src_file)

    return src_file, os.path.dirname(dst_file), dst_file


def cpy(src_file, dst_dir):
    """
    Copy a file to destination directory

    :param src_file: File to copy
    :param dst_dir: Directory to copy
    """

    mkdirs(dst_dir)
    logging.info('{} -> {}'.format(os.path.normpath(src_file), os.path.normpath(dst_dir)))
    shutil.copy(src_file, dst_dir)


def compare(src, dst):
    """
    Compare files in two directory. To make sure source and destination has same prefix,
    src in full path of files is replaced with dst.

    :param src: Source directory
    :param dst: Destination directory
    :return: Tuple of difference and intersection of ``src`` and ``dst`` directory.
    """
    src_files = set([s.replace(src, dst) for s in walk(src)])
    dst_files = set(walk(dst))

    return src_files - dst_files, src_files.intersection(dst_files)


def walk(src):
    """
    Generate list of files in a directory recursively.
    This method ignores directory named ``.ccx_archive``.

    :param src: Directory to walk
    :return: List of file paths
    """
    out = []
    for folder, subs, files in os.walk(src):
        for filename in files:
            f = os.path.join(folder, filename)
            out.append(f)

        if '.ccx_archive' in subs:
            subs.remove('.ccx_archive')

    return out


def find_unused_name(p):
    """
    Find a unused name for a file by adding number at the end of the filename.
    If that already exists then increment the number, until a name is found.

    :param p: File path to find unused name.
    :return: Unused name for the provided file.
    """
    d, f = os.path.split(p)

    c = 0
    while True:
        c += 1
        np = os.path.join(d, '{}.{}'.format(f, c))

        if not os.path.exists(np):
            return np


def file_hash(p, block_size=4096):
    """
    Compute and return hash 256 digest of provided file.
    This method reads file block by block. Block size can
    be specified by `block_size` parameter defaults to 4KB (4096)

    :param p: path of file to compute hash
    :param block_size: amount data read simultaneously in byte
    :return: hash digest of the file
    """
    h = hashlib.sha256()
    with open(p) as f:
        for chunk in iter(lambda: f.read(block_size), ''):
            h.update(chunk)
    return h.hexdigest()


def copy_gen_files(out_dir):
    """
    Copy generated files from the output directory to current directory.
    First this method generates difference and intersection between these two directories.
    A file in difference set means it is in source but not in destination, so we copy it directly.
    A file in intersection set means it is in both source and destination, now we first check whether
    these are same then do nothing.
    Otherwise we create a back up of destination file and replace it with newly generated file.

    :param out_dir: Output directory of cookiecutter generated output.
    """

    diff, intersection = compare(out_dir, '.')

    if len(diff) > 0:
        logging.info('Copying different files')

    for p in diff:
        src_file, dst_dir, dst_file = gen_file_path(out_dir, p.replace(out_dir + "/", ''), '.')
        cpy(src_file, dst_dir)

    if len(intersection) > 0:
        logging.info('Copying already existing files')

    for p in intersection:
        src_file, dst_dir, dst_file = gen_file_path(out_dir, p.replace(out_dir + "/", ''), '.')

        # try to figure out whether same file already exists using hash
        new_file_hash = file_hash(src_file)
        old_file_hash = file_hash(dst_file)

        if new_file_hash == old_file_hash:
            logging.info('Same file already exists. Not changing')

        else:
            np = find_unused_name(p)
            logging.info('Moving old files: {} -> {}'.format(os.path.normpath(p), os.path.normpath(np)))
            shutil.copy(p, np)
            cpy(src_file, dst_dir)


@argh.arg('path', help="Path of cookiecutter template")
@argh.arg('--extra-config', help="Extra configurations in json format.", default='{}', type=json.loads)
def process(path, extra_config=None):
    """
    Process cookiecutter template. This function assumes there is a ``cookiecutter.json`` in
    the local directory.
    It will generate the files in ``.ccx_archive` directory first then copy to the current directory.
    If there is already a file then old file is backed up and replaced with new one.

    :param path: Path to the template
    :param extra_config: Extra configurations as json string
    """
    if not extra_config:
        extra_config = {}

    if not os.path.exists(path):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'example-templates', path)

    if not os.path.exists(path):
        logging.error("Path not found.")

    path = os.path.normpath(path)
    logging.info('Processing cookie cutter template at: {}'.format(path))

    local_cc = os.path.join('.', 'cookiecutter.json')
    if not os.path.exists(local_cc):
        logging.error('Local config file does not exist. Please provide local context json file.')
        return

    extra_context = read_json(local_cc)
    extra_context['ccx_output_directory'] = os.path.abspath('.')
    extra_context.update(extra_config)

    logging.info('Read context data: ' + os.linesep + json.dumps(extra_context, indent=4))

    archive_path = '.ccx_archive'
    template_name = os.path.basename(path)
    out_dir = os.path.normpath(os.path.join(archive_path, template_name))
    mkdirs(out_dir)

    cookiecutter(path, no_input=True, extra_context=extra_context, output_dir=out_dir)
    gen_dir = os.path.normpath(os.path.join(out_dir, extra_context['app_name']))

    if not os.path.exists(gen_dir):
        logging.error('Generated output should be inside \'app_name\' directory.')
        return

    copy_gen_files(gen_dir)


@argh.arg('-d', '--description', help="Description of the app", default='')
@argh.arg('-g', '--gitignore', help="Generate/update .gitignore to skip .ccx_archive folder", default='True')
def init(name, name_title, description='', gitignore='True'):
    if not app_name_rx.match(name):
        logging.error('App name can contain only alphabets, numbers, and underscore')
        return

    app_dir = os.path.join('.', name)
    if os.path.exists(app_dir):
        logging.error('App directory already exists')
        return

    logging.info('Creating directory: {}'.format(app_dir))
    os.mkdir(app_dir, 0755)

    local_cc = os.path.join(app_dir, 'cookiecutter.json')

    content = OrderedDict()
    content['app_name'] = name
    content['app_name_title'] = name_title
    content['app_description'] = description

    with open(local_cc, 'w') as f:
        content_json = json.dumps(content, indent=4)
        logging.info('Writing file: {}'.format(local_cc))
        f.write(content_json)
        f.write(os.linesep)

    if boolean(gitignore):
        gitignore_file = os.path.join(app_dir, '.gitignore')
        logging.info('Writing file: {}'.format(gitignore_file))
        with open(gitignore_file, 'w') as g:
            g.write('.ccx_archive')
            g.write(os.linesep)


@argh.arg('-s', '--script-name', help="Generate argh script", default='run.py')
@argh.arg('-c', '--colored-logs', help="Colored logs", default='False')
def argh_script(script_name='run.py', colored_logs='False'):
    if os.path.isabs(script_name):
        out_path = script_name
    else:
        out_path = os.path.join('.', script_name)

    if os.path.exists(out_path):
        logging.error('Path exists.')
        return

    if boolean(colored_logs):
        in_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data', 'argh_scripts', 'script_colored_logs.py'
        )
    else:
        in_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data', 'argh_scripts', 'script_normal_logs.py'
        )

    logging.info('Creating argh script: {}'.format(out_path))
    shutil.copyfile(in_path, out_path)


parser = argh.ArghParser()
parser.add_commands([process, init, argh_script])

if __name__ == '__main__':
    logging_format = '[%(asctime)s] %(levelname)s: %(message)s'
    logging.basicConfig(format=logging_format, level=logging.INFO)

    parser.dispatch()
