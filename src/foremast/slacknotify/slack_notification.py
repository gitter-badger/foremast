"""Notify Slack channel."""
import time

from ..utils import get_properties, get_template, post_slack_message


class SlackNotification:
    """Post slack notification.

    Inform users about infrastructure changes to prod* accounts.
    """

    def __init__(self, app=None, env=None, prop_path=None):
        timestamp = time.strftime("%B %d, %Y %H:%M:%S %Z", time.gmtime())

        self.settings = get_properties(prop_path)
        short_commit_sha = self.settings['pipeline']['config_commit'][0:11]

        self.info = {
            'app': app,
            'env': env,
            'config_commit_short': short_commit_sha,
            'timestamp': timestamp,
        }

    def post_message(self):
        """Send templated message to **#deployments-{env}**."""
        message = get_template(
            template_file='slack-templates/pipeline-prepare-ran.j2',
            info=self.info)
        channel = '#deployments-{}'.format(self.info['env'].lower())
        post_slack_message(message, channel)

    def notify_slack_channel(self):
        """Post message to a defined Slack channel."""
        message = get_template(
            template_file='slack-templates/pipeline-prepare-ran.j2',
            info=self.info)

        if self.settings['pipeline']['notifications']['slack']:
            post_slack_message(
                message, self.settings['pipeline']['notifications']['slack'])
