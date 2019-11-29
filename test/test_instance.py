# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
from mock import MagicMock

from instance import Instance

class TestInstance:

    @pytest.fixture
    def subject(self, mocker):
        instance_api = mocker.Mock(autospec=True)
        instance_api.machine_name = mocker.Mock(return_value='billy')
        self.subject = Instance(1, instance_api)

    def test_init(self, subject):
        assert self.subject.index_name() == 'node-1'
        assert self.subject.machine_name() == 'billy'

    def test_start(self, subject):
        result = self.subject.start()

        assert result == self.subject
        self.subject.instance_api.start_instance.assert_called_with()

    def test_kill(self, subject):
        result = self.subject.kill()

        assert result == self.subject.instance_api.stop_instance.return_value
        self.subject.instance_api.stop_instance.assert_called_with()

    def test_restart(self, subject):
        result = self.subject.restart()

        assert result == self.subject.instance_api.restart_instance.return_value
        self.subject.instance_api.restart_instance.assert_called_with()

    def test_get_ip(self, subject):
        result = self.subject.get_ip()

        assert result == self.subject.instance_api.get_external_ip.return_value
        self.subject.instance_api.get_external_ip.assert_called_with()

    def test_shell(self, subject):
        self.subject.shell()

        self.subject.node.shell.assert_called_with()

    def test_update(self, subject):
        self.subject.update()

        self.subject.node.update.assert_called_with()

    def test_start_node(self, subject):
        result = self.subject.start_node('booga')

        assert result == self.subject.node.start.return_value
        self.subject.node.start.assert_called_with(self.subject.instance_api.get_external_ip.return_value, 'booga')

    def test_stop_node(self, subject):
        self.subject.stop_node()

        self.subject.dns.revert.assert_called_with()
        self.subject.traffic.stop.assert_called_with()
        self.subject.node.shutdown.assert_called_with()

    def test_retrieve_logs(self, subject):
        self.subject.retrieve_logs("dir")

        self.subject.node.retrieve_logs.assert_called_with("dir")

    def test_tail(self, subject):
        self.subject.tail()

        self.subject.node.tail.assert_called_with()

    def test_inspect(self, subject):
        self.subject.inspect()

        self.subject.node.display_neighborhood.assert_called_with()

    def test_inbound(self, subject):
        self.subject.inbound()

        self.subject.node.gossip_received.assert_called_with()

    def test_outbound(self, subject):
        self.subject.outbound()

        self.subject.node.gossip_produced.assert_called_with()

    def test_subvert(self, subject):
        self.subject.subvert()

        self.subject.dns.subvert.assert_called_with()

    def test_revert(self, subject):
        self.subject.revert()

        self.subject.traffic.stop.assert_called_with()
        self.subject.dns.revert.assert_called_with()

    def test_verify(self, subject):
        self.subject.verify()

        self.subject.traffic.verify.assert_called_with()

    def test_curl(self, subject):
        self.subject.curl()

        self.subject.dns.subvert.assert_called_with()
        self.subject.traffic.curl.assert_called_with()

    def test_wget(self, subject):
        self.subject.wget()

        self.subject.dns.subvert.assert_called_with()
        self.subject.traffic.wget.assert_called_with()
