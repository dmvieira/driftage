import json
from datetime import datetime
from typing import Optional
from driftage.base.agent.subscriptor import Subscriptor
from spade.template import Template
from driftage.monitor.behaviour.fast_notify_contacts import FastNotifyContacts
from driftage.monitor.behaviour.wait_monitor_subscriptions import (
    WaitMonitorSubscriptions)
from driftage.base.conf import getLogger


class Monitor(Subscriptor):
    def __init__(
            self,
            jid: str,
            password: str,
            identifier: Optional[str] = None,
            verify_security: bool = False
    ):
        """[summary]

        :param jid: [description]
        :type jid: str
        :param password: [description]
        :type password: str
        :param identifier: [description], defaults to None
        :type identifier: Optional[str], optional
        :param verify_security: [description], defaults to False
        :type verify_security: bool, optional
        """
        super().__init__(jid, password, verify_security)
        self._identifier = identifier if identifier else self.name
        self._logger = getLogger("monitor")

    async def setup(self):
        """[summary]
        """
        self.add_behaviour(WaitMonitorSubscriptions())
        self._logger.info("Monitor started")

    def collect(self, data: dict):
        """[summary]

        :param data: [description]
        :type data: dict
        """
        self.add_behaviour(
            FastNotifyContacts(), template=Template(body=json.dumps({
                "data": data,
                "metadata": {
                    "timestamp": datetime.utcnow().timestamp(),
                    "identifier": self._identifier
                }
            })))

    __call__ = collect
