from setuptools import setup , find_packages

setup (
    name = 'robotframework-roboai',
    version= '0.2.0',
    description='Custom AI-powered library for Robot Framework',
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