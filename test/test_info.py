# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
from info import *
import tnt_config


class TestInfo:

    @pytest.fixture
    def printing(self, mocker):
        self.mock_print = mocker.patch('__builtin__.print')

    @pytest.fixture
    def instances(self, mocker):
        self.mock_first_instance = mocker.MagicMock()
        self.mock_first_instance.get_ip.return_value = '1.2.3.4'
        self.mock_first_instance.instance_api.__class__ = 'FirstClass'
        self.mock_second_instance = mocker.MagicMock()
        self.mock_second_instance.get_ip.return_value = '2.3.4.5'
        self.mock_second_instance.instance_api.__class__ = 'SecondClass'
        tnt_config.INSTANCES = {'first': self.mock_first_instance, 'second': self.mock_second_instance}

    def test_name(self):
        assert name() == 'info'

    def test_command(self, mocker, instances, printing):
        real_command = command()

        assert real_command.name == 'info'
        assert real_command.info == 'Prints running instance info'

        real_command.run_for([])

        assert self.mock_print.mock_calls == [
            mocker.call('first @ 1.2.3.4 (FirstClass)'),
            mocker.call('second @ 2.3.4.5 (SecondClass)')
        ]
