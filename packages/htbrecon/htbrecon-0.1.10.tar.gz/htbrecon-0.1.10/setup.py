from setuptools import setup, find_packages

setup(
    name='htbrecon',
    version='0.1.10',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'InquirerPy',
        'colorama',
        'openai'
    ],
    entry_points={
        'console_scripts': [
            'htbrecon=htbrecon.main:run',
        ],
    },
    author='l3str4nge',
    description='Auto-recon CLI tool for HTB machines',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Environment :: Console',
    ],
    python_requires='>=3.7',
)