from setuptools import setup, find_packages

setup(
    name='vital-graph',
    version='0.0.1',
    author='Marc Hadfield',
    author_email='marc@vital.ai',
    description='VitalGraph',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vital-ai/vital-graph',
    packages=find_packages(exclude=["test", "rdflib_sqlalchemy"]),
    entry_points={
        
    },

    license='Apache License 2.0',
    install_requires=[
        "pytidb[models]",
        "pytidb",
        "python-dotenv",
        "rdflib>=7.1.4",
        "six>=1.7.0",
        "alembic>=0.8.8",
        "SQLAlchemy>=2.0.23",
    ],

    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
