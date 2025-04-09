from setuptools import setup , find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory/"README.md").read_text(encoding="utf-8")

setup (
    name = 'robotframework-roboai',
    version= '0.2.1',
    description='Custom AI-powered library for Robot Framework',
    long_description=long_description,
    long_description_content_type='text/markdown', 
    author='Mrigendra Kumar',
    license='MIT',
    packages=find_packages(),
    install_requires = [
        'openai',
        'robotframework',
        'python-dotenv',
    ],
    entry_points = {
        'robotframework_library' : [
            'AILibrary = ai_lib.ai_lib:AILibrary',
        ]
    },

    classifiers=[
        'Framework :: Robot Framework',
        'Programming Language :: Python :: 3',
    ],
)