from setuptools import setup

setup(
    name='Hermodur',
    version='0.0.3',
    url="http://github.com/vis-netlausnir/hermodur/",
    license="BSD",
    author="Bjarki Gudlaugsson",
    author_email="bjarkig@vis.is",
    description="A simple AMQP socket.io connection for Tornado",
    packages=['hermodur'],
    zip_safe=False,
    platforms='any',
    dependency_links = [
        'https://github.com/vis-netlausnir/stormed-amqp/tarball/master#egg=stormed-amqp-0.1.1',
        'https://github.com/vis-netlausnir/tornadio2/tarball/master#egg=TornadIO2-0.0.1'
    ],
    install_requires=[
        'distribute>=0.6.19',
		'simplejson',
        'tornadio2==0.0.1',
        'stormed_amqp==0.1.1',
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
