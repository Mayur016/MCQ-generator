from setuptools import setup, find_packages

setup(
    name="mcqgenerator",
    version='0.0.1',
    author="Mayur Patil",
    author_email="mayurpatil2572001@gmail.com",
    install_requires = ["openai", "langchain", "streamlit", "python-dotenv", "PyPDF2"],
    packages= find_packages()
)