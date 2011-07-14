from setuptools import setup

setup(
    name='Hermodur',
    version='0.0.2',
    url="http://github.com/vis-netlausnir/hermodur/",
    license="BSD",
    author="Bjarki Gudlaugsson",
    author_email="bjarkig@vis.is",
    description="A simple AMQP socket.io connection for Tornado",
    packages=['hermodur'],
    zip_safe=False,
    platforms='any',
    dependency_links = [
        'http://github.com/paolo-losi/stormed-amqp/tarball/master#StormedAMQP-dev',
        'http://github.com/mrjoes/tornadio/tarball/master#egg=TornadIO-dev'
    ],
    install_requires=[
        'distribute>=0.6.19',
        'tornadio==dev',
        'stormed-amqp==dev',
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
