from setuptools import setup, find_packages

setup(
    name="chatbot_session_flow",  # Unique package name
    version="0.1.7",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=4.1.2"
    ],
    author="Dennis Kamau",
    author_email="kamadennis05@gmail.com",
    description="A django Whatsapp chatbot session manager",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DK-denno/whatsapp-chatbot.git",  # Your repository
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)