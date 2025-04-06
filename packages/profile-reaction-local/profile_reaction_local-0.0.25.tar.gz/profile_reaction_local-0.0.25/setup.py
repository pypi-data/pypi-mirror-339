import setuptools

PACKAGE_NAME = "profile-reaction-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version="0.0.25",  # https://pypi.org/project/profile-reaction-local/
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles Profile Reaction Local Python",
    long_description="This is a package for sharing common methods of profile reaction CRUD to profile_reaction database used in different repositories",  # noqa: E501
    long_description_content_type="text/markdown",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f"{package_dir}/src"},
    package_data={package_dir: ["*.py"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "database-mysql-local>=0.0.199",
        "logger-local>=0.0.133",
    ],
)
