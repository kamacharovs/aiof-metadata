from setuptools import setup, find_packages


with open("README.md", encoding="utf-8") as f:
    readme = f.read()

with open("LICENSE", encoding="utf-8") as f:
    license = f.read()


if __name__ == "__main__":
    setup(
        name = "aiof-metadata",
        version = "0.1.0",
        description = "All in one finance data crunching backend",
        long_description = readme,
        author = "Georgi Kamacharov",
        author_email = "aiof@email.com",
        url = "https://github.com/gkama/aiof-metadata",
        license = license,
        packages = find_packages(exclude=("tests", "docs"))
    )