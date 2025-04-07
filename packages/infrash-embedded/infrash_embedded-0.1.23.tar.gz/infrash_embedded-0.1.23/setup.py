from setuptools import setup, find_packages

setup(
    name="infrash_embedded",
    version="0.1.23",
    description="Print from html to pdf, zpl, image, printer: html to print, htmlinfrash_embedded, html to pdf,html2pdf, pdf to print, pdfinfrash_embedded, zpl to print,zplinfrash_embedded, image to print,  imageinfrash_embedded, ",
    author="Tom Softreck",
    author_email="info@softreck.dev",
    url="https://github.com/infrash_embedded/infrash_embedded",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
