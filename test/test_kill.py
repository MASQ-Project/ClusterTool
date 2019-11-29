# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
from ec2 import EC2
from compute import Compute
from virtualbox import VirtualBoxManage
from docker import Docker
import tnt_config
import kill as subject


class TestKill:

    @pytest.fixture
    def neighbor(self, mocker):
        self.mock_instance = mocker.Mock()
        self.mock_instance.index_name = mocker.Mock(return_value='node-0')
        instance_dict = {'node-0': self.mock_instance}
        mocker.patch.object(tnt_config, 'INSTANCES', instance_dict)

    @pytest.fixture
    def ec2_instance(self, mocker, neighbor):
        self.mock_ec2_instance = mocker.Mock(spec=EC2)
        self.mock_instance.instance_api = self.mock_ec2_instance

    @pytest.fixture
    def compute_instance(self, mocker, neighbor):
        self.mock_compute_instance = mocker.Mock(spec=Compute)
        self.mock_instance.instance_api = self.mock_compute_instance

    @pytest.fixture
    def vbox_instance(self, mocker, neighbor):
        self.mock_vbox_instance = mocker.Mock(spec=VirtualBoxManage)
        self.mock_instance.instance_api = self.mock_vbox_instance

    @pytest.fixture
    def docker_instance(self, mocker, neighbor):
        self.mock_docker_instance = mocker.Mock(spec=Docker)
        self.mock_instance.instance_api = self.mock_docker_instance

    def test_name(self):
        assert subject.name() == 'kill'

    def test_command_properties(self):
        real_command = subject.command()

        assert real_command.name == 'kill'
        assert real_command.info == 'shuts down'

    def test_command_for_ec2(self, ec2_instance):
        real_select_command = subject.command()

        real_select_command.run_for('node-0')

        self.mock_instance.kill.assert_called_with()
        assert self.mock_ec2_instance in tnt_config.EC2_INSTANCES

    def test_command_for_compute(self, compute_instance):
        real_select_command = subject.command()

        real_select_command.run_for('node-0')

        self.mock_instance.kill.assert_called_with()
        assert self.mock_compute_instance in tnt_config.COMPUTE_INSTANCES

    def test_command_for_virtualbox(self, vbox_instance):
        real_select_command = subject.command()

        real_select_command.run_for('node-0')

        self.mock_instance.kill.assert_called_with()
        assert self.mock_vbox_instance in tnt_config.VIRTUALBOX_INSTANCES

    def test_command_for_docker(self, docker_instance):
        real_select_command = subject.command()

        real_select_command.run_for('node-0')

        self.mock_instance.kill.assert_called_with()
        assert self.mock_docker_instance in tnt_config.DOCKER_INSTANCES
