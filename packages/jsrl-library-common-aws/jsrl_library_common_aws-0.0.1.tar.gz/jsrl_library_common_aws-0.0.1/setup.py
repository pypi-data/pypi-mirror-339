LIBRARY_VERSION = "0.0.1"
INTERNAL_VERSION = "0"
LIBRARY_NAME = "jsrl-library-common-aws"

with open("README.md") as file:
    long_description = file.read()

with open("LICENSE.txt") as file:
    license = file.read()

if __name__ == "__main__":
    from setuptools import setup
    
    setup(
        name=LIBRARY_NAME,
        version=LIBRARY_VERSION,
        description="library with resuable components/functions by any backend project",
        long_description=long_description,
        classifiers=[
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Libraries",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.13",
            "Operating System :: OS Independent",
        ],
        keywords=[
            "jsrl-library-common",
            "jsrl-library-common-aws"
        ],
        author="Juan Sebastian Reyes Leyton",
        author_email="sebas.reyes2002@hotmail.com",
        url="",
        download_url="",
        license=license,
        platforms="Unix",
        packages=["jsrl_library_common",
                  "jsrl_library_common/",
                  "jsrl_library_common/constants",
                  "jsrl_library_common/constants/aws",
                  "jsrl_library_common/exceptions",
                  "jsrl_library_common/exceptions/aws",
                  "jsrl_library_common/utils",
                  "jsrl_library_common/utils/aws"],
        include_package_data=True,
        install_requires=[
            'boto3==1.35.80',
            'botocore==1.35.80',
            's3transfer==0.10.4'
        ]
    )