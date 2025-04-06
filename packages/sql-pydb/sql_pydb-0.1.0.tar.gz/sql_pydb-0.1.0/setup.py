from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="sql_pydb",
    version="0.1.0",
    packages=find_packages(),
    description='A Python package for simplified SQL operations across MSSQL, PostgreSQL, MySQL, and SQLite.',
    url='https://github.com/dwarakhnv/SQLPy',
    install_requires=[
        'pandas>=1.3.0',         
        'numpy>=1.21.0',         
        'pyodbc>=4.0.30',        
        'python-dateutil>=2.8.1',
    ],
    entry_points={
        "console_scripts": [
            # CLI Command = Module:Function
            # "sqlpydb = SQLPy.__main__:main",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.8',
)


# python setup.py sdist bdist_wheel
# pip install ../SQLPy/dist/SQLPy-0.1.0-py3-none-any.whl --force-reinstall
