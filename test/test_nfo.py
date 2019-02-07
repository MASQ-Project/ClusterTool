# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
import command
import nfo as subject


class TestNfo:

    @pytest.fixture
    def instance(self, mocker):
        self.mock_instance = mocker.Mock(autospec=True)
        self.mock_instance.name = 'bootstrap'
        instance_dict = {'bootstrap': self.mock_instance}
        mocker.patch.object(command, 'INSTANCES', instance_dict)

    def test_name(self):
        assert subject.name() == 'nfo'

    def test_command_properties(self):
        real_command = subject.command()

        assert real_command.name == 'nfo'
        assert real_command.info == "nukes from orbit - it's the only way to be sure. Restarts"

    def test_command(self, instance):
        real_command = subject.command()

        real_command.run_for('bootstrap')

        self.mock_instance.restart.assert_called_with()
