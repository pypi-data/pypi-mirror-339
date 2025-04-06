from setuptools import setup, find_packages
import os
import sys

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define post-install command for Windows
if sys.platform.startswith('win'):
    try:
        from setuptools.command.install import install as _install
        from setuptools.command.develop import develop as _develop

        # Custom command for regular install
        class install(_install):
            def run(self):
                _install.run(self)
                # Run post-install script
                self.execute(self._post_install, [], msg="Running post install task")
            
            def _post_install(self):
                from speedclickpro_postinstall import main
                main()

        # Custom command for development install
        class develop(_develop):
            def run(self):
                _develop.run(self)
                # Run post-install script
                self.execute(self._post_install, [], msg="Running post install task")
            
            def _post_install(self):
                from speedclickpro_postinstall import main
                main()

        cmdclass = {
            'install': install,
            'develop': develop,
        }
    except ImportError:
        cmdclass = {}
else:
    cmdclass = {}

setup(
    name="speedclickpro",
    version="1.0.7",  # ปรับเวอร์ชั่นเพื่อการอัพเดท
    author="SpeedClick Pro Team",
    author_email="your.email@example.com",  # Change this to your email
    description="Advanced auto-clicker with animation sequencing capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/speedclickpro",  # Change to your repo if any
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/speedclickpro/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Utilities",
        "Intended Audience :: End Users/Desktop",
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "speedclickpro": ["icons/*", "profiles/*"],
    },
    py_modules=["speedclickpro_postinstall"],  # เพิ่ม post-install script
    cmdclass=cmdclass,  # เพิ่ม custom install commands
    python_requires=">=3.7",
    install_requires=[
        "pyautogui>=0.9.54",
        "keyboard>=0.13.5",
        "Pillow>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "speedclickpro=speedclickpro:run",
        ],
        "gui_scripts": [
            "speedclickpro-gui=speedclickpro:run",  # เพิ่ม GUI entry point
        ],
    },
    scripts=[
        "scripts/speedclickpro",       # Unix-style launcher
        "scripts/speedclickpro.bat",    # Windows launcher
    ],
    # Force setuptools to create PATH shortcuts
    zip_safe=False,
    options={
        'bdist_wheel': {'universal': True},
        'install': {'single_version_externally_managed': True},
    },
)
