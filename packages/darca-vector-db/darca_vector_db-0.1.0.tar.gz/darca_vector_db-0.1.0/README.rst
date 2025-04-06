darca-vector-db
===============

A pluggable vector database client system with backend support. Currently, the only supported backend is Qdrant.
This project provides a unified client interface to interact with vector databases. It is designed to be easily extensible to support additional backends in the future.

|Build Status| |Deploy Status| |CodeCov| |Formatting| |License| |PyPi Version| |Docs|

.. |Build Status| image:: https://github.com/roelkist/darca-vector-db/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/roelkist/darca-vector-db/actions
.. |Deploy Status| image:: https://github.com/roelkist/darca-vector-db/actions/workflows/cd.yml/badge.svg
   :target: https://github.com/roelkist/darca-vector-db/actions
.. |Codecov| image:: https://codecov.io/gh/roelkist/darca-vector-db/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/roelkist/darca-vector-db
   :alt: Codecov
.. |Formatting| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black code style
.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
.. |PyPi Version| image:: https://img.shields.io/pypi/v/darca-vector-db
   :target: https://pypi.org/project/darca-vector-db/
   :alt: PyPi
.. |Docs| image:: https://img.shields.io/github/deployments/roelkist/darca-vector-db/github-pages
   :target: https://roelkist.github.io/darca-vector-db/
   :alt: GitHub Pages

GitHub Repository:
------------------
Visit the official repository at: `darca-vector-db on GitHub <https://github.com/roelkist/darca-vector-db>`_

Installation
------------
The project uses `Poetry` for dependency management and virtual environment handling.

To set up the project locally, follow these steps:

1. Clone the repository:
   .. code-block:: bash

       git clone https://github.com/roelkist/darca-vector-db.git
       cd darca-vector-db

2. Install dependencies and set up the environment with a single command:
   .. code-block:: bash

       make install

This command will handle creating the virtual environment, installing Poetry, and installing dependencies.

Make Targets for Faster Iterations
-----------------------------------
You can use specific make targets for faster development cycles:

- `make format`  : Formats the codebase using `black` and `isort`.
- `make test`    : Runs the test suite with coverage reporting.
- `make docs`    : Builds the documentation using Sphinx.
- `make check`   : Runs all checks (formatting, testing, docs) before committing.

Always run `make check` before committing changes to ensure consistency and quality.


3. Running tests:
   .. code-block:: bash

       make test

4. Formatting the code:
   .. code-block:: bash

       make format

5. Building the documentation:
   .. code-block:: bash

       make docs

Features
--------
- Unified client interface for vector databases
- Qdrant support
- Easy to extend for additional backends
- Structured logging and error handling
- Flexible CI and local environment support
- Automated testing and code formatting

Usage
-----
To use the client, instantiate it with the desired backend (currently only Qdrant is supported):

.. code-block:: python

    from darca_vector_db import DBClient

    client = DBClient(backend="qdrant", host="localhost", port=6333)
    client.connect()
    client.create_collection(name="my_vectors", vector_size=128, distance_metric="cosine")
    client.insert_vector("my_vectors", vector_id=1, vector=[0.1] * 128, metadata={"label": "example"})
    results = client.search_vectors("my_vectors", query_vector=[0.1] * 128, top_k=5)
    print(results)

Contributing
------------
Contributions are welcome! Please refer to the `CONTRIBUTING.rst` for detailed guidelines.

License
-------
MIT License

Author
------
Roel Kist

