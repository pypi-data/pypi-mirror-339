from setuptools import setup, find_packages

setup(
    name="nerd-dictation-gui",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "PyQt6>=6.0.0",
    ],
    package_data={
        "nerd_dictation_gui": ["resources/*.png"],
    },
    entry_points={
        "console_scripts": [
            "nerd-dictation-gui=nerd_dictation_gui.main:main",
        ],
    },
    author="Karl Haines",
    author_email="kmhnashville@gmail.com",
    description="GUI for nerd-dictation",
    keywords="dictation, speech-to-text, gui",
    python_requires=">=3.6",
)
