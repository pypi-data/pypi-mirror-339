from typing import List

from kuhl_haus.canary.env import CANARY_CONFIG_FILE_PATH, RESOLVERS_CONFIG_FILE_PATH
from kuhl_haus.canary.models.dns_resolver import DnsResolver, DnsResolverList
from kuhl_haus.canary.models.endpoint_model import EndpointModel
from kuhl_haus.canary.scripts.script import Script
from kuhl_haus.canary.tasks.dns_check import query_dns
from kuhl_haus.canary.tasks.http_health_check import invoke_health_check
from kuhl_haus.canary.tasks.tls import invoke_tls_check


class Canary(Script):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def invoke(self):
        self.__invoke_endpoint_checks()

    def __invoke_endpoint_checks(self):
        endpoints = EndpointModel.from_file(CANARY_CONFIG_FILE_PATH)
        resolvers = DnsResolverList.from_file(RESOLVERS_CONFIG_FILE_PATH)
        if not endpoints:
            self.recorder.logger.info(f"No endpoints found, exiting.")
            return
        for ep in endpoints:
            if ep.ignore:
                self.recorder.logger.info(f"Skipping {ep.mnemonic}")
                continue
            try:
                self.__invoke_dns_check(ep=ep, resolvers=resolvers)
                self.__invoke_tls_check(ep=ep)
                self.__invoke_health_check(ep=ep)
            except Exception as e:
                self.recorder.logger.exception(
                    msg=f"Unhandled exception testing mnemonic:{ep.mnemonic}",
                    exc_info=e
                )

    def __invoke_health_check(self, ep: EndpointModel):
        metrics = self.recorder.get_metrics(mnemonic=ep.mnemonic, hostname=ep.hostname)
        invoke_health_check(ep=ep, metrics=metrics, logger=self.recorder.logger)
        self.recorder.log_metrics(metrics)

    def __invoke_tls_check(self, ep: EndpointModel):
        metrics = self.recorder.get_metrics(mnemonic="tls", hostname=ep.hostname)
        invoke_tls_check(ep=ep, metrics=metrics, logger=self.recorder.logger)
        self.recorder.log_metrics(metrics)

    def __invoke_dns_check(self, ep: EndpointModel, resolvers: List[DnsResolver]):
        if resolvers:
            metrics = self.recorder.get_metrics(mnemonic="dns", hostname=ep.hostname)
            query_dns(resolvers=resolvers, ep=ep, metrics=metrics, logger=self.recorder.logger)
            self.recorder.log_metrics(metrics)
