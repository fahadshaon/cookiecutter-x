# Needed a way to generate cookiecutter output to a specific directory.
# Even though cookiecutter's generate function has a output directory parameter,
# none of the external functions have output directory parameter.
# So blindly copied the ``cookiecutter`` function from ``cookiecutter.main`` module and
# added an optional argument ``output_dir``, which is simply passed to ``generate_files`` function.
# I am well aware of the future maintenance issues and I am not happy about it either :(


from cookiecutter.main import *


def cookiecutter(template, checkout=None, no_input=False, extra_context=None, output_dir=None):
    """
    API equivalent to using Cookiecutter at the command line.

    :param template: A directory containing a project template directory,
        or a URL to a git repository.
    :param checkout: The branch, tag or commit ID to checkout after clone.
    :param no_input: Prompt the user at command line for manual configuration?
    :param extra_context: A dictionary of context that overrides default
        and user configuration.
    :param output_dir: Output directory
    """

    # Get user config from ~/.cookiecutterrc or equivalent
    # If no config file, sensible defaults from config.DEFAULT_CONFIG are used
    config_dict = get_user_config()

    template = expand_abbreviations(template, config_dict)

    # TODO: find a better way to tell if it's a repo URL
    if 'git@' in template or 'https://' in template:
        repo_dir = clone(
            repo_url=template,
            checkout=checkout,
            clone_to_dir=config_dict['cookiecutters_dir'],
            no_input=no_input
        )
    else:
        # If it's a local repo, no need to clone or copy to your
        # cookiecutters_dir
        repo_dir = template

    context_file = os.path.join(repo_dir, 'cookiecutter.json')
    logging.debug('context_file is {0}'.format(context_file))

    context = generate_context(
        context_file=context_file,
        default_context=config_dict['default_context'],
        extra_context=extra_context,
    )

    # prompt the user to manually configure at the command line.
    # except when 'no-input' flag is set
    context['cookiecutter'] = prompt_for_config(context, no_input)

    # Create project from local context and project template.
    generate_files(
        repo_dir=repo_dir,
        context=context,
        output_dir=output_dir
    )
