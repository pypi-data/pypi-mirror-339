from setuptools import setup, find_packages

setup(
    name="notify_senpai",
    version="0.1.2",
    packages=find_packages(),
    include_package_data=True,  # ✅ Ensure non-Python files are included
    package_data={
        "notify_senpai": ["notify.sh"],  # ✅ Explicitly include notify.sh
    },
    install_requires=[],
    entry_points={
        "console_scripts": [
            "notify=notify.notifier:notify_on_completion",
            "just_notify=notify.notifier:just_notify",
        ],
    },
)

