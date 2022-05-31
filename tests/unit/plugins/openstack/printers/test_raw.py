"""
#    Copyright 2022 Red Hat
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
from unittest import TestCase

from cibyl.plugins.openstack import Deployment
from cibyl.plugins.openstack.container import Container
from cibyl.plugins.openstack.node import Node
from cibyl.plugins.openstack.package import Package
from cibyl.plugins.openstack.printers.raw import OSRawPrinter
from cibyl.plugins.openstack.service import Service


class TestOSRawPrinter(TestCase):
    """Tests for :class:`OSRawParser`.
    """

    def test_print_deployment(self):
        """Test that the string representation of Deployment works.
        """
        release = '17.0'
        infra = 'ovb'
        services = {'nova': Service('nova', {})}
        nodes = {'controller-0': Node('controller-0', 'controller')}
        ip_version = "4"
        topology = "controllers:1"
        network = "vxlan"
        storage = "ceph"
        dvr = "true"
        tls_everywhere = "false"
        templates = set(["a", "b"])
        ml2_driver = "ovn"
        ironic = "True"
        cleaning_net = "False"
        security_group = "N/A"

        deployment = Deployment(release, infra,
                                nodes, services,
                                ip_version=ip_version,
                                topology=topology,
                                network_backend=network,
                                storage_backend=storage,
                                dvr=dvr,
                                tls_everywhere=tls_everywhere,
                                overcloud_templates=templates,
                                ml2_driver=ml2_driver,
                                ironic_inspector=ironic,
                                cleaning_network=cleaning_net,
                                security_group=security_group)

        printer = OSRawPrinter(verbosity=1)

        result = printer.print_deployment(deployment)

        self.assertIn("Openstack deployment:", result)
        self.assertIn("Release:", result)
        self.assertIn(release, result)
        self.assertIn("Infra type:", result)
        self.assertIn(infra, result)
        self.assertIn("IP version:", result)
        self.assertIn(ip_version, result)
        self.assertIn("Topology:", result)
        self.assertIn(topology, result)
        self.assertIn("Network:", result)
        self.assertIn("Network backend:", result)
        self.assertIn(network, result)
        self.assertIn("Storage:", result)
        self.assertIn("Storage backend:", result)
        self.assertIn(storage, result)
        self.assertIn("DVR:", result)
        self.assertIn(dvr, result)
        self.assertIn("TLS everywhere:", result)
        self.assertIn(tls_everywhere, result)
        self.assertIn("Overcloud templates:", result)
        for template in templates:
            self.assertIn(f"- {template}", result)
        self.assertIn("ML2 driver:", result)
        self.assertIn(ml2_driver, result)
        self.assertIn("Security group mechanism:", result)
        self.assertIn(security_group, result)

        self.assertIn("Ironic:", result)
        self.assertIn("Ironic inspector:", result)
        self.assertIn(ironic, result)
        self.assertIn("Cleaning network:", result)
        self.assertIn(cleaning_net, result)

        self.assertIn("Service name:", result)
        self.assertIn('nova', result)
        self.assertIn("Nodes:", result)
        self.assertIn('controller-0', result)

    def test_print_overcloud_templates_not_available(self):
        """Test that overcloud_templates are printed correctly
        when set to N/A."""
        release = '17.0'
        infra = 'ovb'
        deployment = Deployment(release, infra, {}, {},
                                overcloud_templates="N/A")
        printer = OSRawPrinter(verbosity=1)

        result = printer.print_deployment(deployment)
        self.assertIn("Overcloud templates: N/A", result)

    def test_print_empty_deployment(self):
        """Test that the string representation of an empty deployment shows the
        apropiate message.
        """
        deployment = Deployment("", "", {}, {})
        printer = OSRawPrinter(verbosity=1)
        result = printer.print_deployment(deployment)
        expected = "  No openstack information associated with this job"
        self.assertEqual(result, expected)

    def test_print_deployment_missing_information(self):
        """Test that the string representation of Deployment skips the missing
        information.
        """
        release = '17.0'
        infra = 'ovb'
        nodes = {'controller-0': Node('controller-0', 'controller')}
        ip_version = "4"
        topology = "controllers:1"
        network = "vxlan"
        storage = "ceph"
        dvr = "true"
        tls_everywhere = "false"
        templates = set(["a", "b"])
        ml2_driver = "ovn"
        ironic = "N/A"
        cleaning_net = "N/A"
        security_group = "N/A"

        deployment = Deployment(release, infra,
                                nodes, {},
                                ip_version=ip_version,
                                topology=topology,
                                network_backend=network,
                                storage_backend=storage,
                                dvr=dvr,
                                tls_everywhere=tls_everywhere,
                                overcloud_templates=templates,
                                ml2_driver=ml2_driver,
                                ironic_inspector=ironic,
                                cleaning_network=cleaning_net,
                                security_group=security_group)

        printer = OSRawPrinter(verbosity=0)

        result = printer.print_deployment(deployment)

        self.assertIn("Openstack deployment:", result)
        self.assertIn("Release:", result)
        self.assertIn(release, result)
        self.assertIn("Infra type:", result)
        self.assertIn(infra, result)
        self.assertIn("IP version:", result)
        self.assertIn(ip_version, result)
        self.assertIn("Topology:", result)
        self.assertIn(topology, result)
        self.assertIn("Network:", result)
        self.assertIn("Network backend:", result)
        self.assertIn(network, result)
        self.assertIn("Storage:", result)
        self.assertIn("Storage backend:", result)
        self.assertIn(storage, result)
        self.assertIn("DVR:", result)
        self.assertIn(dvr, result)
        self.assertIn("TLS everywhere:", result)
        self.assertIn(tls_everywhere, result)
        self.assertIn("Overcloud templates:", result)
        for template in templates:
            self.assertIn(f"- {template}", result)
        self.assertIn("ML2 driver:", result)
        self.assertIn(ml2_driver, result)
        self.assertNotIn("Security group mechanism:", result)

        self.assertNotIn("Ironic:", result)
        self.assertNotIn("Ironic inspector:", result)
        self.assertNotIn("Cleaning network:", result)

    def test_print_node(self):
        """Test that the string representation of Node works.
        """
        name = 'controller-0'
        role = 'controller'
        packages = {"rpm-package": Package("rpm-package", "rhos-release")}
        containers = {"container": Container("container", "image")}
        node = Node(name, role, containers=containers, packages=packages)

        printer = OSRawPrinter(verbosity=1)

        result = printer.print_node(node)

        self.assertIn(f"- {name}", result)
        self.assertIn(f"  Role: {role}", result)
        self.assertIn("  Container: container", result)
        self.assertIn("    Image: image", result)
        self.assertIn("  Package: rpm-package", result)
        self.assertIn("    Origin: rhos-release", result)

    def test_print_service(self):
        """Test that the string representation of Service works.
        """
        name = 'test-service'
        config = {'option1': 'true'}
        service = Service(name, config)

        printer = OSRawPrinter(verbosity=1)

        result = printer.print_service(service)

        self.assertIn("Service name:", result)
        self.assertIn(name, result)
        self.assertIn("option1:", result)
        self.assertIn("true", result)

    def test_print_package(self):
        """Test that the string representation of Package works."""
        name = "rpm-package"
        origin = "rhos-release"
        package = Package(name, origin)
        printer = OSRawPrinter(verbosity=1)

        result = printer.print_package(package)
        self.assertIn("Package: ", result)
        self.assertIn(name, result)
        self.assertIn("  Origin: ", result)
        self.assertIn(origin, result)

    def test_print_container(self):
        """Test that the string representation of Package works."""
        name = "container"
        image = "image"
        packages = {"rpm-package": Package("rpm-package", "rhos-release")}
        container = Container(name, image, packages)

        printer = OSRawPrinter(verbosity=1)

        result = printer.print_container(container)

        self.assertIn(f"Container: {name}", result)
        self.assertIn(f"  Image: {image}", result)
        self.assertIn("  Package: rpm-package", result)
        self.assertIn("    Origin: rhos-release", result)
