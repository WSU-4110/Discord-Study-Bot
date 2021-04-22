"""
Discord bot.
"""

import setuptools as st

st.setup(
    name='StudyBot',
    version='0.0.2',
    packages=st.find_packages(),
    include_package_data=True,
    install_requires=[
        'discord.py',
        'mysql-connector-python',
        'pytz',
        'python-dotenv',
        'duckpy',
        'pytest',
        'selenium',
    ]
)
