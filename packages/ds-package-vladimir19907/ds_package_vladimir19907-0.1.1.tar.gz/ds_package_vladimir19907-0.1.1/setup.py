from setuptools import setup, find_packages

setup(
    name="ds_package_vladimir19907",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'pandas>=1.3.0',
        'scikit-learn>=1.0.0',
        'xgboost>=1.5.0',
        'tqdm>=4.62.0'
    ],
    include_package_data=True,
    author="vp",
    author_email="skip@mail.box",
    description="DS pack",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/corpsemanor/ds_deploy",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
)