# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
import os
import node_commands
from node_ssh_commands import NodeSshCommands


class TestNodeSshCommands:

    @pytest.fixture
    def mocks(self, mocker):
        self.mock_executor = mocker.patch('node_ssh_commands.Executor')
        self.mock_terminal_executor = mocker.patch(
            'node_ssh_commands.TerminalExecutor'
        )
        self.mock_tnt_config = mocker.patch('node_ssh_commands.tnt_config')
        self.mock_tnt_config.INSTANCE_USER = 'mockeduser'

    def test_init(self, mocks):
        subject = NodeSshCommands('ip fn')

        assert subject.get_ip == 'ip fn'
        self.mock_terminal_executor.assert_called_with(
            self.mock_executor.return_value
        )

    def test_start(self, mocks):
        subject = NodeSshCommands(lambda: '1.2.3.4')
        node_args = {
            'dns-servers': '--dns-servers 1.1.1.1,8.8.8.8',
            'log-level': '--log-level debug',
            'data-directory': '--data-directory /tmp',
            'ip': '--ip 1.2.3.4',
            'earning-wallet': '--earning-wallet 0xF00DFACE',
            'consuming-private-key': '--consuming-private-key 89d59b93ef6a94c977e1812b727d5f123f7d825ab636e83aad3e2845a68eaedb',
            'additional-args': 'hi'
        }
        self.mock_executor.return_value.execute_sync.return_value = 'started'

        result = subject.start(node_args)

        self.mock_executor.return_value.execute_sync.assert_called_with([
            'ssh', '-oStrictHostKeyChecking=no', 'mockeduser@1.2.3.4',
            'sudo ./MASQNode',
            '--dns-servers', '1.1.1.1,8.8.8.8',
            '--log-level', 'debug',
            '--data-directory', '/tmp',
            '--ip', '1.2.3.4',
            '--earning-wallet', '0xF00DFACE',
            '--consuming-private-key', '89d59b93ef6a94c977e1812b727d5f123f7d825ab636e83aad3e2845a68eaedb',
            'hi',
            '>', '/dev/null', '2>&1', '&'
        ])

        assert result == 'started'

    def test_start_no_additional_args(self, mocks):
        subject = NodeSshCommands(lambda: '1.2.3.4')
        node_args = {
            'dns-servers': '--dns-servers 1.1.1.1,8.8.8.8',
            'log-level': '--log-level debug',
            'data-directory': '--data-directory /tmp',
            'ip': '--ip 1.2.3.4',
            'earning-wallet': '--earning-wallet 0xF00DFACE',
            'consuming-private-key': '--consuming-private-key 89d59b93ef6a94c977e1812b727d5f123f7d825ab636e83aad3e2845a68eaedb',
        }
        self.mock_executor.return_value.execute_sync.return_value = 'started'

        result = subject.start(node_args)

        self.mock_executor.return_value.execute_sync.assert_called_with([
            'ssh', '-oStrictHostKeyChecking=no', 'mockeduser@1.2.3.4',
            'sudo ./MASQNode',
            '--dns-servers', '1.1.1.1,8.8.8.8',
            '--log-level', 'debug',
            '--data-directory', '/tmp',
            '--ip', '1.2.3.4',
            '--earning-wallet', '0xF00DFACE',
            '--consuming-private-key', '89d59b93ef6a94c977e1812b727d5f123f7d825ab636e83aad3e2845a68eaedb',
            '>', '/dev/null', '2>&1', '&'
        ])
        assert result == 'started'

    def test_stop(self, mocks):
        subject = NodeSshCommands(lambda: '1.2.3.4')
        self.mock_executor.return_value.execute_sync.return_value = 'stopped'

        result = subject.stop()

        self.mock_executor.return_value.execute_sync.assert_called_with([
            'ssh', '-oStrictHostKeyChecking=no', 'mockeduser@1.2.3.4',
            node_commands.STOP_COMMAND
        ])
        assert result == 'stopped'

    def test_cat_logs(self, mocks):
        subject = NodeSshCommands(lambda: '1.2.3.4')
        self.mock_executor.return_value.execute_async.return_value = 'meow'

        result = subject.cat_logs()

        self.mock_executor.return_value.execute_async.assert_called_with([
            'ssh', '-oStrictHostKeyChecking=no', 'mockeduser@1.2.3.4',
            node_commands.CAT_LOGS_COMMAND
        ])
        assert result == 'meow'

    def test_delete_logs(self, mocks):
        subject = NodeSshCommands(lambda: '1.2.3.4')
        self.mock_executor.return_value.execute_sync.return_value = 'deleted'

        result = subject.delete_logs()

        self.mock_executor.return_value.execute_sync.assert_called_with([
            'ssh', '-oStrictHostKeyChecking=no', 'mockeduser@1.2.3.4',
            node_commands.DELETE_LOGS_COMMAND
        ])
        assert result == 'deleted'

    def test_retrieve_logs(self, mocks):
        subject = NodeSshCommands(lambda: '1.2.3.4')
        self.mock_executor.return_value.execute_sync.return_value = 'retrieved'

        result = subject.retrieve_logs('dest')

        self.mock_executor.return_value.execute_sync.assert_called_with([
            'scp', '-oStrictHostKeyChecking=no',
            'mockeduser@1.2.3.4:/tmp/MASQNode_rCURRENT.log',
            'dest'
        ])
        assert result == 'retrieved'

    def test_update(self, mocks):
        subject = NodeSshCommands(lambda: '1.2.3.4')
        self.mock_executor.return_value.execute_sync.return_value = 'updated'

        result = subject.update('binary')

        self.mock_executor.return_value.execute_sync.assert_called_with([
            'scp', '-oStrictHostKeyChecking=no',
            os.path.join('binaries', 'binary'),
            'mockeduser@1.2.3.4:binary',
        ])
        assert result == 'updated'

    def test_tail(self, mocks):
        subject = NodeSshCommands(lambda: '1.2.3.4')
        self.mock_terminal_executor.return_value.execute_in_new_terminal\
            .return_value = 'tailing'

        result = subject.tail()

        self.mock_terminal_executor.return_value.execute_in_new_terminal\
            .assert_called_with(
                '1.2.3.4 ssh -oStrictHostKeyChecking=no mockeduser@1.2.3.4 %s' %
                node_commands.TAIL_LOGS_COMMAND
            )
        assert result == 'tailing'

    def test_shell(self, mocks):
        subject = NodeSshCommands(lambda: '1.2.3.4')
        self.mock_terminal_executor.return_value.execute_in_new_terminal\
            .return_value = 'shell'

        result = subject.shell()

        self.mock_terminal_executor.return_value.execute_in_new_terminal\
            .assert_called_with(
                '1.2.3.4 ssh -oStrictHostKeyChecking=no mockeduser@1.2.3.4'
            )
        assert result == 'shell'
