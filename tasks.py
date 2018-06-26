from invoke import Collection

from invocations import docs, travis
from invocations.checks import blacken
from invocations.packaging import release
from invocations.pytest import test, coverage


ns = Collection(release, test, coverage, docs, travis, blacken)
ns.configure(
    {
        "packaging": {
            "sign": True,
            "wheel": True,
            "changelog_file": "docs/changelog.rst",
        },
        "run": {
            "env": {
                # Our ANSI color tests test against hardcoded codes appropriate
                # for this terminal, for now.
                "TERM": "xterm-256color"
            }
        },
        "travis": {"black": {"version": "18.6b4"}},
    }
)
