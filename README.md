oopsallyaml
===========

This is a pre-commit (https://pre-commit.com) hook that scans all YAML files in
your repository, and validates them against their schema.

Usage
-----

Add the following to your `.pre-commit-config.yaml`:

    - repo: https://github.com/hades/oopsallyaml
      rev: master
      hooks:
        - id: oopsallyaml

To prevent errors in the YAML files that have no schemas, the following comment
should be the first line of the YAML file:

    # no schema: <add an explanation why this file has no schema>

To add a YAML schema, add it to the `.yamlschemas` directory in the root of
your Git repository. The file name should be `<schema>.schema.yaml`. Then you
can declare the schema in your YAML files as follows:

    # schema: <schema>
