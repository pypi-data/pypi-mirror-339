from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="winids",
    version="0.1.0",
    author="DeepIDS Team",
    author_email="author@example.com",
    description="Windows-based Intrusion Detection System using machine learning and reinforcement learning for adaptive security",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/winids",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Security",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.6",
    install_requires=[
        "tensorflow>=2.0.0",
        "numpy>=1.18.0",
        "pandas>=1.0.0",
        "matplotlib>=3.1.0",
        "scikit-learn>=0.22.0",
        "pillow>=7.0.0",
    ],
    entry_points={
        "console_scripts": [
            "winids-dashboard=winids.pro_dashboard:main",
            "winids-bridge=winids.bridge:main",
            "winids-monitor=winids.monitor:main",
            "winids-attack-panel=winids.attack_panel:main",
        ],
    },
) 