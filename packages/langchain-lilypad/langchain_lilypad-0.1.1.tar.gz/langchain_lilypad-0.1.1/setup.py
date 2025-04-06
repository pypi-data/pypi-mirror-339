from setuptools import setup, find_packages

setup(
    name='langchain_lilypad',
    version='0.1.1',
    author='Altaga',
    author_email='altaga@protonmail.com',
    description='The  module defines a custom chat model that interacts with the Lilypad API to generate conversational responses and bind tools for enhanced functionality, with mechanisms for parsing tool calls and customizing message payloads.',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)