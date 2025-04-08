from setuptools import setup, find_packages

setup(
    name='booking-site-generator',
    version='0.1.0',
    description='Генератор сайта для системы бронирования',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='katarymba',
    author_email='email@example.com',
    url='https://github.com/Y3ppi3/booking-site-generator',
    packages=find_packages(),
    package_data={
        'shablonizator': [
            'site_templates/booking/*.html',
            'site_templates/booking/js/*.js',
            'site_templates/booking/css/*.css',
            'site_templates/booking/images/*'
        ]
    },
    install_requires=[
        'setuptools>=45.0.0',
        'wheel>=0.34.2',
    ],
    entry_points={
        'console_scripts': [
            'booking-site-gen=shablonizator.generator:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='site generator booking website template',
    python_requires='>=3.7',
    include_package_data=True,
    zip_safe=False,
)