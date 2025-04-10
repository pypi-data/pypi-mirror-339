# Copyright 2023 Open Source Robotics Foundation, Inc.
# Licensed under the Apache License, Version 2.0

from asyncio import Queue
from asyncio import QueueEmpty
import os
from pathlib import Path
import platform
from random import shuffle

from colcon_core.event.job import JobEnded
from colcon_core.event.job import JobSkipped
from colcon_core.event_handler import EventHandlerExtensionPoint
from colcon_core.logging import colcon_logger
from colcon_core.plugin_system import satisfies_version
from colcon_core.plugin_system import SkipExtensionException
from colcon_core.shell import ShellExtensionPoint

logger = colcon_logger.getChild(__name__)


class ROSDomainIDShell(EventHandlerExtensionPoint, ShellExtensionPoint):
    """Set a different ROS_DOMAIN_ID environment variable for each task."""

    # The (shell) priority should be higher than any usable shells
    PRIORITY = 900

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(
            EventHandlerExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')
        satisfies_version(ShellExtensionPoint.EXTENSION_POINT_VERSION, '^2.2')

        self._default_id = os.environ.get('ROS_DOMAIN_ID', None)

        self.allocated_ids = {}
        self.free_ids = Queue()

        all_ids = []
        system = platform.system()

        # TODO(cottsay): Determine usable IDs based on the system's
        #                network configuration
        if system in ('Darwin', 'Windows'):
            all_ids.extend(range(0, 167))
        else:
            all_ids.extend(range(0, 102))
            all_ids.extend(range(215, 233))

        shuffle(all_ids)
        for i in all_ids:
            i_str = str(i)

            # If the user has a specific ID set already, avoid using that
            if i_str != (self._default_id or '0'):
                self.free_ids.put_nowait(i_str)

        logger.debug(f'Have {self.free_ids.qsize()} domain IDs for assignment')

    def get_file_extensions(self):  # noqa: D102
        return ()

    def create_prefix_script(self, prefix_path, merge_install):  # noqa: D102
        return []

    def create_package_script(  # noqa: D102
        self, prefix_path, pkg_name, hooks
    ):
        return []

    def create_hook_set_value(  # noqa: D102
        self, env_hook_name, prefix_path, pkg_name, name, value,
    ):
        return Path('ros_domain_id.txt')

    def create_hook_append_value(  # noqa: D102
        self, env_hook_name, prefix_path, pkg_name, name, subdirectory,
    ):
        return Path('ros_domain_id.txt')

    def create_hook_prepend_value(  # noqa: D102
        self, env_hook_name, prefix_path, pkg_name, name, subdirectory,
    ):
        return Path('ros_domain_id.txt')

    async def generate_command_environment(  # noqa: D102
        self, task_name, build_base, dependencies,
    ):
        # Allocate unique IDs based on the build_base
        build_base = os.path.abspath(os.path.join(
            os.getcwd(), str(build_base)))

        if build_base in self.allocated_ids:
            domain_id = self.allocated_ids[build_base]
        else:
            try:
                domain_id = self.free_ids.get_nowait()
            except QueueEmpty:
                domain_id = None

        if domain_id is None:
            logger.warn(f"No free ROS_DOMAIN_ID to assign for '{build_base}'")
            if self._default_id is None:
                os.environ.pop('ROS_DOMAIN_ID', None)
            else:
                os.environ['ROS_DOMAIN_ID'] = self._default_id
        else:
            # Used for the domain_coordinator by ament_cmake_ros
            os.environ['DISABLE_ROS_ISOLATION'] = '1'
            # Used by rmw_test_fixture_implementation
            os.environ['RMW_TEST_FIXTURE_DISABLE_ISOLATION'] = '1'
            # Attempt to keep tests off the host's network
            os.environ['ROS_AUTOMATIC_DISCOVERY_RANGE'] = 'LOCALHOST'
            os.environ['ROS_DOMAIN_ID'] = domain_id
            logger.debug(
                f"Allocated ROS_DOMAIN_ID={domain_id} for '{build_base}'")

        # If we failed to allocate an ID for this build_base, specifically
        # store 'None' so that future allocation attempts for this build_base
        # are consistent and don't assign an ID that has since been unassigned.
        self.allocated_ids[build_base] = domain_id

        # This extension can't actually perform command environment generation
        raise SkipExtensionException()

    def __call__(self, event):  # noqa: D102
        data = event[0]

        if isinstance(data, (JobEnded, JobSkipped)):
            job = event[1]

            build_base = getattr(job.task_context.args, 'build_base', None)
            if build_base is None:
                return

            build_base = os.path.abspath(os.path.join(
                os.getcwd(), build_base))

            domain_id = self.allocated_ids.pop(build_base, None)
            if domain_id is None:
                return

            self.free_ids.put_nowait(domain_id)
            logger.debug(
                f"Released ROS_DOMAIN_ID={domain_id} for '{build_base}'")
