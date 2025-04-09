from setuptools import setup, find_packages

setup(
    name='n0elog',
    version='1.0.0',
    packages=find_packages(),
    author='n0byte',
    author_email='n0byte@proton.me',
    description='elog hilft dir besser und Simpler und einfacher alles zu loggen.',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/n0byte/elog',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)