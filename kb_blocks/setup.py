from setuptools import setup, find_packages

setup(name="kb_blocks",
      version="0.1",
      url="https://git.kbuilds.com/blocks/kb_blocks",
      author="kbuilds, LLC",
      author_email="k@kbuilds.com",
      description="View library for Python web frameworks",
      install_requires=[
        "markdown",
        ],
      packages=find_packages(),
      include_package_data=True,
      )
