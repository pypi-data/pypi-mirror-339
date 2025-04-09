from setuptools import Extension, setup

# FIXME: replace with ext-modules in pyproject.toml once we depend upon
# setuptools >= 74.1.0.
setup(
    ext_modules=[
        Extension(
            "igwn_ligolw.tokenizer",
            [
                "igwn_ligolw/tokenizer.c",
                "igwn_ligolw/tokenizer.Tokenizer.c",
                "igwn_ligolw/tokenizer.RowBuilder.c",
                "igwn_ligolw/tokenizer.RowDumper.c",
            ],
            include_dirs=["igwn_ligolw"],
        ),
    ],
)
