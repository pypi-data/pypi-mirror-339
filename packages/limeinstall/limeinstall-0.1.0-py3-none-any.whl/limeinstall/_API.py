import os
import subprocess
import sys
import tomllib
from importlib import util
from pathlib import Path
from typing import TYPE_CHECKING
# ======================================================================
# Hinting types
if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import NotRequired
    from typing import TypeAlias
    from typing import TypedDict
    from typing import Self

    PipType: TypeAlias = Callable[[list[str] | None], int]


    PathPattern: TypeAlias = str
    Option: TypeAlias = str
    Options: TypeAlias = set[Option]

    Flag: TypeAlias = str
    Flags: TypeAlias = set[Flag]

    class PackagesConfig(TypedDict):
        required: NotRequired[list[PathPattern]]
        optional: NotRequired[dict[Option, list[PathPattern]]]

    class RequirementsConfig(TypedDict):
        required: NotRequired[list[PathPattern]]
        optional: NotRequired[dict[Option, list[PathPattern]]]

    SubrepoRemote: TypeAlias = str
    SubrepoHead: TypeAlias = str
    SubrepoInfoRaw: TypeAlias = list[SubrepoHead | list[Option] | list[Flags]]

    class SubreposConfig(TypedDict):
        required: NotRequired[dict[SubrepoRemote, SubrepoInfoRaw]]
        optional: NotRequired[dict[Option, dict[SubrepoRemote, SubrepoInfoRaw]]]

    SubrepoInfo: TypeAlias = tuple[SubrepoHead, Options, Flags]
    Subrepos: TypeAlias = dict[SubrepoRemote, SubrepoInfo]

    class InstallConfig(TypedDict):
        packages: NotRequired[PackagesConfig]
        requirements: NotRequired[RequirementsConfig]
        subrepos: NotRequired[SubreposConfig]

    PyprojectProject = TypedDict('PyprojectProject',
        {'dependencies': NotRequired[list[str]],
         'optional-dependencies': NotRequired[dict[str, list[str]]],
         'dynamic': NotRequired[list[str]]})

    class DynamicDependencies(TypedDict):
        file: list[str]

    DynamicConfig = TypedDict('DynamicConfig',
        {'dependencies': NotRequired[DynamicDependencies],
         'optional-dependencies': NotRequired[dict[str, DynamicDependencies]]})

    class PyprojectBuildTool(TypedDict):
        dynamic: NotRequired[DynamicConfig]

    class Pyproject(TypedDict):
        project: PyprojectProject
        tool: NotRequired[dict[str, PyprojectBuildTool]]

else:
    PipType = Self = Option = Options = Flag = Flags = object

    SubrepoRemote = SubrepoHead = SubrepoInfoRaw = object

    SubrepoInfo = Subrepos = object

    PackagesConfig = RequirementsConfig = RequirementsConfig = object
    SubreposConfig = InstallConfig = object
# ======================================================================
# Parameters
ENV_VAR_PREFIX = 'REPO_'
# ======================================================================
def git(*args: str, capture_output: bool = False):
    return subprocess.run(('git', *args), capture_output = capture_output)
# ======================================================================
class working_directory:
    def __init__(self, path: Path) -> None:
        self.new = path
    def __enter__(self) -> Self:
        self.old = Path.cwd()
        os.chdir(self.new)
        return self
    def __exit__(self, *_) -> None:
        os.chdir(self.old)
# ======================================================================
def clone(remote: str, subrepo_name: str, path_subrepo: Path) -> None:

    if path_ref := os.environ.get(ENV_VAR_PREFIX + subrepo_name.upper()):
        print('\nCLONING USING REFERENCE\n')
        if not git('clone', '--reference-if-able', str(Path(path_ref) / '.git'),
                   '--dissociate', remote, str(path_subrepo)).returncode:
            return
    print('\nCLONING FROM UPSTREAM\n')
    git('clone', remote, str(path_subrepo))
# ======================================================================
def set_envvar(name: str, path: Path):
    envvar_name = ENV_VAR_PREFIX + name
    match sys.platform:
        case 'win32':
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment',
                                access = winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, envvar_name, 0, winreg.REG_SZ, str(path))
        case 'linux':
            with open(os.path.expanduser('~/.bashrc'), 'a') as f:
                f.write(f'export {envvar_name}="{path}"\n')

# ======================================================================
def install_requirements(args: Options,
                         config: RequirementsConfig,
                         pip: PipType) -> None:
    # Installing dependency lists
    if required := config.get('required'):
        for path in required:
            # Required dependencies
            pip(['install', '-r', str(Path(path))])

    if optional := config.get('optional'):
        # Optional dependencies
        for option, paths in optional.items():
            if option in args:
                for path in paths:
                    pip(['install', '-r', str(Path(path))])
# ======================================================================
def install_package(path_pyproject: Path, args: set[str], pip: PipType) -> None:

    param = str(path_pyproject.parent)

    print(f'Installing {param}')
    try:
        with open(path_pyproject, mode = 'rb') as f:
            pyproject: Pyproject = tomllib.load(f) # type: ignore[assignment]
    except FileNotFoundError:
        param += f'[{",".join(args)}]'
    else:
        project_config = pyproject['project']
        options: set[str]
        if options_dict := project_config.get('optional-dependencies'):
            if options := args.union(options_dict.keys()):
                param += f'[{",".join(options)}]'

        elif dynamic := project_config.get('dynamic'):
            if 'optional-dependencies' in dynamic:
                tools_config = pyproject['tool']
                for tool in ('setuptools',):
                    if tool_config :=  tools_config.get(tool):
                        if options := args.union(
                            tool_config['dynamic'
                                        ]['optional-dependencies'
                                          ].keys()
                            ):
                            param += f'[{",".join(options)}]'
                        break
            else:
                raise NotImplementedError('No supported tool found for optional dependencies')

    pip(['install', '-e', param])
# ======================================================================
def install_packages(args: Options,
                     config: PackagesConfig,
                     pip: PipType
                     ) -> None:
    path_cwd = Path.cwd()

    if patterns_optional := config.get('required'):
        for pattern in patterns_optional:
            for path in path_cwd.glob(pattern + '/pyproject.toml'):
                install_package(path, args, pip)

    if optional := config.get('optional'):
        for option, patterns_optional in optional.items():
            if option in args:
                optlen = len(option) + 1
                subargs = {arg[optlen:] for arg in args
                            if arg.startswith(option + '-')}
                for pattern in patterns_optional:
                    for path in path_cwd.glob(pattern + '/pyproject.toml'):
                        install_package(path, subargs, pip)
# ======================================================================
def _update_subrepo_info(flags: Flags,
                         remote: SubrepoRemote,
                         option: Option,
                         info: SubrepoInfoRaw,
                         sub_flag: Flag,
                         subrepos: Subrepos) -> None:

    head: str
    options: list[str]
    sub_flags: list[str]

    head, options, sub_flags = info # type: ignore[assignment]

    # Arg in optional repos
    if (previous := subrepos.get(remote)) is None:
        # Subrepo included for the first time
        _sub_flag_set = flags.union(sub_flags)
        _sub_flag_set.add(sub_flag)
        subrepos[remote] = (head,
                            set(options),
                            _sub_flag_set)
    else:

        previous_head, previous_options, previous_flags = previous

        #                previous
        #    |     |    0    |    A   |
        #    | :-: | :-----: | :----: |
        # n  |  0  | update  | update |
        # e  |  A  | replace | update |
        # w  |  B  | replace | error  |

        if previous_head:
            if head and head != previous_head:
                print(f"ERROR: Conflicting head requirements for '{remote}'. "
                      f"Option '{option}' requires '{head}', "
                      f"but '{previous_head}' was already required. Ignoring",
                      file = sys.stderr)
            else:
                previous_options.update(options)

                if sub_flag:
                    previous_flags.add(sub_flag)
                previous_flags.update(sub_flags)
        else:
            previous_options.update(options)

            if sub_flag:
                previous_flags.add(sub_flag)
            previous_flags.update(sub_flags)

            if head: # Replace
                subrepos[remote] = (head,
                                    previous_options,
                                    previous_flags)
# ======================================================================
def _parse_subrepos(args: Options, flags: Flags, config: SubreposConfig
                    ) -> Subrepos:
    subrepos: Subrepos
    subrepos = ({key: (value[0], set(value[1]), set(value[2])) # type: ignore[misc, arg-type]
                 for key, value in required.items()}
                if (required := config.get('required'))
                else {})

    if not (optional := config.get('optional')):
        return subrepos
    for arg in args:
        option, _, sub_flag = arg.rpartition('-')
        if option_repos := optional.get(option):
            for remote, info in option_repos.items():
                _update_subrepo_info(
                    flags, remote, option, info, sub_flag, subrepos)
    return subrepos
# ======================================================================
def install_subrepos(args: Options,
                      flags: Flags,
                      config: SubreposConfig,
                      cloned_subrepos: dict[SubrepoRemote, Path],
                      path_subrepos: Path,
                      pip: PipType
                      ) -> None:

    subrepos = _parse_subrepos(args, flags, config)

    path_subrepos.mkdir(exist_ok = True)

    for remote, (head, subrepo_args, subrepo_flags) in subrepos.items():
        if (path_subrepo := cloned_subrepos.get(remote)) is None:
            subrepo_name = _name_from_remote(remote)

            print(f"Installing '{subrepo_name}'")
            if (path_subrepo := path_subrepos / subrepo_name).exists():

                print(f"Repository '{subrepo_name}' already exists")
                with working_directory(path_subrepo):
                    git('fetch')
                    if head:
                        git('checkout', head)
                    git('pull')
            else:
                clone(remote, subrepo_name, path_subrepo)
                with working_directory(path_subrepo):
                    if head:
                        git('checkout', head)

            cloned_subrepos[remote] = path_subrepo

        spec = util.spec_from_file_location('install',
                                            path_subrepo / 'install.py')
        if spec is not None:
            try:
                installer = util.module_from_spec(spec) # type: ignore
                spec.loader.exec_module(installer) # type: ignore
                print(f"Running install script for '{subrepo_name}'")
                installer.install(subrepo_args, subrepo_flags, cloned_subrepos)
                return
            except Exception:
                pass
        install_package(path_subrepo, args, pip)
# ======================================================================
def install(args: set[str],
            flags: set[str],
            cloned_subrepos: dict[str, Path]) -> None:
    from pip._internal.cli.main import main as pip

    path_cwd = Path.cwd()
    # ------------------------------------------------------------------
    try:
        with open('install.toml', mode = 'rb') as f:
            config: InstallConfig = tomllib.load(f) # type: ignore[assignment]
    except FileNotFoundError:
        try:
            install_package(path_cwd, args, pip)
        except Exception:
            pass
        return
    # ------------------------------------------------------------------
    # Installing requirements lists
    if requirements_config := config.get('requirements'):
        install_requirements(args, requirements_config, pip)
    # ------------------------------------------------------------------
    # Installing packages
    if packages_config := config.get('packages'):
        install_packages(args, packages_config, pip)
    # ------------------------------------------------------------------
    # Installing dev tools
    if '--dev' in flags:
        subprocess.run(('pre-commit', 'install', '--install-hooks'))
    # ------------------------------------------------------------------
    # Installing subrepos
    if subrepos_config := config.get('subrepos'):
        install_subrepos(args, flags, subrepos_config, cloned_subrepos,
                         path_cwd / '.subrepos', pip)

# ======================================================================
def _name_from_remote(remote: str):
    return remote.split('/', 1)[1].split('.git', 1)[0]
# ======================================================================
def main(cli_args: list[str] | None = None,
         path_repo: Path | None = None) -> int:
    """Runs the installation for this repository."""
    if cli_args is None:
        cli_args = sys.argv[1:]
    if path_repo is None:
        path_repo = Path.cwd()
    # ------------------------------------------------------------------
    # arguments processing
    flags: set[str] = set()
    args: set[str] = set()

    for arg in cli_args:
        if arg.startswith('--'):
            flags.add(arg)
        else:
            args.add(arg)

    if flags:
        _args = args.copy()
        for flag in flags:
            args.update(arg + flag[1:] for arg in _args)

        args.update(f[2:] for f in flags)
    # ------------------------------------------------------------------
    with working_directory(path_repo):

        remote = git('remote', '-v', capture_output = True
                     ).stdout.split(b' ', 2)[1].decode('utf-8')
        name = _name_from_remote(remote)

        set_envvar(name.upper(), path_repo)

        git('config', 'pull.rebase', 'true')

        subprocess.run((sys.executable,
                        '-m', 'pip', 'install', '--upgrade', 'pip'))

        install(args, flags, {remote: path_repo})
    return 0
