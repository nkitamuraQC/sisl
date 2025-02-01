from setuptools import setup, find_packages

setup(
    name='sisl',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[],  # 依存関係があればリストに追加
    author='Your Name',
    author_email='your.email@example.com',
    description='A description of the sisl package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/sisl',  # 適切なURLに変更
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
