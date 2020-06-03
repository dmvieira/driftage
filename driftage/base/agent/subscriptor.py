from spade.agent import Agent


class Subscriptor(Agent):
    def __init__(
            self,
            jid: str,
            password: str,
            verify_security: bool = False
    ):
        """[summary]

        :param jid: [description]
        :type jid: str
        :param password: [description]
        :type password: str
        :param verify_security: [description], defaults to False
        :type verify_security: bool, optional
        """
        self._contacts = {}
        super().__init__(jid, password, verify_security)

    @property
    def available_contacts(self):
        """[summary]

        :return: [description]
        :rtype: [type]
        """
        return self._contacts
