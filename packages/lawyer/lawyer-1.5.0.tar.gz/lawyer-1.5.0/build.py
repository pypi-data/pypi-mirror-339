from setuptools import setup, find_packages
from wheel.bdist_wheel import bdist_wheel

class BdistWheelCustom(bdist_wheel):
    def finalize_options(self):
        bdist_wheel.finalize_options(self)
        self.root_is_pure = False

setup(
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"lawyer": ["*.so", "*.pyd", "*.dylib"]},
    include_package_data=True,
    # Forces platform-specific wheel
    options={
        "bdist_wheel": {
            "universal": False,
            "py_limited_api": False,
        }
    },
    cmdclass={
        'bdist_wheel': BdistWheelCustom,
    },
)