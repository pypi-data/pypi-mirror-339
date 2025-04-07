from setuptools import setup, find_packages, __version__

setup(
    name='fastdevcommon',
    version='0.0.1',
    packages=find_packages(),
    description='A common development component',
    long_description=open('README.md').read(),
    # python3，readme文件中文报错
    # long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hwzlikewyh/FastDevCommon.git',
    author='hwzlikewyh',
    author_email='hwzlikewyh@163.com',
    license='MIT',
    install_requires=[
        # 依赖列表
    ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    package_data={'': ['*.csv', '*.txt', '.toml']},  # 这个很重要
    include_package_data=True  # 也选上
)
