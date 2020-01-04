from setuptools import setup

requires = [
    'prettytable',
    'sqlparse',
    'moz_sql_parser',
    'sqlalchemy'
]

tests_require = [
    'pytest<5',  # includes virtualenv
    'pytest-cov'
]

docs_require = [
    'sphinx',
    'sphinx-autobuild'
]

setup(
    name='SQL_Autocorrect',
    version='0.0.2',
    packages=['sql_autocorrect'],
    url='',
    license='',
    author='Rafaël Lopez',
    author_email='rafael.lopez@u-psud.fr',
    description='Logiciel d\'aide à la correction des requêtes SQL',
    include_package_data=True,
    zip_safe=False,
    test_suite='introbd',
    install_requires=requires,
    extras_require={
        'testing': tests_require,
        'docs': docs_require,
    },
    entry_points="""\
    [console_scripts]
    sql-autocorrect = sql_autocorrect.cli.parser:main
    sql-ac-res = sql_autocorrect.cli.reader:affiche_resultat
    """,
)
