# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest

import tnt_config
from binaries_command import BinariesCommand


class TestBinaryCommand:
    def setup_method(self, method):
        pass

    @pytest.fixture
    def instances(self, mocker):
        instance1 = mocker.Mock()
        instance1.binaries_version = None
        instance2 = mocker.Mock()
        instance2.binaries_version = None
        instance3 = mocker.Mock()
        instance3.binaries_version = None
        mocker.patch.dict('tnt_config.INSTANCES', first=instance1, second=instance2, third=instance3)

    def test_construction(self):
        subject = BinariesCommand()

        assert subject.name == 'binaries'
        assert subject.info == 'assigns binaries in /binaries subdirectory to a Node before it is started'
        assert subject.sub_fn() == 0

    def test_display(self, mocker):
        subject = BinariesCommand()
        mock_print = mocker.patch('__builtin__.print')
        subject.display()

        mock_print.assert_called_with("\tbinaries----------> Prompts for instance name then sets the directory from which the binaries will be drawn for that instance")

    def test_run_for_with_no_input_will_prompt(self, instances, mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.side_effect = ['first', '']

        subject = BinariesCommand()

        subject.run_for('specific')

        assert tnt_config.INSTANCES['first'].binaries_version == 'specific'
        assert tnt_config.INSTANCES['second'].binaries_version is None
        assert tnt_config.INSTANCES['third'].binaries_version is None

    def test_all_when_prompted_finishes(self, instances,  mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value = 'all'

        subject = BinariesCommand()

        subject.run_for('specific')

        assert tnt_config.INSTANCES['first'].binaries_version == 'specific'
        assert tnt_config.INSTANCES['second'].binaries_version == 'specific'
        assert tnt_config.INSTANCES['third'].binaries_version == 'specific'

    def test_run_for_specific_instances(self, instances):
        subject = BinariesCommand()

        subject.run_for('specific third first third')

        assert tnt_config.INSTANCES['first'].binaries_version == 'specific'
        assert tnt_config.INSTANCES['second'].binaries_version is None
        assert tnt_config.INSTANCES['third'].binaries_version == 'specific'

    def test_run_for_all(self, instances):
        subject = BinariesCommand()

        subject.run_for('   specific   all')

        assert tnt_config.INSTANCES['first'].binaries_version == 'specific'
        assert tnt_config.INSTANCES['second'].binaries_version == 'specific'
        assert tnt_config.INSTANCES['third'].binaries_version == 'specific'

    def test_complains_when_instance_is_not_known(self, instances, mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.side_effect = ['first', '']
        mock_print = mocker.patch('__builtin__.print')

        subject = BinariesCommand()

        subject.run_for('specific notaninstance')

        mock_print.assert_called_with("\tno known instance called notaninstance")
        assert tnt_config.INSTANCES['first'].binaries_version == 'specific'
        assert tnt_config.INSTANCES['second'].binaries_version is None
        assert tnt_config.INSTANCES['third'].binaries_version is None
