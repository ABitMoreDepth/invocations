import pytest

from invocations.checks import blacken


class checks:
    class blacken_:
        @pytest.mark.parametrize(
            "kwargs,command",
            [
                (dict(), "find . -name '*.py' | xargs black -l 79"),
                (
                    dict(line_length=80),
                    "find . -name '*.py' | xargs black -l 80",
                ),
                (
                    dict(folder=["foo", "bar"]),
                    "find foo bar -name '*.py' | xargs black -l 79",
                ),
                (
                    dict(check=True),
                    "find . -name '*.py' | xargs black -l 79 --check",
                ),
                (
                    dict(diff=True),
                    "find . -name '*.py' | xargs black -l 79 --diff",
                ),
                (
                    dict(
                        diff=True,
                        check=True,
                        line_length=80,
                        folder=["foo", "bar"],
                    ),
                    "find foo bar -name '*.py' | xargs black -l 80 --check --diff",  # noqa
                ),
                (
                    dict(find_opts="-and -not -name foo"),
                    "find . -name '*.py' -and -not -name foo | xargs black -l 79",  # noqa
                ),
            ],
            ids=[
                "base case is all files and 79 characters",
                "line length controllable",
                "folders controllable",
                "check flag passed through",
                "diff flag passed through",
                "most args combined",
                "find opts controllable",
            ],
        )
        def runs_black(self, ctx, kwargs, command):
            blacken(ctx, **kwargs)
            ctx.run.assert_called_once_with(command, pty=True)

        def folder_configurable(self, ctx):
            # Just config -> works fine
            ctx.blacken = dict(folders=["elsewhere"])
            blacken(ctx)
            assert "elsewhere" in ctx.run.call_args[0][0]

        def folder_config_loses_to_runtime(self, ctx):
            # Config + CLI opt -> CLI opt wins
            ctx.blacken = dict(folders=["nowhere"])
            blacken(ctx, folder=["nowhere"])
            assert "nowhere" in ctx.run.call_args[0][0]
