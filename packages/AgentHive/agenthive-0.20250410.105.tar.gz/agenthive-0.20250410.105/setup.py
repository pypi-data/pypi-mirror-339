from setuptools import setup, find_packages
import os

# Read README file for long description
long_description = ''
if os.path.isfile("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

# Read version from file
with open("src/agenthive/version.py", "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"\'')
            break
    else:
        version = "0.1.0"

# Function to read requirements from a file
def read_requirements(filename):
    requirements = []
    if os.path.isfile(filename):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("-r"):
                    if line.startswith("-e "):
                        requirements.append(line.split('#egg=')[1])
                    else:
                        requirements.append(line)
    return requirements

# Read requirements from files
base_requirements = read_requirements("requirements/base_requirements.txt")
coordinator_requirements = [req for req in read_requirements("requirements/coordinator_requirements.txt") 
                           if req not in base_requirements]
worker_requirements = [req for req in read_requirements("requirements/worker_requirements.txt") 
                      if req not in base_requirements]
monitor_requirements = [req for req in read_requirements("requirements/monitor_requirements.txt") 
                       if req not in base_requirements]
test_requirements = [req for req in read_requirements("requirements/test_requirements.txt") 
                    if req not in base_requirements]

cli_requirements = [req for req in read_requirements("requirements/cli_requirements.txt") 
                    if req not in base_requirements]

# Define extras_require
extras_require = {
    "dev": base_requirements + coordinator_requirements + worker_requirements + monitor_requirements + test_requirements + cli_requirements,
}

setup(
    name="AgentHive",
    version=version,
    author="changyy",
    author_email="changyy.csie@gmail.com",
    description="AgentHive is a flexible, Python-based service framework for managing distributed task execution.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/changyy/py-AgentHive",
    project_urls={
        "Bug Tracker": "https://github.com/changyy/py-AgentHive/issues",
        "Documentation": "https://py-agenthiveflow.readthedocs.io",
        "Source Code": "https://github.com/changyy/py-AgentHive",
    },
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.12",
    install_requires=base_requirements + coordinator_requirements + worker_requirements + monitor_requirements,
    extras_require=extras_require,
    entry_points={
        "console_scripts": [
            "agenthive=agenthive.cli:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "agenthive": ["templates/docker/*", "templates/docker/**/*", "service/monitor/backend/templates/*", "service/monitor/backend/templates/**/*"],
    },
)
