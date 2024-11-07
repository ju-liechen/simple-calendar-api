def import_api_routes(api):
    """
    Scans all /apps directories for ./api/<folder>/__init__.py files and dynamically imports
    them. Those files intern reference the `api` object in this file to load their routes.

    Typically run in the urls.py file of the Django project

    Example:
        - /apps/user/api/public_signup/__init__.py
        - /apps/user/api/public_login/__init__.py
        - /apps/user/api/user_me/__init__.py

    """
    import sys
    from pathlib import Path
    import importlib

    root = Path(__file__).resolve().parent.parent.parent
    apps_path = root / 'apps'
    sys.path.append(str(root))  # Ensure the parent directory of 'apps' is in sys.path

    init_files = []
    # Collect all __init__.py files
    for api_path in apps_path.glob("*/api"):
        if api_path.is_dir():
            init_files.extend(api_path.glob("**/__init__.py"))

    # Sort the files based on their parent directory names
    sorted_files = sorted(init_files, key=lambda x: x.parent.stem)

    # Import modules from sorted __init__.py files
    for init_file in sorted_files:
        # Derive the module's dot notation path relative to the 'apps' directory
        relative_path = init_file.relative_to(apps_path).parent
        module_notation = '.'.join(relative_path.parts)

        # Ensure the module notation does not start or end with a dot
        if module_notation.startswith('.'):
            module_notation = module_notation[1:]
        if module_notation.endswith('.'):
            module_notation = module_notation[:-1]

        # Import the module using the corrected module notation
        importlib.import_module(f"apps.{module_notation}")

    return api
