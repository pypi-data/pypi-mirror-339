from setuptools import setup, find_packages

setup(
    name='GameForce',
    version='0.1a1',
    packages=find_packages(),
    include_package_data=True,  # aby uwzględniał dane niebędące kodem
    package_data={
        '': ['*.json'],  # dołączenie plików .json z każdego katalogu
    },
    description='This library is a toolkit for creating simple 2D games using the Pygame library. It allows the management of the map, objects, collisions, meshes and events. It is a flexible library that can be used to build different types of 2D games, such as puzzle, arcade or platform games. Thanks to its powerful classes, users can easily create objects, define events and manage movement and collisions on the map.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Franciszek Chmielewski',
    author_email='ferko2610@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',  # pre-release status
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
