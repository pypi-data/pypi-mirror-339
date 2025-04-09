from setuptools import setup, find_packages
import io
import os

version = os.environ.get('RELEASE_VERSION', '0.3.2'
'').lstrip('v')

setup(
    name="chatgpt-mirai-qq-bot-web-search",
    version=version,
    packages=find_packages(),
    include_package_data=True,  # 这行很重要
    package_data={
        "web_search": ["example/*.yaml", "example/*.yml"],
    },
    install_requires=[
        "playwright","trafilatura","lxml_html_clean",
        "kirara-ai>=3.2.0",
    ],
    entry_points={
        'chatgpt_mirai.plugins': [
            'web_search = web_search:WebSearchPlugin'
        ]
    },
    author="chuanSir",
    author_email="416448943@qq.com",

    description="WebSearch adapter for lss233/chatgpt-mirai-qq-bot",
    long_description=io.open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chuanSir123/web_search",
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU Affero General Public License v3',
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/chuanSir123/web_search/issues",
        "Documentation": "https://github.com/chuanSir123/web_search/wiki",
        "Source Code": "https://github.com/chuanSir123/web_search",
    },
    python_requires=">=3.8",
)
