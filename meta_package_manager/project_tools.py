# -*- coding: utf-8 -*-
#
# Copyright Kevin Deldycke <kevin@deldycke.com> and contributors.
# All Rights Reserved.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

""" Collection of utilities to manage mpm project itself.
"""

from pathlib import Path

from boltons.iterutils import flatten
from simplejson import dumps as json_dumps

from .managers import pool
from .platform import ALL_OS_LABELS


def generate_labels():
    """ Generate GitHub labels to use in issues and PR management.
    """
    label_defs = Path('../.github/labels.json').resolve()

    # Format: label name, color, optional description.
    LABELS = [
        ('BitBar plugin',   '#fef2c0', None),
        ('bug',             '#ee0701', None),
        ('documentation',   '#d4c5f9', None),
        ('duplicate',       '#cccccc', None),
        ('enhancement',     '#84b6eb', None),
        ('help wanted',     '#128A0C', None),
        ('invalid',         '#e6e6e6', None),
        ('question',        '#cc317c', None),
        ('wontfix',         '#ffffff', None),
    ]

    # Define some colors.
    PLATFORM_COLOR = '#bfd4f2'
    MANAGER_COLOR = '#bfdadc'

    # Some managers sharing some roots will be grouped together.
    MANAGER_GROUPS = {
        'dpkg-like': {'dpkg', 'apt', 'opkg'},
        'npm-like': {'npm', 'yarn'},
    }

    # Create one label per platform.
    for platform_id in ALL_OS_LABELS:
        LABELS.append((
            'platform: {}'.format(platform_id), PLATFORM_COLOR, None))

    # Create one label per manager.
    grouped_managers = set(flatten(MANAGER_GROUPS.values()))
    for manager_id in pool():
        if manager_id not in grouped_managers:
            LABELS.append((
                'manager: {}'.format(manager_id), MANAGER_COLOR, None))

    # Add labels for grouped managers.
    for group_label, manager_ids in MANAGER_GROUPS.items():
        LABELS.append((
            'manager: {}'.format(group_label), MANAGER_COLOR,
            ', '.join(sorted(manager_ids))))

    # Save to json definition file.
    label_defs = [
        dict(zip(['name', 'color', 'description'], label))
        for label in sorted(LABELS)]
    Path(__file__).parent.joinpath('../.github/labels.json').resolve().open(
        'w').write(json_dumps(
            label_defs,
            indent=4,
            separators=(',', ': '),
        ))
