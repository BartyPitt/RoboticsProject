Miscellaneous
==================

Documentation Instructions
---------------------------

We create this documentation that you are seeing now with ``sphinx`` documentation generator.
If you are creating the documentation for this project you will need to have ``sphinx`` installed on your computer.
It can be done by


.. code-block:: bash

    pip install sphinx             # for Windows
    apt-get install python-sphinx  # for Linux


You will also have to install ``recommonmark`` which can be done by

.. code-block:: bash

    pip install recommonmark       # for Windows
    apt-get install recommonmark   # for Linux



To compile and view your documentation, navigate to ``RoboticsProject/docs`` and open a terminal there. On your terminal, type in 


.. code-block:: bash

	make clean html

This should compile your .rst documentation files to html in the ``docs/_build/html`` folder. To view how the webpage would look like, navigate to the ``docs/_build/html`` folder and open ``index.html`` in your browser.
