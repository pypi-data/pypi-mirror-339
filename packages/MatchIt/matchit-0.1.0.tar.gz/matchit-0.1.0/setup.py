from setuptools import setup, find_packages

setup(name="matchit",
      version="0.1.0",
      description="A package for Padel match making and padel player rankings",
      author="Andreas Løvgaard",
      packages=find_packages(),
      install_requires=[
          "pandas",
          "pydantic",
          "jupyter"
      ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.13",
        ],
        python_requires='>=3.8',
    )