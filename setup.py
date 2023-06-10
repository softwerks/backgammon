# Copyright 2019 Softwerks LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

with open("README.rst", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="backgammon",
    version="1.1.0",
    author="Softwerks",
    author_email="info@softwerks.com",
    description="Backgammon engine for the Backgammon Network.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/softwerks/backgammon",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
