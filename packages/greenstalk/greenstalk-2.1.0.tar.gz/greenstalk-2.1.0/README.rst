Greenstalk
==========

.. image:: https://img.shields.io/pypi/v/greenstalk.svg
    :target: https://pypi.org/project/greenstalk/
    :alt: Greenstalk on PyPI

Greenstalk is a small and unopinionated Python client library for communicating
with the `beanstalkd`_ work queue. The API provided mostly maps one-to-one with
commands in the `protocol`_.

Quickstart
----------

.. code-block:: pycon

    >>> import greenstalk
    >>> client = greenstalk.Client(('127.0.0.1', 11300))
    >>> client.put('hello')
    1
    >>> job = client.reserve()
    >>> job.id
    1
    >>> job.body
    'hello'
    >>> client.delete(job)
    >>> client.close()

Documentation is available on `Read the Docs`_.

.. _`beanstalkd`: https://beanstalkd.github.io/
.. _`protocol`: https://raw.githubusercontent.com/beanstalkd/beanstalkd/master/doc/protocol.txt
.. _`Read the Docs`: https://greenstalk.readthedocs.io/
