# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
import tnt_config
import nfo as subject


class TestNfo:

    @pytest.fixture
    def instance(self, mocker):
        self.mock_instance = mocker.Mock(autospec=True)
        self.mock_instance._index_name = 'node-0'
        instance_dict = {'node-0': self.mock_instance}
        mocker.patch.object(tnt_config, 'INSTANCES', instance_dict)

    def test_name(self):
        assert subject.name() == 'nfo'

    def test_command_properties(self):
        real_command = subject.command()

        assert real_command.name == 'nfo'
        assert real_command.info == "nukes from orbit - it's the only way to be sure. Restarts"

    def test_command(self, instance):
        real_command = subject.command()

        real_command.run_for('node-0')

        self.mock_instance.restart.assert_called_with()
