import sys
import click
import os
from easy_smr.commands.helpers import safe_run_subprocess
from easy_smr.config.config import ConfigManager

def _config(app_name):
    config_file_path = os.path.join(f'{app_name}.json')
    if not os.path.isfile(config_file_path):
        raise ValueError("This is not a easy_smr directory: {}".format(os.getcwd()))
    else:
        return ConfigManager(config_file_path).get_config()


def _build(source_dir, image_name, docker_tag):
    """
    Builds a Docker image that contains code under the given source root directory.

    Assumes that Docker is installed and running locally.

    :param source_dir: [str], source root directory
    :param image_name: [str], The name of the Docker image
    :param docker_tag: [str], the Docker tag for the image
    """
    easy_smr_module_path = os.path.relpath(os.path.join(source_dir, 'easy_smr_base/'))

    build_script_path = os.path.join(easy_smr_module_path, 'build.sh')
    dockerfile_path = os.path.join(easy_smr_module_path, 'Dockerfile')

    train_file_path = os.path.join(easy_smr_module_path, 'training', 'train')
    serve_file_path = os.path.join(easy_smr_module_path, 'prediction', 'serve')
    executor_file_path = os.path.join(easy_smr_module_path, 'executor.sh')

    if not os.path.isfile(build_script_path) or not os.path.isfile(train_file_path) or not \
            os.path.isfile(serve_file_path):
        raise ValueError("This is not a easy_smr directory: {}".format(source_dir))

    os.chmod(train_file_path, 0o777)
    os.chmod(serve_file_path, 0o777)
    os.chmod(executor_file_path, 0o777)

    target_dir_name = os.path.basename(os.path.normpath(source_dir))

    command = [
            "{}".format(build_script_path),
            "{}".format(os.path.relpath(source_dir)),
            "{}".format(os.path.relpath(target_dir_name)),
            "{}".format(dockerfile_path),
            docker_tag,
            image_name,
        ]
    safe_run_subprocess(command, "Docker image built successfully!")

@click.command()
@click.option(
    u"-a",
    u"--app-name",
    required=True,
    help="The app name whose json file will be referenced for setting up command"
)
@click.pass_obj
def build(obj, app_name):
    """
    Command to build SageMaker app
    """
    print("Started building SageMaker Docker image. It will take some minutes...\n")

    config = _config(app_name)
    _build(
        source_dir=config.easy_smr_module_dir,
        docker_tag=obj['docker_tag'],
        image_name=config.image_name,
        )
