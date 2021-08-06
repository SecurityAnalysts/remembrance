from distutils.core import setup

setup(
        name='remembrance',
        version='0.0.1',
        packages=['remembrance', 'remembrance.native', 'remembrance.injection'],
        url='https://github.com/Zeta314/remembrance',
        license='MIT',
        author='Zeta314',
        author_email='ale3152001@gmail.com',
        description='A little python framework to interact with Windows processes, their memory, their threads and '
                    'much more! '
)
