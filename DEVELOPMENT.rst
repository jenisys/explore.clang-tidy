DEVELOPMENT ASPECTS
===============================================================================


PROGRAMMING LANGUAGES
-------------------------------------------------------------------------------

* C++: As source code examples for using `clang-tidy`_
* `Python`_: Used for many tools, like `clang-tidy`_ runners
* `Rust`_: Used for one `clang-tidy`_ runner

SEE ALSO:

* https://en.cppreference.com/w/cpp
* https://python.org (for python packages: https://pypi.org )
* https://www.rust-lang.org


.. _clang-tidy: https://releases.llvm.org/16.0.0/tools/clang/tools/extra/docs/clang-tidy/index.html
.. _Python: https://python.org
.. _Rust: https://www.rust-lang.org


VERSION CONTROL
-------------------------------------------------------------------------------

* DEFAULT BRANCH: Use "main" as default branch
* Use `git-subrepo`_ to manage additional git-repositories
* Use ``git subrepo status`` to show all sub-repository(s)

GIT-SUBREPOSITORIES:

* clang-tidy-mistakes: https://github.com/polystat/clang-tidy-mistakes.git


RELATED TO: `git-subrepo`_

* https://github.com/ingydotnet/git-subrepo
* Article on: http://blog.s-schoener.com/2019-04-20-git-subrepo/

.. _git-subrepo: https://github.com/ingydotnet/git-subrepo


USE: direnv
-------------------------------------------------------------------------------

Use `direnv`_ to:

* on entering the directory: setup environment variables for this project
* on entering the directory: setup and activate a Python ``virtualenv``
* on leaving the directory: clean up and resotore the old state restored

FILE(s):

* `.envrc <.envrc>`_

SEE ALSO:

* https://direnv.net/
* https://github.com/direnv/direnv

.. _direnv: https://direnv.net/
