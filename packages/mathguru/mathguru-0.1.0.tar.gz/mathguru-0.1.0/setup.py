from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
readme = (this_directory / "README.md").read_text(encoding="utf-8") if (this_directory / "README.md").exists() else ""

setup(
    name='mathguru',  
    version='0.1.0',
    description='A mathematics library for data science, development, and educational use.',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/narendrasingh-tech/mathguru',
    author='Narendra Singh',
    author_email='narendra@example.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    keywords='math mathematics data-science education numpy', 
    packages=find_packages(exclude=["tests*", "docs*"]),
    python_requires='>=3.7',
    install_requires=[
        'numpy>=1.21.0',
    ],
    include_package_data=True,
    project_urls={
        "Bug Tracker": "https://github.com/narendrasingh-tech/mathguru/issues",
        "Source Code": "https://github.com/narendrasingh-tech/mathguru",
    },
)
