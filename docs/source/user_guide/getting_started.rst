.. _getting-started:

################################################################################
Getting Started
################################################################################

Profkit is under development and it cannot yet be installed via PyPi. It has to installed from source, and the latest source code is available in the `Github repository <https://github.com/sinel/profkit>`_.

Requirements
================================================================================

Profkit depends on many requirements which are all specified and maintained by the ``pyproject.toml`` file in the root directory of its Github repository.

Installing from source
================================================================================

You may use pip (or, in a similar manner, any other dependency manager such as Poetry) to install Profkit and use it as a library.

.. code-block:: python

    python -m pip install profkit@git+https://github.com/sinel/profkit

The installation can be verified using:

.. code-block:: python

    import profkit

    profkit.about()
