from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='DirNet',
    version='1.0',
    description='Lightweight library for neural network-based directional prediction',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=['DirNet'],
    author='foloip',
    install_requires=[
        "numpy"
    ],
    author_email='NeuralNetworkTools@gmail.com',
    keywords=['neural network', 'direction prediction', 'ai', 'machine learning', 'Perceptron', 'Backpropagation', 'relu'],
    url='https://github.com/Foloip'
)