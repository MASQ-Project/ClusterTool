# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
import init as subject

class TestInit:

    @pytest.fixture
    def printing(self, mocker):
        self.mock_print = mocker.patch('__builtin__.print', autospec=True)

    @pytest.fixture
    def available_instances(self, mocker):
        self.mock_first_compute_instance = mocker.Mock()
        self.mock_second_compute_instance = mocker.Mock()
        self.mock_first_compute_instance.index_name = mocker.Mock(return_value='g-node-1')
        self.mock_first_compute_instance.machine_name = mocker.Mock(return_value='Google-machine1')
        self.mock_second_compute_instance.index_name = mocker.Mock(return_value='g-node-2')
        self.mock_second_compute_instance.machine_name = mocker.Mock(return_value='Google-machine2')
        self.mock_first_compute_instance.__class__ = 'Compute'
        self.mock_second_compute_instance.__class__ = 'Compute'
        mocker.patch.object(subject, 'COMPUTE_INSTANCES', [
            self.mock_first_compute_instance,
            self.mock_second_compute_instance
        ])

        self.mock_first_ec2_instance = mocker.Mock()
        self.mock_second_ec2_instance = mocker.Mock()
        self.mock_first_ec2_instance.index_name = mocker.Mock(return_value='a-node-1')
        self.mock_first_ec2_instance.machine_name = mocker.Mock(return_value='Amazon-machine1')
        self.mock_second_ec2_instance.index_name = mocker.Mock(return_value='a-node-2')
        self.mock_second_ec2_instance.machine_name = mocker.Mock(return_value='Amazon-machine2')
        self.mock_first_ec2_instance.__class__ = 'EC2'
        self.mock_second_ec2_instance.__class__ = 'EC2'
        mocker.patch.object(subject, 'EC2_INSTANCES', [
            self.mock_first_ec2_instance,
            self.mock_second_ec2_instance
        ])

        self.mock_first_vbox_instance = mocker.Mock()
        self.mock_second_vbox_instance = mocker.Mock()
        self.mock_first_vbox_instance.index_name = mocker.Mock(return_value='v-node-1')
        self.mock_first_vbox_instance.machine_name = mocker.Mock(return_value='VBox-machine1')
        self.mock_second_vbox_instance.index_name = mocker.Mock(return_value='v-node-2')
        self.mock_second_vbox_instance.machine_name = mocker.Mock(return_value='VBox-machine2')
        self.mock_first_vbox_instance.__class__ = 'VirtualBox'
        self.mock_second_vbox_instance.__class__ = 'VirtualBox'
        mocker.patch.object(subject, 'VIRTUALBOX_INSTANCES', [
            self.mock_first_vbox_instance,
            self.mock_second_vbox_instance
        ])

        self.mock_first_docker_instance = mocker.Mock()
        self.mock_second_docker_instance = mocker.Mock()
        self.mock_first_docker_instance.index_name = mocker.Mock(return_value='d-node-1')
        self.mock_first_docker_instance.machine_name = mocker.Mock(return_value='Docker-machine1')
        self.mock_second_docker_instance.index_name = mocker.Mock(return_value='d-node-2')
        self.mock_second_docker_instance.machine_name = mocker.Mock(return_value='Docker-machine2')
        self.mock_first_docker_instance.__class__ = 'Docker'
        self.mock_second_docker_instance.__class__ = 'Docker'
        mocker.patch.object(subject, 'DOCKER_INSTANCES', [
            self.mock_first_docker_instance,
            self.mock_second_docker_instance
        ])

        yield

        subject.INSTANCES.clear()

    @pytest.fixture
    def instances(self, mocker, available_instances):
        self.mock_first_instance = mocker.Mock()
        self.mock_second_instance = mocker.Mock()
        self.mock_first_instance.index_name = mocker.Mock(return_value='node-0')
        self.mock_second_instance.index_name = mocker.Mock(return_value='node-1')
        self.mock_first_instance.__class__ = 'ExistingClass'
        self.mock_second_instance.__class__ = 'ExistingClass'
        mocker.patch.object(subject, 'INSTANCES', {
            'node-0': self.mock_first_instance,
            'node-1': self.mock_second_instance
        })

        yield

        subject.INSTANCES.clear()

    def test_name(self):
        assert subject.name() == 'init'

    def test_command(self, mocker, instances, printing):
        real_command = subject.command()

        assert real_command.name == 'init'
        assert real_command.info == 'Configures instances for use during this run of TNT'

        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.side_effect = ['cloud', 'all']

        real_command.run_for([])

        assert self.mock_print.mock_calls == [
            mocker.call('\nAvailable configured cloud instances:'),
            mocker.call("\tGoogle: ['Google-machine1', 'Google-machine2']"),
            mocker.call("\tAmazon: ['Amazon-machine1', 'Amazon-machine2']"),
            mocker.call('\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox-machine1', 'VBox-machine2']\n"),
            mocker.call("\tDocker: ['Docker-machine1', 'Docker-machine2']\n"),
            mocker.call("Configured node-2 on Google-machine1 (Compute)"),
            mocker.call("Configured node-3 on Google-machine2 (Compute)"),
            mocker.call("Configured node-4 on Amazon-machine1 (EC2)"),
            mocker.call("Configured node-5 on Amazon-machine2 (EC2)")
        ]

        assert mock_input.mock_calls == [
            mocker.call("Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) "),
            mocker.call().strip(),
            mocker.call("How many instances do you want to use? (1-4, or 'all', blank to cancel) "),
            mocker.call().strip()
        ]

        assert subject.INSTANCES['node-0'].index_name() == 'node-0'
        assert subject.INSTANCES['node-1'].index_name() == 'node-1'
        assert subject.INSTANCES['node-2'].instance_api.machine_name() == 'Google-machine1'
        assert subject.INSTANCES['node-3'].instance_api.machine_name() == 'Google-machine2'
        assert subject.INSTANCES['node-4'].instance_api.machine_name() == 'Amazon-machine1'
        assert subject.INSTANCES['node-5'].instance_api.machine_name() == 'Amazon-machine2'
        assert not subject.COMPUTE_INSTANCES
        assert not subject.EC2_INSTANCES

        self.mock_first_instance.start.assert_called_with()
        self.mock_second_instance.start.assert_called_with()
        self.mock_first_compute_instance.start_instance.assert_called_with()
        self.mock_second_compute_instance.start_instance.assert_called_with()
        self.mock_first_ec2_instance.start_instance.assert_called_with()
        self.mock_second_ec2_instance.start_instance.assert_called_with()

    def test_command_with_one_cloud_when_prompted(self, mocker, instances, printing):
        real_command = subject.command()

        assert real_command.name == 'init'
        assert real_command.info == 'Configures instances for use during this run of TNT'

        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.side_effect = ['cloud', '1']

        real_command.run_for([])

        assert self.mock_print.mock_calls == [
            mocker.call('\nAvailable configured cloud instances:'),
            mocker.call("\tGoogle: ['Google-machine1', 'Google-machine2']"),
            mocker.call("\tAmazon: ['Amazon-machine1', 'Amazon-machine2']"),
            mocker.call('\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox-machine1', 'VBox-machine2']\n"),
            mocker.call("\tDocker: ['Docker-machine1', 'Docker-machine2']\n"),
            mocker.call("Configured node-2 on Google-machine1 (Compute)")
        ]

        assert mock_input.mock_calls == [
            mocker.call("Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) "),
            mocker.call().strip(),
            mocker.call("How many instances do you want to use? (1-4, or 'all', blank to cancel) "),
            mocker.call().strip()
        ]

        assert subject.INSTANCES['node-0'].index_name() == 'node-0'
        assert subject.INSTANCES['node-1'].index_name() == 'node-1'
        assert subject.INSTANCES['node-2'].instance_api.index_name() == 'g-node-1'
        assert len(subject.COMPUTE_INSTANCES) == 1
        assert len(subject.EC2_INSTANCES) == 2

        self.mock_first_instance.start.assert_called_with()
        self.mock_second_instance.start.assert_called_with()
        self.mock_first_compute_instance.start_instance.assert_called_with()

    def test_command_with_one_vbox_when_prompted(self, mocker, instances, printing):
        real_command = subject.command()

        assert real_command.name == 'init'
        assert real_command.info == 'Configures instances for use during this run of TNT'

        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.side_effect = ['vbox', '1']

        real_command.run_for([])

        assert self.mock_print.mock_calls == [
            mocker.call('\nAvailable configured cloud instances:'),
            mocker.call("\tGoogle: ['Google-machine1', 'Google-machine2']"),
            mocker.call("\tAmazon: ['Amazon-machine1', 'Amazon-machine2']"),
            mocker.call('\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox-machine1', 'VBox-machine2']\n"),
            mocker.call("\tDocker: ['Docker-machine1', 'Docker-machine2']\n"),
            mocker.call("Configured node-2 on VBox-machine1 (VirtualBox)")
        ]

        assert mock_input.mock_calls == [
            mocker.call("Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) "),
            mocker.call().strip(),
            mocker.call("How many instances do you want to use? (1-2, or 'all', blank to cancel) "),
            mocker.call().strip()
        ]

        assert subject.INSTANCES['node-0'].index_name() == 'node-0'
        assert subject.INSTANCES['node-1'].index_name() == 'node-1'
        assert subject.INSTANCES['node-2'].instance_api.index_name() == 'v-node-1'
        assert subject.INSTANCES['node-2'].instance_api.machine_name() == 'VBox-machine1'
        assert len(subject.VIRTUALBOX_INSTANCES) == 1

        self.mock_first_instance.start.assert_called_with()
        self.mock_second_instance.start.assert_called_with()
        self.mock_first_vbox_instance.start_instance.assert_called_with()

    def test_command_with_one_docker_when_prompted(self, mocker, instances, printing):
        real_command = subject.command()

        assert real_command.name == 'init'
        assert real_command.info == 'Configures instances for use during this run of TNT'

        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.side_effect = ['docker', '1']

        real_command.run_for([])

        assert self.mock_print.mock_calls == [
            mocker.call('\nAvailable configured cloud instances:'),
            mocker.call("\tGoogle: ['Google-machine1', 'Google-machine2']"),
            mocker.call("\tAmazon: ['Amazon-machine1', 'Amazon-machine2']"),
            mocker.call('\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox-machine1', 'VBox-machine2']\n"),
            mocker.call("\tDocker: ['Docker-machine1', 'Docker-machine2']\n"),
            mocker.call("Configured node-2 on Docker-machine1 (Docker)")
        ]

        assert mock_input.mock_calls == [
            mocker.call("Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) "),
            mocker.call().strip(),
            mocker.call("How many instances do you want to use? (1-2, or 'all', blank to cancel) "),
            mocker.call().strip()
        ]

        assert subject.INSTANCES['node-0'].index_name() == 'node-0'
        assert subject.INSTANCES['node-1'].index_name() == 'node-1'
        assert subject.INSTANCES['node-2'].instance_api.index_name() == 'd-node-1'
        assert subject.INSTANCES['node-2'].instance_api.machine_name() == 'Docker-machine1'
        assert len(subject.DOCKER_INSTANCES) == 1

        self.mock_first_instance.start.assert_called_with()
        self.mock_second_instance.start.assert_called_with()
        self.mock_first_docker_instance.start_instance.assert_called_with()

    def test_command_node0_with_one_when_prompted(self, mocker, available_instances, printing):
        real_command = subject.command()

        assert real_command.name == 'init'
        assert real_command.info == 'Configures instances for use during this run of TNT'

        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.side_effect = ['cloud', '1']

        real_command.run_for([])

        assert self.mock_print.mock_calls == [
            mocker.call('\nAvailable configured cloud instances:'),
            mocker.call("\tGoogle: ['Google-machine1', 'Google-machine2']"),
            mocker.call("\tAmazon: ['Amazon-machine1', 'Amazon-machine2']"),
            mocker.call('\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox-machine1', 'VBox-machine2']\n"),
            mocker.call("\tDocker: ['Docker-machine1', 'Docker-machine2']\n"),
            mocker.call("Configured node-0 on Google-machine1 (Compute)")
        ]

        assert mock_input.mock_calls == [
            mocker.call("Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) "),
            mocker.call().strip(),
            mocker.call("How many instances do you want to use? (1-4, or 'all', blank to cancel) "),
            mocker.call().strip()
        ]

        assert subject.INSTANCES['node-0'].index_name() == 'node-0'
        assert len(subject.COMPUTE_INSTANCES) == 1
        assert len(subject.EC2_INSTANCES) == 2

        self.mock_first_compute_instance.start_instance.assert_called_with()

    def test_command_with_invalid_group(self, mocker, instances, printing):
        real_command = subject.command()

        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.side_effect = ['invalidgroup', '']

        real_command.run_for([])

        assert self.mock_print.mock_calls == [
            mocker.call('\nAvailable configured cloud instances:'),
            mocker.call("\tGoogle: ['Google-machine1', 'Google-machine2']"),
            mocker.call("\tAmazon: ['Amazon-machine1', 'Amazon-machine2']"),
            mocker.call(
                '\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox-machine1', 'VBox-machine2']\n"),
            mocker.call("\tDocker: ['Docker-machine1', 'Docker-machine2']\n"),
            mocker.call('invalidgroup is not a valid platform group. Try again')
        ]

        assert mock_input.mock_calls == [
            mocker.call("Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) "),
            mocker.call().strip(),
            mocker.call("Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) "),
            mocker.call().strip()
        ]

        assert len(subject.INSTANCES) == 2

    def test_command_with_zero_instances_when_prompted(self, mocker, instances, printing):
        real_command = subject.command()

        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.side_effect = ['cloud', '0']

        real_command.run_for([])

        assert self.mock_print.mock_calls == [
            mocker.call('\nAvailable configured cloud instances:'),
            mocker.call("\tGoogle: ['Google-machine1', 'Google-machine2']"),
            mocker.call("\tAmazon: ['Amazon-machine1', 'Amazon-machine2']"),
            mocker.call(
                '\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox-machine1', 'VBox-machine2']\n"),
            mocker.call("\tDocker: ['Docker-machine1', 'Docker-machine2']\n"),
        ]

        assert mock_input.mock_calls == [
            mocker.call("Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) "),
            mocker.call().strip(),
            mocker.call("How many instances do you want to use? (1-4, or 'all', blank to cancel) "),
            mocker.call().strip()
        ]

        assert len(subject.INSTANCES) == 2

    def test_command_with_blank_to_cancel_when_prompted(self, mocker, instances, printing):
        real_command = subject.command()

        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.side_effect = ['cloud', '']

        real_command.run_for([])

        assert self.mock_print.mock_calls == [
            mocker.call('\nAvailable configured cloud instances:'),
            mocker.call("\tGoogle: ['Google-machine1', 'Google-machine2']"),
            mocker.call("\tAmazon: ['Amazon-machine1', 'Amazon-machine2']"),
            mocker.call(
                '\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox-machine1', 'VBox-machine2']\n"),
            mocker.call("\tDocker: ['Docker-machine1', 'Docker-machine2']\n"),
        ]

        assert mock_input.mock_calls == [
            mocker.call("Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) "),
            mocker.call().strip(),
            mocker.call("How many instances do you want to use? (1-4, or 'all', blank to cancel) "),
            mocker.call().strip()
        ]

        assert len(subject.INSTANCES) == 2

    def test_command_with_too_many_instances_when_prompted(self, mocker, instances, printing):
        real_command = subject.command()

        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.side_effect = ['cloud', '5', '']

        real_command.run_for([])

        assert self.mock_print.mock_calls == [
            mocker.call('\nAvailable configured cloud instances:'),
            mocker.call("\tGoogle: ['Google-machine1', 'Google-machine2']"),
            mocker.call("\tAmazon: ['Amazon-machine1', 'Amazon-machine2']"),
            mocker.call(
                '\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox-machine1', 'VBox-machine2']\n"),
            mocker.call("\tDocker: ['Docker-machine1', 'Docker-machine2']\n"),
            mocker.call('5 is not in range 1-4. Try again')
        ]

        assert mock_input.mock_calls == [
            mocker.call("Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) "),
            mocker.call().strip(),
            mocker.call("How many instances do you want to use? (1-4, or 'all', blank to cancel) "),
            mocker.call().strip(),
            mocker.call("How many instances do you want to use? (1-4, or 'all', blank to cancel) "),
            mocker.call().strip()
        ]

        assert len(subject.INSTANCES) == 2

    def test_command_with_not_a_number_when_prompted(self, mocker, instances, printing):
        real_command = subject.command()

        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.side_effect = ['cloud', 'shouldbenumber', '']

        real_command.run_for([])

        assert self.mock_print.mock_calls == [
            mocker.call('\nAvailable configured cloud instances:'),
            mocker.call("\tGoogle: ['Google-machine1', 'Google-machine2']"),
            mocker.call("\tAmazon: ['Amazon-machine1', 'Amazon-machine2']"),
            mocker.call(
                '\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox-machine1', 'VBox-machine2']\n"),
            mocker.call("\tDocker: ['Docker-machine1', 'Docker-machine2']\n"),
            mocker.call("shouldbenumber isn't a number. Try again")
        ]

        assert mock_input.mock_calls == [
            mocker.call("Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) "),
            mocker.call().strip(),
            mocker.call("How many instances do you want to use? (1-4, or 'all', blank to cancel) "),
            mocker.call().strip(),
            mocker.call("How many instances do you want to use? (1-4, or 'all', blank to cancel) "),
            mocker.call().strip()
        ]

        assert len(subject.INSTANCES) == 2
