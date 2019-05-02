# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest

from executor import TerminalExecutor


class TestTerminalExecutor:

    @pytest.fixture
    def mocks(self, mocker):
        self.mock_executor = mocker.Mock()

    @pytest.fixture
    def linux(self, mocker):
        mock_sys = mocker.patch('executor.sys')
        mock_sys.platform = 'linux2'

    @pytest.fixture
    def printing(self, mocker):
        self.mock_print = mocker.patch('__builtin__.print')

    @pytest.fixture
    def copyfile(self, mocker):
	self.mock_copyfile = mocker.patch('shutil.copyfile')

    @pytest.fixture
    def mac_os(self, mocker):
        mock_sys = mocker.patch('executor.sys')
        mock_sys.platform = 'darwin'

    @pytest.fixture
    def unknown_platform(self, mocker):
        mock_sys = mocker.patch('executor.sys')
        mock_sys.platform = 'unknown'

    def test_execute_in_new_terminal_for_linux(self, mocks, linux, copyfile, mocker):
        from mock import patch, mock_open
        with patch("__builtin__.open", mock_open(), create=True) as mock_file, patch('os.chmod') as mock_chmod:
	    self.mock_executor.execute_sync.return_value = 'executed'
	    subject = TerminalExecutor(self.mock_executor)

	    result = subject.execute_in_new_terminal('the command')

	    self.mock_copyfile.assert_called_with('./tnt_wrapper.sh', '/tmp/tnt_wrapper.sh')
            mock_file.assert_called_with("/tmp/tnt_terminal.sh", 'w')
            assert mock_chmod.mock_calls == [
		mocker.call('/tmp/tnt_wrapper.sh', 0755),
		mocker.call('/tmp/tnt_terminal.sh', 0755)
	    ]
	    self.mock_executor.execute_sync.assert_called_with([
	       'gnome-terminal', '--geometry', '180x24+0+0', '-e', '/tmp/tnt_terminal.sh'
	    ])
	    assert result == 'executed'

    def test_execute_in_new_terminal_for_unknown_platform(self, mocks, printing, unknown_platform, mocker):
        subject = TerminalExecutor(self.mock_executor)

        result = subject.execute_in_new_terminal('the command')

        assert self.mock_print.mock_calls == [
            mocker.call('\tThis TNT command is not yet supported on the current platform (unknown)')
        ]
        assert self.mock_executor.execute_sync.call_count == 0
        assert result is None

    def test_execute_in_new_terminal_for_mac_os(self, mocks, mac_os, copyfile, mocker):
        from mock import patch, mock_open
        with patch("__builtin__.open", mock_open(), create=True) as mock_file, patch('os.chmod') as mock_chmod:
            subject = TerminalExecutor(self.mock_executor)
            self.mock_executor.execute_sync.return_value = 'executed'

            result = subject.execute_in_new_terminal('the command')

	    self.mock_copyfile.assert_called_with('./tnt_wrapper.sh', '/tmp/tnt_wrapper.sh')
            mock_file.assert_called_with("/tmp/tnt_terminal.sh", 'w')
            assert mock_chmod.mock_calls == [
		mocker.call('/tmp/tnt_wrapper.sh', 0755),
		mocker.call('/tmp/tnt_terminal.sh', 0755)
	    ]

            self.mock_executor.execute_sync.assert_called_with([
                'open', '-n', '-a', 'iTerm', '--args', '/tmp/tnt_terminal.sh'
            ])
            assert result == 'executed'
