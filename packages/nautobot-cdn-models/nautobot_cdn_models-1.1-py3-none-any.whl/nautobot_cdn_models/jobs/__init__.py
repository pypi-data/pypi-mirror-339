
from nautobot.core.celery import register_jobs
from .CheckBGPCommunities import CheckBGPCommunities
from .bulk_hpc_add import NewHpcs
from .deploy_update_site_button import DeployAkamaiSite
from .node_lcdn_update_button import LcdnNodeToActive, LcdnNodeToMaintenance


jobs = [CheckBGPCommunities, DeployAkamaiSite, NewHpcs, LcdnNodeToMaintenance, LcdnNodeToActive]

register_jobs(*jobs)