from setuptools import setup, find_packages

setup(
    name='nullstools',  # Название пакета
    version='0.1',      # Версия пакета
    packages=find_packages(),  # Находит все пакеты в вашем проекте
    long_description=open('README.md').read(),  # Описание из README
    long_description_content_type='text/markdown',
    author='darkmean',
    description=open('README.md').read(),
    url='https://github.com/darkmean-dev/nullstools',  # Ссылка на репозиторий или сайт
    classifiers=[  # Категории для PyPI
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Укажите вашу лицензию
        'Operating System :: OS Independent',
    ],
)