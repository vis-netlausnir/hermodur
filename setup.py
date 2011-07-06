from setuptools import setup

setup(
    name='Hermodur',
    version='0.0.1',
    url="http://github.com/vis-netlausnir/hermodur/",
    license="BSD",
    author="Bjarki Gudlaugsson",
    author_email="bjarkig@vis.is",
    description="A simple AMQP WebSocket handler for Tornado",
    packages=['hermodur'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'distribute>=0.6.19',
        'stormed-amqp>=0.1',
        'tornado'
    ],
    classifiers=[
        'Development Status :: Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WEBSOCKET/AMQP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)