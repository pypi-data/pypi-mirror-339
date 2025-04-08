# Copyright 2023-2024 Geoffrey R. Scheller
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

"""
### Developer Tools - Queue based data structures

#### Modules

##### module dtools.queues.restrictive

- mutable data structures geared to specific algorithmic use cases
  - *class* dtools.queues.restrictive.FIFOQueue: First In First Out Queue
  - *class* dtools.queues.restrictive.LIFOQueue: Last In First Out Queue
  - *class* dtools.queues.restrictive.DoubleQueue: Double-ended Queue

---

##### *module* dtools.queues.splitends

- *class* dtools.splitends.se.SE: Mutable LIFO queues (stacks)
  - which allow for data sharing between different instances
  - each splitend sees itself as a singularly linked list
    - from the "end" of the hair to its "root"
  - multiple instances can form bush like data structures
    - like follicles of hair with split ends

"""

__version__ = '0.27.0'
__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2023-2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'
