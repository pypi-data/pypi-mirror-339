
from setuptools import setup, find_packages

"""
    BUILD INSTRUCTIONS
    ##################
    
    Create Python Virtual Environment
    ---------------------------------
        A virtual environment allows you to create a project, and install dependencies, isolated from
        other projects where differing package versions and variations have the potential to clash.
        
        First you need the tools to create a Python virtual environment. There are many popular options such as conda,
        venv (comes with versions of python) and virtualenv. To install virtualenv type the following into a prompt window:
            pip install virtualenv
        or:
            apt-get install virtualenv
        
        You now need a place to create your environment. You can do this by creating a new directory somewhere:
            cd Desktop
            mkdir ailie_build
            cd ailie_build
        
        With the tool installed we can now create an environment under a custom name. I am using the name "buildenv".
        Go to the projects intended directory and run:
            python -m venv buildenv
        
        Now the environment is created, we can activate it. This is done using the following command within the directory:
            source buildenv/bin/activate
        or on Windows:
            buildenv\Scripts\activate.bat
        
        The command prompt should now start with (buildenv) on each new prompt line. This shows that the new environment
        is activated and we are using it.
    
    
    Installing Building Tools
    -------------------------
        A series of packages are needed to create an installable python package.
        
        Enter the following into a python virtual environment:
            pip install setuptools wheel twine
        
        pip: A popular python package manager fpr installing new packages.
        setuptools: A package development tool for building and distributing packages.
        wheel: A format for distributing python modules in a ready to install approach.
        twine: A tool for publishing python modules to the Python Package Index (PyPI) registry.
        
        
    Building the Package
    --------------------
        Copy the package folder into the newly created Ailie_build directory.
        To build the package type the following:
            python setup.py sdist bdist_wheel
            
        Two new directories in the ailie_build folder should be created, build and dist.
        The dist folder contains the Python .whl that is our built module ready for isntall.
        
        
    Install the Created Package
    ---------------------------
        To install the package using pip, type the following command:
            pip install dist/<package_name>
        * Where <package_name> is the name of the package created for your systems setup.
        * The forward slash may have to be swapped to a backslash depending on OS
        
        On my laptop, this appears as: ailie_net-0.1-py3-none-any.whl
        
    
    Quick Test
    ----------
    
        If not already installed, numpy needs ot be installed in your environment
            pip install numpy
        
        In the command prompt activate a python terminal:
            python
        
        A new python terminal should now be created.
        You should now be able to import the Ailie_Net module using the following command:
            import Ailie_Net as ai
            
        If no error message is displayed, then the install is successful.
        
        The package also has a number of test scripts available. To run these the following dependencies
        may be required:
            pip install numpy
            pip install pandas
            pip install matplotlib
            pip install json
"""

# Read readme file to gather description information
with open("README.md") as readme_file:
    description = readme_file.read()

setup(
    name='ailie_net',
    version='0.1',
    author='Ryan Brown',
    license='MIT',
    readme = 'README.md',
    long_description=description,
    long_description_content_type='text/markdown',
    url='https://github.com/RyanB-Micro/Ailie_Net',
    packages=find_packages(),
)