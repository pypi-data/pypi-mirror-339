from setuptools import setup, find_packages

setup(
    name='profidata',
    version='0.1',
    author='ark4dev',
    packages=find_packages(),
    install_requires=[
        'numpy',
        # 'scikit-learn',
        # 'matplotlib',
        # 'seaborn',
        # 'plotly',
        # 'statsmodels',
        'scipy',
        'polars',
    ],
)