from setuptools import setup, find_packages

setup(
    name="gmail-generator",
    version="4.6.1",
    author="B_Q_5",
    description="Tele : @B_Q_5",
    packages=find_packages(),
    install_requires=[
        'pyTelegramBotAPI>=4.12.0',
        'psutil>=5.9.0',
        'rich>=12.0.0',
        'colorama>=0.4.6'
    ],
)