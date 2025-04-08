from setuptools import setup

setup(
    name='quillpy',
    version='0.1.0',
    description='A lightweight terminal-based text editor',
    author='mralfiem591',
    author_email='iamamccabe@gmail.com',
    url='https://github.com/mralfiem591/quillpy',
    license='MIT',
    python_requires='>=3.6',
    project_urls={
        'Bug Tracker': 'https://github.com/mralfiem591/quillpy/issues',
        'Source Code': 'https://github.com/mralfiem591/quillpy',
    },
    packages=['quillpy'],
    install_requires=[
        'windows-curses; platform_system=="Windows"',
        'pywin32; platform_system=="Windows"'
    ],
    entry_points={
        'console_scripts': [
            'quillpy=quillpy.quill:main'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Text Editors :: Documentation',
        'Topic :: Utilities',
        'Operating System :: OS Independent',
    ]
)
