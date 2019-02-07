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
        self.mock_first_compute_instance.name = 'Google1'
        self.mock_second_compute_instance.name = 'Google2'
        self.mock_first_compute_instance.__class__ = 'Compute'
        self.mock_second_compute_instance.__class__ = 'Compute'
        mocker.patch.object(subject, 'COMPUTE_INSTANCES', [
            self.mock_first_compute_instance,
            self.mock_second_compute_instance
        ])

        self.mock_first_ec2_instance = mocker.Mock()
        self.mock_second_ec2_instance = mocker.Mock()
        self.mock_first_ec2_instance.name = 'Amazon1'
        self.mock_second_ec2_instance.name = 'Amazon2'
        self.mock_first_ec2_instance.__class__ = 'EC2'
        self.mock_second_ec2_instance.__class__ = 'EC2'
        mocker.patch.object(subject, 'EC2_INSTANCES', [
            self.mock_first_ec2_instance,
            self.mock_second_ec2_instance
        ])

        self.mock_first_vbox_instance = mocker.Mock()
        self.mock_second_vbox_instance = mocker.Mock()
        self.mock_first_vbox_instance.name = 'VBox1'
        self.mock_second_vbox_instance.name = 'VBox2'
        self.mock_first_vbox_instance.__class__ = 'VirtualBox'
        self.mock_second_vbox_instance.__class__ = 'VirtualBox'
        mocker.patch.object(subject, 'VIRTUALBOX_INSTANCES', [
            self.mock_first_vbox_instance,
            self.mock_second_vbox_instance
        ])

        self.mock_first_docker_instance = mocker.Mock()
        self.mock_second_docker_instance = mocker.Mock()
        self.mock_first_docker_instance.name = 'Docker1'
        self.mock_second_docker_instance.name = 'Docker2'
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
        self.mock_first_instance.name = 'bootstrap'
        self.mock_second_instance.name = 'node-1'
        self.mock_first_instance.__class__ = 'ExistingClass'
        self.mock_second_instance.__class__ = 'ExistingClass'
        mocker.patch.object(subject, 'INSTANCES', {
            'bootstrap': self.mock_first_instance,
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
            mocker.call("\tGoogle: ['Google1', 'Google2']"),
            mocker.call("\tAmazon: ['Amazon1', 'Amazon2']"),
            mocker.call('\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox1', 'VBox2']\n"),
            mocker.call("\tDocker: ['Docker1', 'Docker2']\n"),
            mocker.call("Configured node-2 on Google1 (Compute)"),
            mocker.call("Configured node-3 on Google2 (Compute)"),
            mocker.call("Configured node-4 on Amazon1 (EC2)"),
            mocker.call("Configured node-5 on Amazon2 (EC2)")
        ]

        assert mock_input.called_with("Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) ")
        assert mock_input.called_with("How many instances do you want to use? (1-4, or 'all', blank to cancel")

        assert subject.INSTANCES['bootstrap'].name == 'bootstrap'
        assert subject.INSTANCES['node-1'].name == 'node-1'
        assert subject.INSTANCES['node-2'].instance_api.name == 'Google1'
        assert subject.INSTANCES['node-3'].instance_api.name == 'Google2'
        assert subject.INSTANCES['node-4'].instance_api.name == 'Amazon1'
        assert subject.INSTANCES['node-5'].instance_api.name == 'Amazon2'
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
            mocker.call("\tGoogle: ['Google1', 'Google2']"),
            mocker.call("\tAmazon: ['Amazon1', 'Amazon2']"),
            mocker.call('\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox1', 'VBox2']\n"),
            mocker.call("\tDocker: ['Docker1', 'Docker2']\n"),
            mocker.call("Configured node-2 on Google1 (Compute)")
        ]

        assert mock_input.called_with("Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) ")
        assert mock_input.called_with("How many instances do you want to use? (1-4, or 'all', blank to cancel")

        assert subject.INSTANCES['bootstrap'].name == 'bootstrap'
        assert subject.INSTANCES['node-1'].name == 'node-1'
        assert subject.INSTANCES['node-2'].instance_api.name == 'Google1'
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
            mocker.call("\tGoogle: ['Google1', 'Google2']"),
            mocker.call("\tAmazon: ['Amazon1', 'Amazon2']"),
            mocker.call('\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox1', 'VBox2']\n"),
            mocker.call("\tDocker: ['Docker1', 'Docker2']\n"),
            mocker.call("Configured node-2 on VBox1 (VirtualBox)")
        ]

        assert mock_input.called_with("Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) ")
        assert mock_input.called_with("How many instances do you want to use? (1-4, or 'all', blank to cancel")

        assert subject.INSTANCES['bootstrap'].name == 'bootstrap'
        assert subject.INSTANCES['node-1'].name == 'node-1'
        assert subject.INSTANCES['node-2'].instance_api.name == 'VBox1'
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
            mocker.call("\tGoogle: ['Google1', 'Google2']"),
            mocker.call("\tAmazon: ['Amazon1', 'Amazon2']"),
            mocker.call('\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox1', 'VBox2']\n"),
            mocker.call("\tDocker: ['Docker1', 'Docker2']\n"),
            mocker.call("Configured node-2 on Docker1 (Docker)")
        ]

        assert mock_input.called_with("Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) ")
        assert mock_input.called_with("How many instances do you want to use? (1-4, or 'all', blank to cancel")

        assert subject.INSTANCES['bootstrap'].name == 'bootstrap'
        assert subject.INSTANCES['node-1'].name == 'node-1'
        assert subject.INSTANCES['node-2'].instance_api.name == 'Docker1'
        assert len(subject.DOCKER_INSTANCES) == 1

        self.mock_first_instance.start.assert_called_with()
        self.mock_second_instance.start.assert_called_with()
        self.mock_first_docker_instance.start_instance.assert_called_with()

    def test_command_bootstrap_with_one_when_prompted(self, mocker, available_instances, printing):
        real_command = subject.command()

        assert real_command.name == 'init'
        assert real_command.info == 'Configures instances for use during this run of TNT'

        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.side_effect = ['cloud', '1']

        real_command.run_for([])

        assert self.mock_print.mock_calls == [
            mocker.call('\nAvailable configured cloud instances:'),
            mocker.call("\tGoogle: ['Google1', 'Google2']"),
            mocker.call("\tAmazon: ['Amazon1', 'Amazon2']"),
            mocker.call('\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox1', 'VBox2']\n"),
            mocker.call("\tDocker: ['Docker1', 'Docker2']\n"),
            mocker.call("Configured bootstrap on Google1 (Compute)")
        ]

        assert mock_input.called_with("Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) ")
        assert mock_input.called_with("How many instances do you want to use? (1-4, or 'all', blank to cancel")

        assert subject.INSTANCES['bootstrap'].name == 'bootstrap'
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
            mocker.call("\tGoogle: ['Google1', 'Google2']"),
            mocker.call("\tAmazon: ['Amazon1', 'Amazon2']"),
            mocker.call(
                '\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox1', 'VBox2']\n"),
            mocker.call("\tDocker: ['Docker1', 'Docker2']\n"),
            mocker.call('invalidgroup is not a valid platform group. Try again')
        ]

        assert mock_input.called_with(
            "Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) ")

        assert len(subject.INSTANCES) == 2

    def test_command_with_zero_instances_when_prompted(self, mocker, instances, printing):
        real_command = subject.command()

        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.side_effect = ['cloud', '0']

        real_command.run_for([])

        assert self.mock_print.mock_calls == [
            mocker.call('\nAvailable configured cloud instances:'),
            mocker.call("\tGoogle: ['Google1', 'Google2']"),
            mocker.call("\tAmazon: ['Amazon1', 'Amazon2']"),
            mocker.call(
                '\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox1', 'VBox2']\n"),
            mocker.call("\tDocker: ['Docker1', 'Docker2']\n")
        ]

        assert mock_input.called_with(
            "Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) ")
        assert mock_input.called_with("How many instances do you want to use? (1-4, or 'all', blank to cancel")

        assert len(subject.INSTANCES) == 2

    def test_command_with_blank_to_cancel_when_prompted(self, mocker, instances, printing):
        real_command = subject.command()

        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.side_effect = ['cloud', '']

        real_command.run_for([])

        assert self.mock_print.mock_calls == [
            mocker.call('\nAvailable configured cloud instances:'),
            mocker.call("\tGoogle: ['Google1', 'Google2']"),
            mocker.call("\tAmazon: ['Amazon1', 'Amazon2']"),
            mocker.call(
                '\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox1', 'VBox2']\n"),
            mocker.call("\tDocker: ['Docker1', 'Docker2']\n")
        ]

        assert mock_input.called_with(
            "Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) ")
        assert mock_input.called_with("How many instances do you want to use? (1-4, or 'all', blank to cancel")

        assert len(subject.INSTANCES) == 2

    def test_command_with_too_many_instances_when_prompted(self, mocker, instances, printing):
        real_command = subject.command()

        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.side_effect = ['cloud', '5', '']

        real_command.run_for([])

        assert self.mock_print.mock_calls == [
            mocker.call('\nAvailable configured cloud instances:'),
            mocker.call("\tGoogle: ['Google1', 'Google2']"),
            mocker.call("\tAmazon: ['Amazon1', 'Amazon2']"),
            mocker.call(
                '\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox1', 'VBox2']\n"),
            mocker.call("\tDocker: ['Docker1', 'Docker2']\n"),
            mocker.call('5 is not in range 1-4. Try again')
        ]

        assert mock_input.called_with(
            "Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) ")
        assert mock_input.called_with("How many instances do you want to use? (1-4, or 'all', blank to cancel")

        assert len(subject.INSTANCES) == 2

    def test_command_with_not_a_number_when_prompted(self, mocker, instances, printing):
        real_command = subject.command()

        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.side_effect = ['cloud', 'shouldbenumber', '']

        real_command.run_for([])

        assert self.mock_print.mock_calls == [
            mocker.call('\nAvailable configured cloud instances:'),
            mocker.call("\tGoogle: ['Google1', 'Google2']"),
            mocker.call("\tAmazon: ['Amazon1', 'Amazon2']"),
            mocker.call(
                '\nAvailable configured local instances (probably cannot be used alongside above):'),
            mocker.call("\tVirtualBox: ['VBox1', 'VBox2']\n"),
            mocker.call("\tDocker: ['Docker1', 'Docker2']\n"),
            mocker.call("shouldbenumber isn't a number. Try again")
        ]

        assert mock_input.called_with(
            "Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) ")
        assert mock_input.called_with("How many instances do you want to use? (1-4, or 'all', blank to cancel")

        assert len(subject.INSTANCES) == 2
