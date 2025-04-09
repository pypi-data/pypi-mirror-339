"""
Tests for the llama_scheduler package.

This module contains comprehensive tests for the llama_scheduler package,
including unit tests for individual components and integration tests for
the entire system.
"""

import unittest

from llama_scheduler import (
    NodeProfile,
    ResourceRequirement,
    ResourceType,
)


class TestResourceRequirement(unittest.TestCase):
    """Tests for the ResourceRequirement class."""

    def test_resource_requirement_creation(self):
        """Test creating a resource requirement."""
        req = ResourceRequirement(ResourceType.CPU, 2.0)
        self.assertEqual(req.resource_type, ResourceType.CPU)
        self.assertEqual(req.amount, 2.0)

    def test_resource_requirement_str(self):
        """Test string representation of a resource requirement."""
        req = ResourceRequirement(ResourceType.MEMORY, 1024.0)
        self.assertEqual(str(req), "MEMORY: 1024.0")


class TestNodeProfile(unittest.TestCase):
    """Tests for the NodeProfile class."""

    def setUp(self):
        """Set up test fixtures."""
        self.node = NodeProfile(
            node_id="test-node",
            available_resources={
                ResourceType.CPU: 8.0,
                ResourceType.MEMORY: 16384.0,
                ResourceType.STORAGE: 1024 * 1024 * 1024 * 100,
            },
            energy_consumption_idle=50.0,
            energy_consumption_max=200.0,
        )

    def test_node_creation(self):
        """Test creating a node profile."""
        self.assertEqual(self.node.node_id, "test-node")
        self.assertEqual(self.node.available_resources[ResourceType.CPU], 8.0)
        self.assertEqual(self.node.energy_consumption_idle, 50.0)
        self.assertEqual(self.node.energy_consumption_max, 200.0)
        self.assertEqual(self.node.current_load, 0.0)

    def test_estimated_energy_consumption(self):
        """Test estimating energy consumption based on load."""
        # At 0% load, should be idle consumption
        self.assertAlmostEqual(self.node.get_estimated_energy_consumption(0.0), 50.0)

        # At 50% load, should be halfway between idle and max
        self.node.current_load = 0.0
        self.assertAlmostEqual(self.node.get_estimated_energy_consumption(0.5), 125.0)

        # At 100% load, should be max consumption
        self.node.current_load = 0.0
        self.assertAlmostEqual(self.node.get_estimated_energy_consumption(1.0), 200.0)
