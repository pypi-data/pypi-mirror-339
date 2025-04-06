# cppcheck-suppressor

A tool that creates suppression files from Cppcheck output. The created suppression file can be used as a baseline to run further Cppcheck analysis, highlighting any new errors in the analyzed code.

__Setting a baseline helps to see new issues. However, all the errors reported by Cppcheck should be reviewed with care.__

## Installation

Install the latest cppcheck-suppressor python module with

```bash
pip install cppcheck-suppressor
```

## Usage

To use the cppcheck-suppressor together with Cppcheck, first make a throughout analysis of your project with Cppcheck without any suppressions and save the results to a xml file:

```bash
cppcheck --xml src/ 2> cppcheck_errors.xml
```

This assumes your sources are in the `src/` folder. Use the arguments for Cppcheck that you would use otherwise - just no `--suppress` or `--suppress-xml` arguments, and keep the `--xml` argument.

Then use the cppcheck-suppressor to create a baseline from the Cppcheck results:

```bash
python -m cppcheck_suppressor -f cppcheck_errors.xml -o baseline.xml
```

And finally use the baseline in the further Cppcheck analyses:

```bash
cppcheck --suppress-xml=baseline.xml src/
```

Now, Cppcheck reports only new issues from the project. The baseline should be updated - especially when any errors are solved from the project.
