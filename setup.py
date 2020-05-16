import setuptools

with open("README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="star_base",
    version="0.0.1",

    description="Stores weather station data",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "star_base"},
    packages=setuptools.find_packages(where="star_base"),

    install_requires=[
        "aws-cdk.core==1.38.0",
        "aws-cdk.aws_iam==1.38.0",
        "aws-cdk.aws_s3==1.38.0",
        "aws-cdk.aws-lambda==1.38.0",
        "aws-cdk.aws_apigateway==1.38.0",
        "aws-cdk.aws_dynamodb==1.38.0",
        "aws-cdk.aws-cloudfront==1.38.0",
        "boto3==1.13.11",
    ],

    python_requires=">=3.8",

    classifiers=[
        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",

        "Typing :: Typed",
    ],
)
