import os
from setuptools import setup

BASEDIR = os.path.abspath(os.path.dirname(__file__))
TX_ENTRY_POINT = 'deepl_translate_plug = ovos_translate_plugin_deepl:DeepLTranslator'
DETECT_ENTRY_POINT = 'deepl_detection_plug = ovos_translate_plugin_deepl:DeepLDetector'

def get_version():
    """ Find the version of the package"""
    version = None
    version_file = os.path.join(BASEDIR, 'ovos_translate_plugin_deepl', 'version.py')
    major, minor, build, alpha = (None, None, None, None)
    with open(version_file) as f:
        for line in f:
            if 'VERSION_MAJOR' in line:
                major = line.split('=')[1].strip()
            elif 'VERSION_MINOR' in line:
                minor = line.split('=')[1].strip()
            elif 'VERSION_BUILD' in line:
                build = line.split('=')[1].strip()
            elif 'VERSION_ALPHA' in line:
                alpha = line.split('=')[1].strip()

            if ((major and minor and build and alpha) or
                    '# END_VERSION_BLOCK' in line):
                break
    version = f"{major}.{minor}.{build}"
    if alpha and int(alpha) > 0:
        version += f"a{alpha}"
    return version


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


setup(
    name='ovos_translate_plugin_deepl',
    version=get_version(),
    description='OVOS translation/detection module wrapping deepl-python',
    url='https://github.com/emphasize/ovos-translate-plugin-deepl',
    author='emphasize',
    author_email='',
    license='Apache-2.0',
    packages=['ovos_translate_plugin_deepl'],
    install_requires=required("requirements/requirements.txt"),
    extras_require={
        "test": required("requirements/test_requirements.txt")
    },
    package_data={'': package_files('ovos_translate_plugin_deepl')},
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    entry_points={
        'neon.plugin.lang.translate': TX_ENTRY_POINT,
        'neon.plugin.lang.detect': DETECT_ENTRY_POINT
    }
)