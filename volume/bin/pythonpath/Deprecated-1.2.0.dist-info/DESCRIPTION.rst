Deprecated Library
------------------

Deprecated is Easy to Use
`````````````````````````

If you need to mark a function or a method as deprecated,
you can use the ``@deprecated`` decorator:

Save in a hello.py:

.. code:: python

    from deprecated import deprecated


    @deprecated(version='1.2.0', reason="You should use another function")
    def some_old_function(x, y):
        return x + y


    class SomeClass(object):
        @deprecated(version='1.3.0', reason="This method is deprecated")
        def some_old_method(self, x, y):
            return x + y


    some_old_function(12, 34)
    obj = SomeClass()
    obj.some_old_method(5, 8)


And Easy to Setup
`````````````````

And run it:

.. code:: bash

    $ pip install Deprecated
    $ python hello.py
    hello.py:15: DeprecationWarning: Call to deprecated function (or staticmethod) some_old_function.
    (You should use another function) -- Deprecated since version 1.2.0.
      some_old_function(12, 34)
    hello.py:17: DeprecationWarning: Call to deprecated method some_old_method.
    (This method is deprecated) -- Deprecated since version 1.3.0.
      obj.some_old_method(5, 8)


You can document your code
``````````````````````````

Have you ever wonder how to document that some functions, classes, methods, etc. are deprecated?
This is now possible with the integrated Sphinx directives:

For instance, in hello_sphinx.py:

.. code:: python

    from deprecated.sphinx import deprecated
    from deprecated.sphinx import versionadded
    from deprecated.sphinx import versionchanged


    @versionadded(version='1.0', reason="This function is new")
    def function_one():
        '''This is the function one'''


    @versionchanged(version='1.0', reason="This function is modified")
    def function_two():
        '''This is the function two'''


    @deprecated(version='1.0', reason="This function will be removed soon")
    def function_three():
        '''This is the function three'''


    function_one()
    function_two()
    function_three()  # warns

    help(function_one)
    help(function_two)
    help(function_three)


The result it immediate
```````````````````````

Run it:

.. code:: bash

    $ python hello_sphinx.py

    hello_sphinx.py:23: DeprecationWarning: Call to deprecated function (or staticmethod) function_three.
    (This function will be removed soon) -- Deprecated since version 1.0.
      function_three()  # warns

    Help on function function_one in module __main__:

    function_one()
        This is the function one

        .. versionadded:: 1.0
           This function is new

    Help on function function_two in module __main__:

    function_two()
        This is the function two

        .. versionchanged:: 1.0
           This function is modified

    Help on function function_three in module __main__:

    function_three()
        This is the function three

        .. deprecated:: 1.0
           This function will be removed soon


Links
`````

* `Python package index (PyPi) <https://pypi.python.org/pypi/deprecated>`_
* `GitHub website <https://github.com/tantale/deprecated>`_
* `Read The Docs <https://readthedocs.org/projects/deprecated>`_
* `EBook on Lulu.com <http://www.lulu.com/commerce/index.php?fBuyContent=21305117>`_
* `StackOverFlow Q&A <https://stackoverflow.com/a/40301488/1513933>`_
* `Development version
  <https://github.com/tantale/deprecated/zipball/master#egg=Deprecated-dev>`_



