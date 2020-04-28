#!/usr/bin/env python3

import sys
sys.path.append('lib')
from ops.charm import CharmBase  # NoQA: E402
from ops.framework import StoredState  # NoQA: E402
from ops.main import main  # NoQA: E402
from ops.model import (  # NoQA: E402
    ActiveStatus,
    MaintenanceStatus,
    WaitingStatus,
)

import logging  # NoQA: E402
logger = logging.getLogger()


class MattermostK8sCharm(CharmBase):

    state = StoredState()

    def __init__(self, *args):
        self.framework.observe(self.on.start, self.configure_pod)
        self.framework.observe(self.on.config_changed, self.configure_pod)
        self.framework.observe(self.on.upgrade_charm, self.configure_pod)

    def configure_pod(self, event):
        if not self.framework.model.unit.is_leader():
            self.model.unit.status = WaitingStatus('Not a leader')
            return
        self.model.unit.status = MaintenanceStatus('Configuring pod')
        config = self.model.config
        self.model.pod.set_spec({
            'containers': [{
                'name': self.framework.model.app.name,
                'imageDetails': {"imagePath": config["mattermost_image"]},
                'ports': [{
                    'containerPort': int(self.framework.model.config['mattermost_port']),
                    'protocol': 'TCP',
                }],
                'env': {
                    'MATTERMOST_HTTPD_LISTEN_PORT': int(self.framework.model.config['mattermost_port']),
                    'DB_HOST': int(self.framework.model.config['pg_db_host']),
                    'DB_PORT_NUMBER': int(self.framework.model.config['pg_db_port']),
                    'MM_USERNAME': int(self.framework.model.config['pg_user']),
                    'MM_PASSWORD': int(self.framework.model.config['pg_password']),
                },
            }]
        })
        self.state.is_started = True
        self.model.unit.status = ActiveStatus()
 

if __name__ == '__main__':
    main(MattermostK8sCharm)
