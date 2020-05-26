from collections import deque
from spade.agent import Agent


class Collector(Agent):
    def __init__(
            self,
            jid: str,
            password: str,
            cache_max_size: int = 10,
            verify_security: bool = False
    ):
        """[summary]

        :param jid: [description]
        :type jid: str
        :param password: [description]
        :type password: str
        :param cache_max_size: [description], defaults to 10
        :type cache_max_size: int, optional
        :param verify_security: [description], defaults to False
        :type verify_security: bool, optional
        """
        self._cache = deque([], cache_max_size)
        self._contacts = {}
        self._sent_data = {}
        super().__init__(jid, password, verify_security)

    @property
    def available_contacts(self):
        """[summary]

        :return: [description]
        :rtype: [type]
        """
        return self._contacts

    @property
    def sent_data(self):
        """[summary]

        :return: [description]
        :rtype: [type]
        """
        return self._sent_data

    @property
    def cache(self):
        """[summary]

        :return: [description]
        :rtype: [type]
        """
        return self._cache
