from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    readme = f.read()

with open('CHANGELOG', 'r') as f:
    changelog = f.read()

install_requires = []

if __name__ == "__main__":
    setup(
        name='gamenight',
        version='0.0.1',
        author='Alec Nikolas Reiter',
        author_email='alecreiter@gmail.com',
        description='Organize a game night!',
        long_description=readme + '\n\n' + changelog,
        license='MIT',
        packages=find_packages('src', exclude=["test"]),
        package_dir={'': 'src'},
        package_data={'': ['LICENSE', 'NOTICE', 'README.rst', 'CHANGELOG']},
        include_package_data=True,
        zip_safe=False,
        url="https://github.com/justanr/gamenight",
        install_requires=install_requires
    )
