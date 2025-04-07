# Copyright 2024 John Sirois.
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import annotations

import asyncio
import dataclasses
import itertools
import os
import shlex
import sys
import time
from argparse import ArgumentParser
from asyncio import CancelledError
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Collection, DefaultDict, Iterable, Iterator, Mapping

from dev_cmd import __version__, color, parse, venv
from dev_cmd.color import ColorChoice
from dev_cmd.console import Console
from dev_cmd.errors import DevCmdError, ExecutionError, InvalidArgumentError
from dev_cmd.expansion import expand
from dev_cmd.invoke import Invocation
from dev_cmd.model import Command, Configuration, ExitStyle, Group, PythonConfig, Task, Venv
from dev_cmd.parse import parse_dev_config
from dev_cmd.placeholder import DEFAULT_ENVIRONMENT
from dev_cmd.project import find_pyproject_toml

DEFAULT_EXIT_STYLE = ExitStyle.AFTER_STEP
DEFAULT_GRACE_PERIOD = 5.0


def _iter_commands(
    steps: Iterable[Command | Group | Task], seen: set[Command] | None = None
) -> Iterator[Command]:
    seen = seen if seen is not None else set()
    for step in steps:
        if isinstance(step, Command):
            if step not in seen:
                seen.add(step)
                yield step
        elif isinstance(step, Task):
            for command in _iter_commands(step.steps.members, seen=seen):
                yield command
        else:
            for command in _iter_commands(step.members, seen=seen):
                yield command


def _ensure_venvs(
    steps: Iterable[Command | Task], pythons: Iterable[PythonConfig]
) -> Mapping[str, Venv]:
    pythons_to_requesting_commands: DefaultDict[str, list[Command]] = defaultdict(list)
    for command in _iter_commands(steps):
        if command.python:
            pythons_to_requesting_commands[command.python].append(command)

    if pythons_to_requesting_commands and not pythons:
        missing_pythons = "\n".join(
            f"+ {python!r} requested by: {' '.join(repr(rc.name) for rc in requesting_commands)}"
            for python, requesting_commands in pythons_to_requesting_commands.items()
        )
        raise InvalidArgumentError(
            f"Some of your configured commands requested custom pythons but you have not "
            f"configured any `[[tool.dev-cmd.python]]` entries.\n"
            f"See: https://github.com/jsirois/dev-cmd/blob/main/README.md#custom-pythons\n"
            f"\n"
            f"The missing pythons are:\n"
            f"{missing_pythons}"
        )

    venvs_by_python: dict[str, Venv] = {}
    for python, requesting_commands in pythons_to_requesting_commands.items():
        python_config = parse.select_python_config(python, pythons)
        if not python_config:
            commands = "\n".join(f"+ {rc.name}" for rc in requesting_commands)
            raise InvalidArgumentError(
                f"The following commands requested a custom Python of {python!r} but none of the "
                f"configured `[[tool.dev-cmd.python]]` entries apply:\n"
                f"{commands}"
            )
        venvs_by_python[python] = venv.ensure(python, python_config)
    return venvs_by_python


def _run(
    config: Configuration,
    *names: str,
    skips: Collection[str] = (),
    console: Console = Console(),
    parallel: bool = False,
    timings: bool = False,
    extra_args: Iterable[str] = (),
    exit_style_override: ExitStyle | None = None,
    grace_period_override: float | None = None,
) -> None:
    grace_period = grace_period_override or config.grace_period or DEFAULT_GRACE_PERIOD

    available_cmds = {cmd.name: cmd for cmd in config.commands}
    available_tasks = {task.name: task for task in config.tasks}

    missing_skips = sorted(
        skip for skip in skips if skip not in available_cmds and skip not in available_tasks
    )
    if missing_skips:
        if len(missing_skips) == 1:
            missing_skips_list = missing_skips[0]
        else:
            missing_skips_list = f"{', '.join(missing_skips[:-1])} and {missing_skips[-1]}"
        raise InvalidArgumentError(
            f"You requested skips of {missing_skips_list} which do not correspond to any "
            f"configured command or task names."
        )

    if names:
        try:
            invocation = Invocation.create(
                *(available_tasks.get(name) or available_cmds[name] for name in names),
                skips=skips,
                console=console,
                grace_period=grace_period,
                timings=timings,
                venv=config.venv,
            )
        except KeyError as e:
            raise InvalidArgumentError(
                os.linesep.join(
                    (
                        f"A requested task is not defined in {config.source}: {e}",
                        "",
                        f"Available tasks: {' '.join(sorted(available_tasks))}",
                        f"Available commands: {' '.join(sorted(available_cmds))}",
                    )
                )
            )
    elif config.default:
        invocation = Invocation.create(
            config.default,
            skips=skips,
            console=console,
            grace_period=grace_period,
            timings=timings,
            venv=config.venv,
        )
    else:
        raise InvalidArgumentError(
            os.linesep.join(
                (
                    f"usage: {sys.argv[0]} task|cmd [task|cmd...]",
                    "",
                    f"Available tasks: {' '.join(sorted(task.name for task in config.tasks))}",
                    f"Available commands: {' '.join(sorted(cmd.name for cmd in config.commands))}",
                )
            )
        )

    if extra_args and not invocation.accepts_extra_args:
        raise InvalidArgumentError(
            f"The following extra args were passed but none of the selected commands accept extra "
            f"arguments: {shlex.join(extra_args)}"
        )

    invocation = dataclasses.replace(
        invocation, venvs=_ensure_venvs(invocation.steps, config.pythons)
    )

    exit_style = exit_style_override or config.exit_style or DEFAULT_EXIT_STYLE
    return asyncio.run(
        invocation.invoke_parallel(*extra_args, exit_style=exit_style)
        if parallel
        else invocation.invoke(*extra_args, exit_style=exit_style)
    )


@dataclass(frozen=True)
class Options:
    tasks: tuple[str, ...]
    skips: frozenset[str]
    list: bool
    quiet: bool
    parallel: bool
    timings: bool
    extra_args: tuple[str, ...]
    python: str | None = None
    exit_style: ExitStyle | None = None
    grace_period: float | None = None


def _parse_args() -> Options:
    parser = ArgumentParser(
        description=(
            "A simple command runner to help running development tools easily and consistently."
        ),
    )
    parser.add_argument("-V", "--version", action="version", version=__version__)
    parser.add_argument(
        "-l",
        "--list",
        default=False,
        action="store_true",
        help="List the commands and tasks that can be run.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help=(
            "Do not output information about the commands `dev-cmd` is running; just show output "
            "from the commands run themselves."
        ),
    )
    parser.add_argument(
        "-s",
        "--skip",
        dest="skips",
        action="append",
        default=[],
        help=(
            "After calculating all steps to run given the command line args, remove these steps, "
            "whether they be command names or task names from that list."
        ),
    )
    parser.add_argument(
        "-p",
        "--parallel",
        action="store_true",
        help=(
            "Run all the top level command and task names passed in parallel. Has no effect unless "
            "there are two or more top level commands or tasks requested."
        ),
    )
    parser.add_argument(
        "-t",
        "--timings",
        action="store_true",
        help="Emit timing information for each command run.",
    )

    if venv.AVAILABLE:
        parser.add_argument(
            "--py",
            "--python",
            dest="python",
            help="Select an older python to run dev-cmd against.",
        )

    exit_style_group = parser.add_mutually_exclusive_group()
    exit_style_group.add_argument(
        "-k",
        "--keep-going",
        dest="exit_style",
        action="store_const",
        const=ExitStyle.END,
        help=(
            "Normally, `dev-cmd` exits with an error code after the first task step with an "
            "errored command completes. You can choose to `-k` / `--keep-going` to run all steps "
            "to the end before exiting. This option is mutually exclusive with "
            "`-X` / `--exit-style`."
        ),
    )
    exit_style_group.add_argument(
        "-X",
        "--exit-style",
        dest="exit_style",
        type=ExitStyle,
        choices=list(ExitStyle),
        default=None,
        help=(
            "When to exit a `dev-cmd` invocation that encounters command errors. Normally, "
            "`dev-cmd` exits with an error code after the first task step with an errored command "
            "completes. This option is mutually exclusive with `-k` / `--keep-going`."
        ),
    )

    parser.add_argument(
        "--grace-period",
        type=float,
        default=None,
        help=(
            "The amount of time in fractional seconds to wait for terminated commands to exit "
            f"before killing them forcefully: {DEFAULT_GRACE_PERIOD} seconds by default. If set to "
            f"zero or a negative value, commands are always killed forcefully with no grace "
            f"period. This setting comes into play when the `--exit-style` is either "
            f"{ExitStyle.AFTER_STEP.value!r} or {ExitStyle.IMMEDIATE.value!r}."
        ),
    )
    parser.add_argument(
        "--color",
        type=ColorChoice,
        choices=list(ColorChoice),
        default=ColorChoice.AUTO,
        help=(
            "When to color `dev-cmd` output. By default an appropriate color mode is "
            "'auto'-detected, but color use can be forced 'always' on or 'never' on."
        ),
    )
    parser.add_argument(
        "tasks",
        nargs="*",
        metavar="cmd|task",
        help=(
            "One or more names of `commands` or `tasks` to run that are defined in the "
            "[tool.dev-cmd] section of `pyproject.toml`. If no command or task names are passed "
            "and a [tool.dev-cmd] `default` is defined or there is only one command defined, that "
            "is run."
        ),
    )

    args: list[str] = []
    extra_args: list[str] | None = None
    for arg in sys.argv[1:]:
        if "--" == arg and extra_args is None:
            extra_args = []
        elif extra_args is not None:
            extra_args.append(arg)
        else:
            args.append(arg)

    options = parser.parse_args(args)
    color.set_color(ColorChoice(options.color))

    tasks = tuple(itertools.chain.from_iterable(expand(task) for task in options.tasks))
    parallel = options.parallel and len(tasks) > 1
    if options.parallel and not parallel and not options.quiet:
        single_task = repr(tasks[0]) if tasks else "the default"
        print(
            color.yellow(
                f"A parallel run of top-level tasks was requested but only one was requested, "
                f"{single_task}; so proceeding with a normal run."
            )
        )

    return Options(
        tasks=tasks,
        skips=frozenset(options.skips),
        list=options.list,
        quiet=options.quiet,
        parallel=parallel,
        timings=options.timings,
        extra_args=tuple(extra_args) if extra_args is not None else (),
        python=getattr(options, "python", None),
        exit_style=options.exit_style,
        grace_period=options.grace_period,
    )


def _list(
    console,  # type: Console
    config,  # type: Configuration
):
    # type: (...) -> Any

    console.print(f"{color.cyan('Commands')}:")
    hidden_command_count = len(tuple(command for command in config.commands if command.hidden))
    if hidden_command_count > 0:
        subject = "command is" if hidden_command_count == 1 else "commands are"
        print(color.color(f"({hidden_command_count} {subject} hidden.)", fg="gray"))
    seen: set[str] = set()
    for command in config.commands:
        command = command.base or command
        if command.name in seen:
            continue
        seen.add(command.name)
        if command.hidden:
            continue
        rendered_command_name = color.color(command.name, fg="magenta", style="bold")
        if config.default == command:
            rendered_command_name = f"* {rendered_command_name}"
        if command.accepts_extra_args:
            extra_args_help = color.magenta(f" (-- extra {command.args[0]} args ...)")
            rendered_command_name = f"{rendered_command_name}{extra_args_help}"
        if command.description:
            console.print(f"{rendered_command_name}:")
            console.print(f"    {color.color(command.description, fg='gray')}")
        elif command.factor_descriptions:
            console.print(f"{rendered_command_name}:")
        else:
            console.print(rendered_command_name)
        for factor_description in command.factor_descriptions:
            factor_desc_header = f"    -{factor_description.factor}"
            rendered_factor = color.magenta(factor_desc_header)
            default = factor_description.default
            if default:
                substituted_default = DEFAULT_ENVIRONMENT.substitute(default).value
                if substituted_default != default:
                    extra_info = f"[default: {default} (currently {substituted_default})]"
                else:
                    extra_info = f"[default: {default}]"
            else:
                extra_info = "[required]"
            if factor_description.description:
                desc_lines = factor_description.description.splitlines()
                console.print(f"{rendered_factor}: {color.color(desc_lines[0], fg='gray')}")
                for extra_line in desc_lines[1:]:
                    console.print(
                        f"{' ' * len(factor_desc_header)}  {color.color(extra_line, fg='gray')}"
                    )
                console.print(
                    f"{' ' * len(factor_desc_header)}  {color.color(extra_info, fg='gray')}"
                )
            else:
                console.print(f"{rendered_factor}: {color.color(extra_info, fg='gray')}")
    if config.tasks:
        console.print()
        console.print(f"{color.cyan('Tasks')}:")
        hidden_task_count = len(tuple(task for task in config.tasks if task.hidden))
        if hidden_task_count > 0:
            subject = "task is" if hidden_task_count == 1 else "tasks are"
            print(color.color(f"({hidden_task_count} {subject} hidden.)", fg="gray"))
        for task in config.tasks:
            if task.hidden:
                continue
            rendered_task_name = color.color(task.name, fg="magenta", style="bold")
            if config.default == task:
                rendered_task_name = f"* {rendered_task_name}"
            if extra_args_cmd := task.accepts_extra_args():
                extra_args_help = color.magenta(f" (-- extra {extra_args_cmd.args[0]} args ...)")
                rendered_task_name = f"{rendered_task_name}{extra_args_help}"
            if task.description:
                console.print(f"{rendered_task_name}: ")
                console.print(f"    {color.color(task.description, fg='gray')}")
            else:
                console.print(rendered_task_name)


def main() -> Any:
    start = time.time()
    options = _parse_args()
    console = Console(quiet=options.quiet)
    try:
        pyproject_toml = find_pyproject_toml()
        config = parse_dev_config(pyproject_toml, *options.tasks, requested_python=options.python)
    except DevCmdError as e:
        return 1 if console.quiet else f"{color.red('Configuration error')}: {color.yellow(str(e))}"

    if options.list:
        return _list(console, config)

    success = False
    try:
        _run(
            config,
            *options.tasks,
            skips=options.skips,
            console=console,
            parallel=options.parallel,
            timings=options.timings,
            extra_args=options.extra_args,
            exit_style_override=options.exit_style,
            grace_period_override=options.grace_period,
        )
        success = True
    except DevCmdError as e:
        if console.quiet:
            return 1
        return f"{color.red('Configuration error')}: {color.yellow(str(e))}"
    except OSError as e:
        if console.quiet:
            return 1
        return f"{color.color('Failed to launch a command', fg='red', style='bold')}: {color.red(str(e))}"
    except ExecutionError as e:
        if console.quiet:
            return e.exit_code
        prefix = f"{color.red('dev-cmd')} {color.color(e.step_name, fg='red', style='bold')}"
        return f"{prefix}] {color.red(e.message)}"
    except (CancelledError, KeyboardInterrupt):
        if console.quiet:
            return 1
        return f"{color.red('dev-cmd')}] {color.color('Cancelled', fg='red', style='bold')}"
    finally:
        if not console.quiet:
            summary_color = "green" if success else "red"
            status = color.color(
                "Success" if success else "Failure", fg=summary_color, style="bold"
            )
            timing = color.color(f"in {time.time() - start:.3f}s", fg=summary_color)
            console.print(f"{color.cyan('dev-cmd')}] {status} {timing}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
