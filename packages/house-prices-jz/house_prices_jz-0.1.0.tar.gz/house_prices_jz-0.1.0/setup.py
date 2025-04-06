from setuptools import setup, find_packages

setup(
    name='house_prices_jz',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas==2.2.2',
        'numpy==1.26.4',
        'scikit-learn==1.4.2',
        'joblib==1.4.0',
    ],
    author='Jiso Chacko',
    author_email='jisochacko007@gmail.com',
    description='A package for house price prediction model',
    python_requires='>=3.8',
)