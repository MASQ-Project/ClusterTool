# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
import update as subject


class TestInfo:

    @pytest.fixture
    def mocks(self, mocker):
        self.mock_first_instance = mocker.MagicMock()
        self.mock_second_instance = mocker.MagicMock()
        mocker.patch.dict(
            'tnt_config.INSTANCES',
            first=self.mock_first_instance,
            second=self.mock_second_instance
        )

    def test_name(self):
        assert subject.name() == 'update'

    def test_command(self, mocks):
        real_command = subject.command()

        assert real_command.name == 'update'
        assert real_command.info == \
            'sends updated binaries (from pwd) and then nfo'

        real_command.run_for('all')

        self.mock_first_instance.update.assert_called_with()
        self.mock_second_instance.update.assert_called_with()
