from setuptools import setup

setup(
    name='german_transliterate',
    version='0.1.3',
    author='Matteo Paltenghi',
    author_email='mattepalte@live.it',
    packages=['german_transliterate'],
    url='http://github.com/MattePalte/german_transliterate',
    license='CC-BY-4.0 License',
    description=(
        'german_transliterate can clean and transliterate (i.e. normalize) German text '
        'including abbreviations, numbers, timestamps etc. (fork of https://github.com/repodiac/german_transliterate)'
    ),
    long_description=(
        "german_transliterate is a Python module to clean and transliterate (i.e. normalize) German text.\n\n"
        "Features:\n"
        "- Clean messy text (e.g., map peculiar Unicode encodings to ASCII).\n"
        "- Replace common abbreviations in text.\n\n"
        "It can be used in combination with various text mining tasks."
    ),
    long_description_content_type='text/markdown',
    install_requires=[
        "num2words",
    ],
)
