# Tests

Tests for this product are set up with `pytest`.

## Run Tests With `pytest`

```bash
$ pytest
...............                                                                                                                                                                                                        [100%]
15 passed in 6.24s
```

## Run Tests and Display Code Coverage

```bash
$ pytest --cov=netflix_open_content_helper
...............                                                                                                                                                                                                        [100%]
======================================================================================================= tests coverage =======================================================================================================
______________________________________________________________________________________ coverage: platform darwin, python 3.13.2-final-0 ______________________________________________________________________________________

Name                                          Stmts   Miss  Cover
-----------------------------------------------------------------
src/netflix_open_content_helper/__init__.py      10      1    90%
src/netflix_open_content_helper/__main__.py       4      4     0%
src/netflix_open_content_helper/cli.py           87      5    94%
-----------------------------------------------------------------
TOTAL                                           101     10    90%
15 passed in 6.32s
```

## Run Tests and Generate Code Coverage HTML Report

```bash
$ pytest --cov=netflix_open_content_helper --cov-report=html
...............                                                                                                                                                                                                        [100%]
======================================================================================================= tests coverage =======================================================================================================
______________________________________________________________________________________ coverage: platform darwin, python 3.13.2-final-0 ______________________________________________________________________________________

Coverage HTML written to dir htmlcov
15 passed in 6.32s
```

Open ./htmlcov/index.html in a web browser to inspect details of the test results.
