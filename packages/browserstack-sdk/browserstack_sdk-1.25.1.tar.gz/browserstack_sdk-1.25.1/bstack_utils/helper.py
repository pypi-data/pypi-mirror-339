# coding: UTF-8
import sys
bstack11l1ll1_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1ll1l1_opy_ (bstack1l1ll1_opy_):
    global bstack1l111ll_opy_
    bstack1lll1ll_opy_ = ord (bstack1l1ll1_opy_ [-1])
    bstack111llll_opy_ = bstack1l1ll1_opy_ [:-1]
    bstack1l1l11l_opy_ = bstack1lll1ll_opy_ % len (bstack111llll_opy_)
    bstack1l1l1l_opy_ = bstack111llll_opy_ [:bstack1l1l11l_opy_] + bstack111llll_opy_ [bstack1l1l11l_opy_:]
    if bstack11l1ll1_opy_:
        bstack11ll111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstackl_opy_ + bstack1lll1ll_opy_) % bstack1l11111_opy_) for bstackl_opy_, char in enumerate (bstack1l1l1l_opy_)])
    else:
        bstack11ll111_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstackl_opy_ + bstack1lll1ll_opy_) % bstack1l11111_opy_) for bstackl_opy_, char in enumerate (bstack1l1l1l_opy_)])
    return eval (bstack11ll111_opy_)
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11ll1l1l1ll_opy_, bstack1l1l11l1_opy_, bstack1lllll1l1_opy_, bstack1l1ll1lll_opy_,
                                    bstack11ll1llll11_opy_, bstack11ll1ll1l1l_opy_, bstack11ll1ll1ll1_opy_, bstack11ll1lll1ll_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1ll11l11l_opy_, bstack11lll111ll_opy_
from bstack_utils.proxy import bstack111ll1l1_opy_, bstack11ll11l1_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l1ll1111l_opy_
from browserstack_sdk._version import __version__
bstack11ll11ll_opy_ = Config.bstack1l11l1l1ll_opy_()
logger = bstack1l1ll1111l_opy_.get_logger(__name__, bstack1l1ll1111l_opy_.bstack1lll1l11lll_opy_())
def bstack11lllll11l1_opy_(config):
    return config[bstack1ll1l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᦞ")]
def bstack11lllll1l1l_opy_(config):
    return config[bstack1ll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᦟ")]
def bstack1l1l1l1111_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1l1lll1l_opy_(obj):
    values = []
    bstack11l1l111ll1_opy_ = re.compile(bstack1ll1l1_opy_ (u"ࡳࠤࡡࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࡝ࡦ࠮ࠨࠧᦠ"), re.I)
    for key in obj.keys():
        if bstack11l1l111ll1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11ll111l11l_opy_(config):
    tags = []
    tags.extend(bstack11l1l1lll1l_opy_(os.environ))
    tags.extend(bstack11l1l1lll1l_opy_(config))
    return tags
def bstack11l1l111111_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1llllll1_opy_(bstack11l1l1l1lll_opy_):
    if not bstack11l1l1l1lll_opy_:
        return bstack1ll1l1_opy_ (u"ࠩࠪᦡ")
    return bstack1ll1l1_opy_ (u"ࠥࡿࢂࠦࠨࡼࡿࠬࠦᦢ").format(bstack11l1l1l1lll_opy_.name, bstack11l1l1l1lll_opy_.email)
def bstack11llll11ll1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1lll1111_opy_ = repo.common_dir
        info = {
            bstack1ll1l1_opy_ (u"ࠦࡸ࡮ࡡࠣᦣ"): repo.head.commit.hexsha,
            bstack1ll1l1_opy_ (u"ࠧࡹࡨࡰࡴࡷࡣࡸ࡮ࡡࠣᦤ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1ll1l1_opy_ (u"ࠨࡢࡳࡣࡱࡧ࡭ࠨᦥ"): repo.active_branch.name,
            bstack1ll1l1_opy_ (u"ࠢࡵࡣࡪࠦᦦ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1ll1l1_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࠦᦧ"): bstack11l1llllll1_opy_(repo.head.commit.committer),
            bstack1ll1l1_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࡤࡪࡡࡵࡧࠥᦨ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1ll1l1_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࠥᦩ"): bstack11l1llllll1_opy_(repo.head.commit.author),
            bstack1ll1l1_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡣࡩࡧࡴࡦࠤᦪ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1ll1l1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨᦫ"): repo.head.commit.message,
            bstack1ll1l1_opy_ (u"ࠨࡲࡰࡱࡷࠦ᦬"): repo.git.rev_parse(bstack1ll1l1_opy_ (u"ࠢ࠮࠯ࡶ࡬ࡴࡽ࠭ࡵࡱࡳࡰࡪࡼࡥ࡭ࠤ᦭")),
            bstack1ll1l1_opy_ (u"ࠣࡥࡲࡱࡲࡵ࡮ࡠࡩ࡬ࡸࡤࡪࡩࡳࠤ᦮"): bstack11l1lll1111_opy_,
            bstack1ll1l1_opy_ (u"ࠤࡺࡳࡷࡱࡴࡳࡧࡨࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧ᦯"): subprocess.check_output([bstack1ll1l1_opy_ (u"ࠥ࡫࡮ࡺࠢᦰ"), bstack1ll1l1_opy_ (u"ࠦࡷ࡫ࡶ࠮ࡲࡤࡶࡸ࡫ࠢᦱ"), bstack1ll1l1_opy_ (u"ࠧ࠳࠭ࡨ࡫ࡷ࠱ࡨࡵ࡭࡮ࡱࡱ࠱ࡩ࡯ࡲࠣᦲ")]).strip().decode(
                bstack1ll1l1_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᦳ")),
            bstack1ll1l1_opy_ (u"ࠢ࡭ࡣࡶࡸࡤࡺࡡࡨࠤᦴ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1ll1l1_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡴࡡࡶ࡭ࡳࡩࡥࡠ࡮ࡤࡷࡹࡥࡴࡢࡩࠥᦵ"): repo.git.rev_list(
                bstack1ll1l1_opy_ (u"ࠤࡾࢁ࠳࠴ࡻࡾࠤᦶ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11ll11ll1l1_opy_ = []
        for remote in remotes:
            bstack11ll111l111_opy_ = {
                bstack1ll1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᦷ"): remote.name,
                bstack1ll1l1_opy_ (u"ࠦࡺࡸ࡬ࠣᦸ"): remote.url,
            }
            bstack11ll11ll1l1_opy_.append(bstack11ll111l111_opy_)
        bstack11ll1111lll_opy_ = {
            bstack1ll1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᦹ"): bstack1ll1l1_opy_ (u"ࠨࡧࡪࡶࠥᦺ"),
            **info,
            bstack1ll1l1_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫ࡳࠣᦻ"): bstack11ll11ll1l1_opy_
        }
        bstack11ll1111lll_opy_ = bstack11l1lll11l1_opy_(bstack11ll1111lll_opy_)
        return bstack11ll1111lll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1ll1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡱࡳࡹࡱࡧࡴࡪࡰࡪࠤࡌ࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᦼ").format(err))
        return {}
def bstack11l1lll11l1_opy_(bstack11ll1111lll_opy_):
    bstack11l1lll1lll_opy_ = bstack11ll111ll11_opy_(bstack11ll1111lll_opy_)
    if bstack11l1lll1lll_opy_ and bstack11l1lll1lll_opy_ > bstack11ll1llll11_opy_:
        bstack11l1l11llll_opy_ = bstack11l1lll1lll_opy_ - bstack11ll1llll11_opy_
        bstack11l1l11lll1_opy_ = bstack11ll11l1lll_opy_(bstack11ll1111lll_opy_[bstack1ll1l1_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᦽ")], bstack11l1l11llll_opy_)
        bstack11ll1111lll_opy_[bstack1ll1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦᦾ")] = bstack11l1l11lll1_opy_
        logger.info(bstack1ll1l1_opy_ (u"࡙ࠦ࡮ࡥࠡࡥࡲࡱࡲ࡯ࡴࠡࡪࡤࡷࠥࡨࡥࡦࡰࠣࡸࡷࡻ࡮ࡤࡣࡷࡩࡩ࠴ࠠࡔ࡫ࡽࡩࠥࡵࡦࠡࡥࡲࡱࡲ࡯ࡴࠡࡣࡩࡸࡪࡸࠠࡵࡴࡸࡲࡨࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡼࡿࠣࡏࡇࠨᦿ")
                    .format(bstack11ll111ll11_opy_(bstack11ll1111lll_opy_) / 1024))
    return bstack11ll1111lll_opy_
def bstack11ll111ll11_opy_(bstack11ll11lll1_opy_):
    try:
        if bstack11ll11lll1_opy_:
            bstack11ll11l11ll_opy_ = json.dumps(bstack11ll11lll1_opy_)
            bstack11ll11l11l1_opy_ = sys.getsizeof(bstack11ll11l11ll_opy_)
            return bstack11ll11l11l1_opy_
    except Exception as e:
        logger.debug(bstack1ll1l1_opy_ (u"࡙ࠧ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤࡨࡧ࡬ࡤࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡶ࡭ࡿ࡫ࠠࡰࡨࠣࡎࡘࡕࡎࠡࡱࡥ࡮ࡪࡩࡴ࠻ࠢࡾࢁࠧᧀ").format(e))
    return -1
def bstack11ll11l1lll_opy_(field, bstack11l1ll1lll1_opy_):
    try:
        bstack11l1l1l111l_opy_ = len(bytes(bstack11ll1ll1l1l_opy_, bstack1ll1l1_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᧁ")))
        bstack11ll11111l1_opy_ = bytes(field, bstack1ll1l1_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᧂ"))
        bstack11l1lll111l_opy_ = len(bstack11ll11111l1_opy_)
        bstack11l1ll1l1ll_opy_ = ceil(bstack11l1lll111l_opy_ - bstack11l1ll1lll1_opy_ - bstack11l1l1l111l_opy_)
        if bstack11l1ll1l1ll_opy_ > 0:
            bstack11l1l11l111_opy_ = bstack11ll11111l1_opy_[:bstack11l1ll1l1ll_opy_].decode(bstack1ll1l1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᧃ"), errors=bstack1ll1l1_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࠩᧄ")) + bstack11ll1ll1l1l_opy_
            return bstack11l1l11l111_opy_
    except Exception as e:
        logger.debug(bstack1ll1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡶࡵࡹࡳࡩࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩࡦ࡮ࡧ࠰ࠥࡴ࡯ࡵࡪ࡬ࡲ࡬ࠦࡷࡢࡵࠣࡸࡷࡻ࡮ࡤࡣࡷࡩࡩࠦࡨࡦࡴࡨ࠾ࠥࢁࡽࠣᧅ").format(e))
    return field
def bstack1ll111l11_opy_():
    env = os.environ
    if (bstack1ll1l1_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤᧆ") in env and len(env[bstack1ll1l1_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥᧇ")]) > 0) or (
            bstack1ll1l1_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧᧈ") in env and len(env[bstack1ll1l1_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨᧉ")]) > 0):
        return {
            bstack1ll1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨ᧊"): bstack1ll1l1_opy_ (u"ࠤࡍࡩࡳࡱࡩ࡯ࡵࠥ᧋"),
            bstack1ll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᧌"): env.get(bstack1ll1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ᧍")),
            bstack1ll1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᧎"): env.get(bstack1ll1l1_opy_ (u"ࠨࡊࡐࡄࡢࡒࡆࡓࡅࠣ᧏")),
            bstack1ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᧐"): env.get(bstack1ll1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ᧑"))
        }
    if env.get(bstack1ll1l1_opy_ (u"ࠤࡆࡍࠧ᧒")) == bstack1ll1l1_opy_ (u"ࠥࡸࡷࡻࡥࠣ᧓") and bstack11l11l1ll_opy_(env.get(bstack1ll1l1_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡇࡎࠨ᧔"))):
        return {
            bstack1ll1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᧕"): bstack1ll1l1_opy_ (u"ࠨࡃࡪࡴࡦࡰࡪࡉࡉࠣ᧖"),
            bstack1ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᧗"): env.get(bstack1ll1l1_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ᧘")),
            bstack1ll1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᧙"): env.get(bstack1ll1l1_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡎࡔࡈࠢ᧚")),
            bstack1ll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᧛"): env.get(bstack1ll1l1_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠣ᧜"))
        }
    if env.get(bstack1ll1l1_opy_ (u"ࠨࡃࡊࠤ᧝")) == bstack1ll1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧ᧞") and bstack11l11l1ll_opy_(env.get(bstack1ll1l1_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࠣ᧟"))):
        return {
            bstack1ll1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᧠"): bstack1ll1l1_opy_ (u"ࠥࡘࡷࡧࡶࡪࡵࠣࡇࡎࠨ᧡"),
            bstack1ll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᧢"): env.get(bstack1ll1l1_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣ࡜ࡋࡂࡠࡗࡕࡐࠧ᧣")),
            bstack1ll1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᧤"): env.get(bstack1ll1l1_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᧥")),
            bstack1ll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᧦"): env.get(bstack1ll1l1_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ᧧"))
        }
    if env.get(bstack1ll1l1_opy_ (u"ࠥࡇࡎࠨ᧨")) == bstack1ll1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤ᧩") and env.get(bstack1ll1l1_opy_ (u"ࠧࡉࡉࡠࡐࡄࡑࡊࠨ᧪")) == bstack1ll1l1_opy_ (u"ࠨࡣࡰࡦࡨࡷ࡭࡯ࡰࠣ᧫"):
        return {
            bstack1ll1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᧬"): bstack1ll1l1_opy_ (u"ࠣࡅࡲࡨࡪࡹࡨࡪࡲࠥ᧭"),
            bstack1ll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᧮"): None,
            bstack1ll1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᧯"): None,
            bstack1ll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᧰"): None
        }
    if env.get(bstack1ll1l1_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡕࡅࡓࡉࡈࠣ᧱")) and env.get(bstack1ll1l1_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡆࡓࡒࡓࡉࡕࠤ᧲")):
        return {
            bstack1ll1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᧳"): bstack1ll1l1_opy_ (u"ࠣࡄ࡬ࡸࡧࡻࡣ࡬ࡧࡷࠦ᧴"),
            bstack1ll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᧵"): env.get(bstack1ll1l1_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡇࡊࡖࡢࡌ࡙࡚ࡐࡠࡑࡕࡍࡌࡏࡎࠣ᧶")),
            bstack1ll1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᧷"): None,
            bstack1ll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᧸"): env.get(bstack1ll1l1_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ᧹"))
        }
    if env.get(bstack1ll1l1_opy_ (u"ࠢࡄࡋࠥ᧺")) == bstack1ll1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨ᧻") and bstack11l11l1ll_opy_(env.get(bstack1ll1l1_opy_ (u"ࠤࡇࡖࡔࡔࡅࠣ᧼"))):
        return {
            bstack1ll1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣ᧽"): bstack1ll1l1_opy_ (u"ࠦࡉࡸ࡯࡯ࡧࠥ᧾"),
            bstack1ll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᧿"): env.get(bstack1ll1l1_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡑࡏࡎࡌࠤᨀ")),
            bstack1ll1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᨁ"): None,
            bstack1ll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᨂ"): env.get(bstack1ll1l1_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᨃ"))
        }
    if env.get(bstack1ll1l1_opy_ (u"ࠥࡇࡎࠨᨄ")) == bstack1ll1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤᨅ") and bstack11l11l1ll_opy_(env.get(bstack1ll1l1_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࠣᨆ"))):
        return {
            bstack1ll1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᨇ"): bstack1ll1l1_opy_ (u"ࠢࡔࡧࡰࡥࡵ࡮࡯ࡳࡧࠥᨈ"),
            bstack1ll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᨉ"): env.get(bstack1ll1l1_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡕࡒࡈࡃࡑࡍ࡟ࡇࡔࡊࡑࡑࡣ࡚ࡘࡌࠣᨊ")),
            bstack1ll1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᨋ"): env.get(bstack1ll1l1_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᨌ")),
            bstack1ll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᨍ"): env.get(bstack1ll1l1_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠤᨎ"))
        }
    if env.get(bstack1ll1l1_opy_ (u"ࠢࡄࡋࠥᨏ")) == bstack1ll1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨᨐ") and bstack11l11l1ll_opy_(env.get(bstack1ll1l1_opy_ (u"ࠤࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠧᨑ"))):
        return {
            bstack1ll1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᨒ"): bstack1ll1l1_opy_ (u"ࠦࡌ࡯ࡴࡍࡣࡥࠦᨓ"),
            bstack1ll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᨔ"): env.get(bstack1ll1l1_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡕࡓࡎࠥᨕ")),
            bstack1ll1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᨖ"): env.get(bstack1ll1l1_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᨗ")),
            bstack1ll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲᨘࠣ"): env.get(bstack1ll1l1_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡍࡉࠨᨙ"))
        }
    if env.get(bstack1ll1l1_opy_ (u"ࠦࡈࡏࠢᨚ")) == bstack1ll1l1_opy_ (u"ࠧࡺࡲࡶࡧࠥᨛ") and bstack11l11l1ll_opy_(env.get(bstack1ll1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࠤ᨜"))):
        return {
            bstack1ll1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᨝"): bstack1ll1l1_opy_ (u"ࠣࡄࡸ࡭ࡱࡪ࡫ࡪࡶࡨࠦ᨞"),
            bstack1ll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᨟"): env.get(bstack1ll1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᨠ")),
            bstack1ll1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᨡ"): env.get(bstack1ll1l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡎࡄࡆࡊࡒࠢᨢ")) or env.get(bstack1ll1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤᨣ")),
            bstack1ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᨤ"): env.get(bstack1ll1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᨥ"))
        }
    if bstack11l11l1ll_opy_(env.get(bstack1ll1l1_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᨦ"))):
        return {
            bstack1ll1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᨧ"): bstack1ll1l1_opy_ (u"࡛ࠦ࡯ࡳࡶࡣ࡯ࠤࡘࡺࡵࡥ࡫ࡲࠤ࡙࡫ࡡ࡮ࠢࡖࡩࡷࡼࡩࡤࡧࡶࠦᨨ"),
            bstack1ll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᨩ"): bstack1ll1l1_opy_ (u"ࠨࡻࡾࡽࢀࠦᨪ").format(env.get(bstack1ll1l1_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᨫ")), env.get(bstack1ll1l1_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙ࡏࡄࠨᨬ"))),
            bstack1ll1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᨭ"): env.get(bstack1ll1l1_opy_ (u"ࠥࡗ࡞࡙ࡔࡆࡏࡢࡈࡊࡌࡉࡏࡋࡗࡍࡔࡔࡉࡅࠤᨮ")),
            bstack1ll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᨯ"): env.get(bstack1ll1l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᨰ"))
        }
    if bstack11l11l1ll_opy_(env.get(bstack1ll1l1_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࠣᨱ"))):
        return {
            bstack1ll1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᨲ"): bstack1ll1l1_opy_ (u"ࠣࡃࡳࡴࡻ࡫ࡹࡰࡴࠥᨳ"),
            bstack1ll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᨴ"): bstack1ll1l1_opy_ (u"ࠥࡿࢂ࠵ࡰࡳࡱ࡭ࡩࡨࡺ࠯ࡼࡿ࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠤᨵ").format(env.get(bstack1ll1l1_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡕࡓࡎࠪᨶ")), env.get(bstack1ll1l1_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡂࡅࡆࡓ࡚ࡔࡔࡠࡐࡄࡑࡊ࠭ᨷ")), env.get(bstack1ll1l1_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡒࡕࡓࡏࡋࡃࡕࡡࡖࡐ࡚ࡍࠧᨸ")), env.get(bstack1ll1l1_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫᨹ"))),
            bstack1ll1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᨺ"): env.get(bstack1ll1l1_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᨻ")),
            bstack1ll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᨼ"): env.get(bstack1ll1l1_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᨽ"))
        }
    if env.get(bstack1ll1l1_opy_ (u"ࠧࡇ࡚ࡖࡔࡈࡣࡍ࡚ࡔࡑࡡࡘࡗࡊࡘ࡟ࡂࡉࡈࡒ࡙ࠨᨾ")) and env.get(bstack1ll1l1_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣᨿ")):
        return {
            bstack1ll1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᩀ"): bstack1ll1l1_opy_ (u"ࠣࡃࡽࡹࡷ࡫ࠠࡄࡋࠥᩁ"),
            bstack1ll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᩂ"): bstack1ll1l1_opy_ (u"ࠥࡿࢂࢁࡽ࠰ࡡࡥࡹ࡮ࡲࡤ࠰ࡴࡨࡷࡺࡲࡴࡴࡁࡥࡹ࡮ࡲࡤࡊࡦࡀࡿࢂࠨᩃ").format(env.get(bstack1ll1l1_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧᩄ")), env.get(bstack1ll1l1_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࠪᩅ")), env.get(bstack1ll1l1_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉ࠭ᩆ"))),
            bstack1ll1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᩇ"): env.get(bstack1ll1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᩈ")),
            bstack1ll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᩉ"): env.get(bstack1ll1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᩊ"))
        }
    if any([env.get(bstack1ll1l1_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᩋ")), env.get(bstack1ll1l1_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡔࡈࡗࡔࡒࡖࡆࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦᩌ")), env.get(bstack1ll1l1_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᩍ"))]):
        return {
            bstack1ll1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᩎ"): bstack1ll1l1_opy_ (u"ࠣࡃ࡚ࡗࠥࡉ࡯ࡥࡧࡅࡹ࡮ࡲࡤࠣᩏ"),
            bstack1ll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᩐ"): env.get(bstack1ll1l1_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡐࡖࡄࡏࡍࡈࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᩑ")),
            bstack1ll1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᩒ"): env.get(bstack1ll1l1_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᩓ")),
            bstack1ll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᩔ"): env.get(bstack1ll1l1_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᩕ"))
        }
    if env.get(bstack1ll1l1_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨᩖ")):
        return {
            bstack1ll1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᩗ"): bstack1ll1l1_opy_ (u"ࠥࡆࡦࡳࡢࡰࡱࠥᩘ"),
            bstack1ll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᩙ"): env.get(bstack1ll1l1_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡖࡪࡹࡵ࡭ࡶࡶ࡙ࡷࡲࠢᩚ")),
            bstack1ll1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᩛ"): env.get(bstack1ll1l1_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡴࡪࡲࡶࡹࡐ࡯ࡣࡐࡤࡱࡪࠨᩜ")),
            bstack1ll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᩝ"): env.get(bstack1ll1l1_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢᩞ"))
        }
    if env.get(bstack1ll1l1_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࠦ᩟")) or env.get(bstack1ll1l1_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨ᩠")):
        return {
            bstack1ll1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᩡ"): bstack1ll1l1_opy_ (u"ࠨࡗࡦࡴࡦ࡯ࡪࡸࠢᩢ"),
            bstack1ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᩣ"): env.get(bstack1ll1l1_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᩤ")),
            bstack1ll1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᩥ"): bstack1ll1l1_opy_ (u"ࠥࡑࡦ࡯࡮ࠡࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠥᩦ") if env.get(bstack1ll1l1_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨᩧ")) else None,
            bstack1ll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᩨ"): env.get(bstack1ll1l1_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡈࡋࡗࡣࡈࡕࡍࡎࡋࡗࠦᩩ"))
        }
    if any([env.get(bstack1ll1l1_opy_ (u"ࠢࡈࡅࡓࡣࡕࡘࡏࡋࡇࡆࡘࠧᩪ")), env.get(bstack1ll1l1_opy_ (u"ࠣࡉࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤᩫ")), env.get(bstack1ll1l1_opy_ (u"ࠤࡊࡓࡔࡍࡌࡆࡡࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤᩬ"))]):
        return {
            bstack1ll1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᩭ"): bstack1ll1l1_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡈࡲ࡯ࡶࡦࠥᩮ"),
            bstack1ll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᩯ"): None,
            bstack1ll1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᩰ"): env.get(bstack1ll1l1_opy_ (u"ࠢࡑࡔࡒࡎࡊࡉࡔࡠࡋࡇࠦᩱ")),
            bstack1ll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᩲ"): env.get(bstack1ll1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᩳ"))
        }
    if env.get(bstack1ll1l1_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࠨᩴ")):
        return {
            bstack1ll1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᩵"): bstack1ll1l1_opy_ (u"࡙ࠧࡨࡪࡲࡳࡥࡧࡲࡥࠣ᩶"),
            bstack1ll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᩷"): env.get(bstack1ll1l1_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᩸")),
            bstack1ll1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᩹"): bstack1ll1l1_opy_ (u"ࠤࡍࡳࡧࠦࠣࡼࡿࠥ᩺").format(env.get(bstack1ll1l1_opy_ (u"ࠪࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉ࠭᩻"))) if env.get(bstack1ll1l1_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠢ᩼")) else None,
            bstack1ll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᩽"): env.get(bstack1ll1l1_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ᩾"))
        }
    if bstack11l11l1ll_opy_(env.get(bstack1ll1l1_opy_ (u"ࠢࡏࡇࡗࡐࡎࡌ࡙᩿ࠣ"))):
        return {
            bstack1ll1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪀"): bstack1ll1l1_opy_ (u"ࠤࡑࡩࡹࡲࡩࡧࡻࠥ᪁"),
            bstack1ll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᪂"): env.get(bstack1ll1l1_opy_ (u"ࠦࡉࡋࡐࡍࡑ࡜ࡣ࡚ࡘࡌࠣ᪃")),
            bstack1ll1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᪄"): env.get(bstack1ll1l1_opy_ (u"ࠨࡓࡊࡖࡈࡣࡓࡇࡍࡆࠤ᪅")),
            bstack1ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪆"): env.get(bstack1ll1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ᪇"))
        }
    if bstack11l11l1ll_opy_(env.get(bstack1ll1l1_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡄࡇ࡙ࡏࡏࡏࡕࠥ᪈"))):
        return {
            bstack1ll1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣ᪉"): bstack1ll1l1_opy_ (u"ࠦࡌ࡯ࡴࡉࡷࡥࠤࡆࡩࡴࡪࡱࡱࡷࠧ᪊"),
            bstack1ll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᪋"): bstack1ll1l1_opy_ (u"ࠨࡻࡾ࠱ࡾࢁ࠴ࡧࡣࡵ࡫ࡲࡲࡸ࠵ࡲࡶࡰࡶ࠳ࢀࢃࠢ᪌").format(env.get(bstack1ll1l1_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡖࡔࡏࠫ᪍")), env.get(bstack1ll1l1_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡈࡔࡔ࡙ࡉࡕࡑࡕ࡝ࠬ᪎")), env.get(bstack1ll1l1_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠩ᪏"))),
            bstack1ll1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᪐"): env.get(bstack1ll1l1_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣ࡜ࡕࡒࡌࡈࡏࡓ࡜ࠨ᪑")),
            bstack1ll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᪒"): env.get(bstack1ll1l1_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉࠨ᪓"))
        }
    if env.get(bstack1ll1l1_opy_ (u"ࠢࡄࡋࠥ᪔")) == bstack1ll1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨ᪕") and env.get(bstack1ll1l1_opy_ (u"ࠤ࡙ࡉࡗࡉࡅࡍࠤ᪖")) == bstack1ll1l1_opy_ (u"ࠥ࠵ࠧ᪗"):
        return {
            bstack1ll1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᪘"): bstack1ll1l1_opy_ (u"ࠧ࡜ࡥࡳࡥࡨࡰࠧ᪙"),
            bstack1ll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᪚"): bstack1ll1l1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࡼࡿࠥ᪛").format(env.get(bstack1ll1l1_opy_ (u"ࠨࡘࡈࡖࡈࡋࡌࡠࡗࡕࡐࠬ᪜"))),
            bstack1ll1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᪝"): None,
            bstack1ll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᪞"): None,
        }
    if env.get(bstack1ll1l1_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡖࡆࡔࡖࡍࡔࡔࠢ᪟")):
        return {
            bstack1ll1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᪠"): bstack1ll1l1_opy_ (u"ࠨࡔࡦࡣࡰࡧ࡮ࡺࡹࠣ᪡"),
            bstack1ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᪢"): None,
            bstack1ll1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᪣"): env.get(bstack1ll1l1_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣࡕࡘࡏࡋࡇࡆࡘࡤࡔࡁࡎࡇࠥ᪤")),
            bstack1ll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᪥"): env.get(bstack1ll1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᪦"))
        }
    if any([env.get(bstack1ll1l1_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࠣᪧ")), env.get(bstack1ll1l1_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡖࡑࠨ᪨")), env.get(bstack1ll1l1_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧ᪩")), env.get(bstack1ll1l1_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡙ࡋࡁࡎࠤ᪪"))]):
        return {
            bstack1ll1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᪫"): bstack1ll1l1_opy_ (u"ࠥࡇࡴࡴࡣࡰࡷࡵࡷࡪࠨ᪬"),
            bstack1ll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᪭"): None,
            bstack1ll1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᪮"): env.get(bstack1ll1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ᪯")) or None,
            bstack1ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪰"): env.get(bstack1ll1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ᪱"), 0)
        }
    if env.get(bstack1ll1l1_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ᪲")):
        return {
            bstack1ll1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣ᪳"): bstack1ll1l1_opy_ (u"ࠦࡌࡵࡃࡅࠤ᪴"),
            bstack1ll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬᪵ࠣ"): None,
            bstack1ll1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥ᪶ࠣ"): env.get(bstack1ll1l1_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉ᪷ࠧ")),
            bstack1ll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸ᪸ࠢ"): env.get(bstack1ll1l1_opy_ (u"ࠤࡊࡓࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡄࡑࡘࡒ࡙ࡋࡒ᪹ࠣ"))
        }
    if env.get(bstack1ll1l1_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄ᪺ࠣ")):
        return {
            bstack1ll1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᪻"): bstack1ll1l1_opy_ (u"ࠧࡉ࡯ࡥࡧࡉࡶࡪࡹࡨࠣ᪼"),
            bstack1ll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᪽"): env.get(bstack1ll1l1_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᪾")),
            bstack1ll1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧᪿࠥ"): env.get(bstack1ll1l1_opy_ (u"ࠤࡆࡊࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉᫀࠧ")),
            bstack1ll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᫁"): env.get(bstack1ll1l1_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤ᫂"))
        }
    return {bstack1ll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵ᫃ࠦ"): None}
def get_host_info():
    return {
        bstack1ll1l1_opy_ (u"ࠨࡨࡰࡵࡷࡲࡦࡳࡥ᫄ࠣ"): platform.node(),
        bstack1ll1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤ᫅"): platform.system(),
        bstack1ll1l1_opy_ (u"ࠣࡶࡼࡴࡪࠨ᫆"): platform.machine(),
        bstack1ll1l1_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥ᫇"): platform.version(),
        bstack1ll1l1_opy_ (u"ࠥࡥࡷࡩࡨࠣ᫈"): platform.architecture()[0]
    }
def bstack11llllll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l1l11l11l_opy_():
    if bstack11ll11ll_opy_.get_property(bstack1ll1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ᫉")):
        return bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮᫊ࠫ")
    return bstack1ll1l1_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠬ᫋")
def bstack11l1ll1111l_opy_(driver):
    info = {
        bstack1ll1l1_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᫌ"): driver.capabilities,
        bstack1ll1l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬᫍ"): driver.session_id,
        bstack1ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪᫎ"): driver.capabilities.get(bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ᫏"), None),
        bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭᫐"): driver.capabilities.get(bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᫑"), None),
        bstack1ll1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᫒"): driver.capabilities.get(bstack1ll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭᫓"), None),
        bstack1ll1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ᫔"):driver.capabilities.get(bstack1ll1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ᫕"), None),
    }
    if bstack11l1l11l11l_opy_() == bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ᫖"):
        if bstack11l11111l_opy_():
            info[bstack1ll1l1_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬ᫗")] = bstack1ll1l1_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ᫘")
        elif driver.capabilities.get(bstack1ll1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᫙"), {}).get(bstack1ll1l1_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ᫚"), False):
            info[bstack1ll1l1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ᫛")] = bstack1ll1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭᫜")
        else:
            info[bstack1ll1l1_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ᫝")] = bstack1ll1l1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᫞")
    return info
def bstack11l11111l_opy_():
    if bstack11ll11ll_opy_.get_property(bstack1ll1l1_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ᫟")):
        return True
    if bstack11l11l1ll_opy_(os.environ.get(bstack1ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ᫠"), None)):
        return True
    return False
def bstack11l1lll1ll_opy_(bstack11ll111ll1l_opy_, url, data, config):
    headers = config.get(bstack1ll1l1_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ᫡"), None)
    proxies = bstack111ll1l1_opy_(config, url)
    auth = config.get(bstack1ll1l1_opy_ (u"ࠨࡣࡸࡸ࡭࠭᫢"), None)
    response = requests.request(
            bstack11ll111ll1l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1ll1l1_opy_(bstack1ll1l11ll_opy_, size):
    bstack1l11l11111_opy_ = []
    while len(bstack1ll1l11ll_opy_) > size:
        bstack11ll1111l_opy_ = bstack1ll1l11ll_opy_[:size]
        bstack1l11l11111_opy_.append(bstack11ll1111l_opy_)
        bstack1ll1l11ll_opy_ = bstack1ll1l11ll_opy_[size:]
    bstack1l11l11111_opy_.append(bstack1ll1l11ll_opy_)
    return bstack1l11l11111_opy_
def bstack11ll11lllll_opy_(message, bstack11l1lll1ll1_opy_=False):
    os.write(1, bytes(message, bstack1ll1l1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ᫣")))
    os.write(1, bytes(bstack1ll1l1_opy_ (u"ࠪࡠࡳ࠭᫤"), bstack1ll1l1_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᫥")))
    if bstack11l1lll1ll1_opy_:
        with open(bstack1ll1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡵ࠱࠲ࡻ࠰ࠫ᫦") + os.environ[bstack1ll1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬ᫧")] + bstack1ll1l1_opy_ (u"ࠧ࠯࡮ࡲ࡫ࠬ᫨"), bstack1ll1l1_opy_ (u"ࠨࡣࠪ᫩")) as f:
            f.write(message + bstack1ll1l1_opy_ (u"ࠩ࡟ࡲࠬ᫪"))
def bstack1l1llll11ll_opy_():
    return os.environ[bstack1ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭᫫")].lower() == bstack1ll1l1_opy_ (u"ࠫࡹࡸࡵࡦࠩ᫬")
def bstack1l11ll111l_opy_(bstack11ll111l1ll_opy_):
    return bstack1ll1l1_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫ᫭").format(bstack11ll1l1l1ll_opy_, bstack11ll111l1ll_opy_)
def bstack11l1ll11ll_opy_():
    return bstack111l1l1ll1_opy_().replace(tzinfo=None).isoformat() + bstack1ll1l1_opy_ (u"࡚࠭ࠨ᫮")
def bstack11l1ll11lll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1ll1l1_opy_ (u"࡛ࠧࠩ᫯"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1ll1l1_opy_ (u"ࠨ࡜ࠪ᫰")))).total_seconds() * 1000
def bstack11l1l1l1l11_opy_(timestamp):
    return bstack11l1l1l1ll1_opy_(timestamp).isoformat() + bstack1ll1l1_opy_ (u"ࠩ࡝ࠫ᫱")
def bstack11l1l1ll111_opy_(bstack11l1ll1ll1l_opy_):
    date_format = bstack1ll1l1_opy_ (u"ࠪࠩ࡞ࠫ࡭ࠦࡦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠨ᫲")
    bstack11l11llllll_opy_ = datetime.datetime.strptime(bstack11l1ll1ll1l_opy_, date_format)
    return bstack11l11llllll_opy_.isoformat() + bstack1ll1l1_opy_ (u"ࠫ࡟࠭᫳")
def bstack11l1llll1ll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1ll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᫴")
    else:
        return bstack1ll1l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᫵")
def bstack11l11l1ll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1ll1l1_opy_ (u"ࠧࡵࡴࡸࡩࠬ᫶")
def bstack11l1ll111l1_opy_(val):
    return val.__str__().lower() == bstack1ll1l1_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ᫷")
def bstack111ll11ll1_opy_(bstack11l1l1llll1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1l1llll1_opy_ as e:
                print(bstack1ll1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤ᫸").format(func.__name__, bstack11l1l1llll1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1ll1l1l1_opy_(bstack11ll11l1111_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11ll11l1111_opy_(cls, *args, **kwargs)
            except bstack11l1l1llll1_opy_ as e:
                print(bstack1ll1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥ᫹").format(bstack11ll11l1111_opy_.__name__, bstack11l1l1llll1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1ll1l1l1_opy_
    else:
        return decorator
def bstack11l11ll1l1_opy_(bstack1111llll1l_opy_):
    if os.getenv(bstack1ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ᫺")) is not None:
        return bstack11l11l1ll_opy_(os.getenv(bstack1ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ᫻")))
    if bstack1ll1l1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᫼") in bstack1111llll1l_opy_ and bstack11l1ll111l1_opy_(bstack1111llll1l_opy_[bstack1ll1l1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᫽")]):
        return False
    if bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᫾") in bstack1111llll1l_opy_ and bstack11l1ll111l1_opy_(bstack1111llll1l_opy_[bstack1ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᫿")]):
        return False
    return True
def bstack111111111_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l1l1l1111_opy_ = os.environ.get(bstack1ll1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠥᬀ"), None)
        return bstack11l1l1l1111_opy_ is None or bstack11l1l1l1111_opy_ == bstack1ll1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᬁ")
    except Exception as e:
        return False
def bstack1llllll1ll_opy_(hub_url, CONFIG):
    if bstack11ll1llll1_opy_() <= version.parse(bstack1ll1l1_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬᬂ")):
        if hub_url:
            return bstack1ll1l1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᬃ") + hub_url + bstack1ll1l1_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦᬄ")
        return bstack1lllll1l1_opy_
    if hub_url:
        return bstack1ll1l1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᬅ") + hub_url + bstack1ll1l1_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥᬆ")
    return bstack1l1ll1lll_opy_
def bstack11ll11l1l11_opy_():
    return isinstance(os.getenv(bstack1ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩᬇ")), str)
def bstack1ll1l111_opy_(url):
    return urlparse(url).hostname
def bstack11l11l111_opy_(hostname):
    for bstack1ll11l1l11_opy_ in bstack1l1l11l1_opy_:
        regex = re.compile(bstack1ll11l1l11_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1ll111ll_opy_(bstack11ll1l11111_opy_, file_name, logger):
    bstack1l1llll1_opy_ = os.path.join(os.path.expanduser(bstack1ll1l1_opy_ (u"ࠫࢃ࠭ᬈ")), bstack11ll1l11111_opy_)
    try:
        if not os.path.exists(bstack1l1llll1_opy_):
            os.makedirs(bstack1l1llll1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1ll1l1_opy_ (u"ࠬࢄࠧᬉ")), bstack11ll1l11111_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1ll1l1_opy_ (u"࠭ࡷࠨᬊ")):
                pass
            with open(file_path, bstack1ll1l1_opy_ (u"ࠢࡸ࠭ࠥᬋ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1ll11l11l_opy_.format(str(e)))
def bstack11ll111111l_opy_(file_name, key, value, logger):
    file_path = bstack11l1ll111ll_opy_(bstack1ll1l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᬌ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1lllll11l1_opy_ = json.load(open(file_path, bstack1ll1l1_opy_ (u"ࠩࡵࡦࠬᬍ")))
        else:
            bstack1lllll11l1_opy_ = {}
        bstack1lllll11l1_opy_[key] = value
        with open(file_path, bstack1ll1l1_opy_ (u"ࠥࡻ࠰ࠨᬎ")) as outfile:
            json.dump(bstack1lllll11l1_opy_, outfile)
def bstack1l1ll1ll1l_opy_(file_name, logger):
    file_path = bstack11l1ll111ll_opy_(bstack1ll1l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᬏ"), file_name, logger)
    bstack1lllll11l1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1ll1l1_opy_ (u"ࠬࡸࠧᬐ")) as bstack11ll11llll_opy_:
            bstack1lllll11l1_opy_ = json.load(bstack11ll11llll_opy_)
    return bstack1lllll11l1_opy_
def bstack11llllll1l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1ll1l1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥ࠻ࠢࠪᬑ") + file_path + bstack1ll1l1_opy_ (u"ࠧࠡࠩᬒ") + str(e))
def bstack11ll1llll1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1ll1l1_opy_ (u"ࠣ࠾ࡑࡓ࡙࡙ࡅࡕࡀࠥᬓ")
def bstack1l11111lll_opy_(config):
    if bstack1ll1l1_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᬔ") in config:
        del (config[bstack1ll1l1_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᬕ")])
        return False
    if bstack11ll1llll1_opy_() < version.parse(bstack1ll1l1_opy_ (u"ࠫ࠸࠴࠴࠯࠲ࠪᬖ")):
        return False
    if bstack11ll1llll1_opy_() >= version.parse(bstack1ll1l1_opy_ (u"ࠬ࠺࠮࠲࠰࠸ࠫᬗ")):
        return True
    if bstack1ll1l1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᬘ") in config and config[bstack1ll1l1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᬙ")] is False:
        return False
    else:
        return True
def bstack1l1lll1ll_opy_(args_list, bstack11l1llll111_opy_):
    index = -1
    for value in bstack11l1llll111_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11l1111lll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11l1111lll_opy_ = bstack11l1111lll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1ll1l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᬚ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1ll1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᬛ"), exception=exception)
    def bstack1111ll1l11_opy_(self):
        if self.result != bstack1ll1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᬜ"):
            return None
        if isinstance(self.exception_type, str) and bstack1ll1l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᬝ") in self.exception_type:
            return bstack1ll1l1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᬞ")
        return bstack1ll1l1_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᬟ")
    def bstack11l1lll11ll_opy_(self):
        if self.result != bstack1ll1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᬠ"):
            return None
        if self.bstack11l1111lll_opy_:
            return self.bstack11l1111lll_opy_
        return bstack11ll1111l1l_opy_(self.exception)
def bstack11ll1111l1l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l1l11ll1l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11111l111_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1llll1l1l1_opy_(config, logger):
    try:
        import playwright
        bstack11l1l1111ll_opy_ = playwright.__file__
        bstack11l1lllllll_opy_ = os.path.split(bstack11l1l1111ll_opy_)
        bstack11ll11l1ll1_opy_ = bstack11l1lllllll_opy_[0] + bstack1ll1l1_opy_ (u"ࠨ࠱ࡧࡶ࡮ࡼࡥࡳ࠱ࡳࡥࡨࡱࡡࡨࡧ࠲ࡰ࡮ࡨ࠯ࡤ࡮࡬࠳ࡨࡲࡩ࠯࡬ࡶࠫᬡ")
        os.environ[bstack1ll1l1_opy_ (u"ࠩࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝ࠬᬢ")] = bstack11ll11l1_opy_(config)
        with open(bstack11ll11l1ll1_opy_, bstack1ll1l1_opy_ (u"ࠪࡶࠬᬣ")) as f:
            bstack11lllll11_opy_ = f.read()
            bstack11ll11l1l1l_opy_ = bstack1ll1l1_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪᬤ")
            bstack11l1l111l1l_opy_ = bstack11lllll11_opy_.find(bstack11ll11l1l1l_opy_)
            if bstack11l1l111l1l_opy_ == -1:
              process = subprocess.Popen(bstack1ll1l1_opy_ (u"ࠧࡴࡰ࡮ࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠤᬥ"), shell=True, cwd=bstack11l1lllllll_opy_[0])
              process.wait()
              bstack11l1llll11l_opy_ = bstack1ll1l1_opy_ (u"࠭ࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࠦࡀ࠭ᬦ")
              bstack11l1ll1l111_opy_ = bstack1ll1l1_opy_ (u"ࠢࠣࠤࠣࡠࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵ࡞ࠥ࠿ࠥࡩ࡯࡯ࡵࡷࠤࢀࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠢࢀࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧࠪ࠽ࠣ࡭࡫ࠦࠨࡱࡴࡲࡧࡪࡹࡳ࠯ࡧࡱࡺ࠳ࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠪࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴ࠭࠯࠻ࠡࠤࠥࠦᬧ")
              bstack11l1llll1l1_opy_ = bstack11lllll11_opy_.replace(bstack11l1llll11l_opy_, bstack11l1ll1l111_opy_)
              with open(bstack11ll11l1ll1_opy_, bstack1ll1l1_opy_ (u"ࠨࡹࠪᬨ")) as f:
                f.write(bstack11l1llll1l1_opy_)
    except Exception as e:
        logger.error(bstack11lll111ll_opy_.format(str(e)))
def bstack1lll1lll11_opy_():
  try:
    bstack11l1l11l1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l1_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩᬩ"))
    bstack11l1ll1llll_opy_ = []
    if os.path.exists(bstack11l1l11l1ll_opy_):
      with open(bstack11l1l11l1ll_opy_) as f:
        bstack11l1ll1llll_opy_ = json.load(f)
      os.remove(bstack11l1l11l1ll_opy_)
    return bstack11l1ll1llll_opy_
  except:
    pass
  return []
def bstack11l1l1l11l_opy_(bstack1l11l1111_opy_):
  try:
    bstack11l1ll1llll_opy_ = []
    bstack11l1l11l1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l1_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪᬪ"))
    if os.path.exists(bstack11l1l11l1ll_opy_):
      with open(bstack11l1l11l1ll_opy_) as f:
        bstack11l1ll1llll_opy_ = json.load(f)
    bstack11l1ll1llll_opy_.append(bstack1l11l1111_opy_)
    with open(bstack11l1l11l1ll_opy_, bstack1ll1l1_opy_ (u"ࠫࡼ࠭ᬫ")) as f:
        json.dump(bstack11l1ll1llll_opy_, f)
  except:
    pass
def bstack1ll1lll11_opy_(logger, bstack11l1l111lll_opy_ = False):
  try:
    test_name = os.environ.get(bstack1ll1l1_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨᬬ"), bstack1ll1l1_opy_ (u"࠭ࠧᬭ"))
    if test_name == bstack1ll1l1_opy_ (u"ࠧࠨᬮ"):
        test_name = threading.current_thread().__dict__.get(bstack1ll1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡃࡦࡧࡣࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠧᬯ"), bstack1ll1l1_opy_ (u"ࠩࠪᬰ"))
    bstack11ll1111111_opy_ = bstack1ll1l1_opy_ (u"ࠪ࠰ࠥ࠭ᬱ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l1l111lll_opy_:
        bstack1lll1l111_opy_ = os.environ.get(bstack1ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᬲ"), bstack1ll1l1_opy_ (u"ࠬ࠶ࠧᬳ"))
        bstack11l11lll11_opy_ = {bstack1ll1l1_opy_ (u"࠭࡮ࡢ࡯ࡨ᬴ࠫ"): test_name, bstack1ll1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᬵ"): bstack11ll1111111_opy_, bstack1ll1l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᬶ"): bstack1lll1l111_opy_}
        bstack11l1ll11l11_opy_ = []
        bstack11l1ll1l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨᬷ"))
        if os.path.exists(bstack11l1ll1l11l_opy_):
            with open(bstack11l1ll1l11l_opy_) as f:
                bstack11l1ll11l11_opy_ = json.load(f)
        bstack11l1ll11l11_opy_.append(bstack11l11lll11_opy_)
        with open(bstack11l1ll1l11l_opy_, bstack1ll1l1_opy_ (u"ࠪࡻࠬᬸ")) as f:
            json.dump(bstack11l1ll11l11_opy_, f)
    else:
        bstack11l11lll11_opy_ = {bstack1ll1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᬹ"): test_name, bstack1ll1l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᬺ"): bstack11ll1111111_opy_, bstack1ll1l1_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬᬻ"): str(multiprocessing.current_process().name)}
        if bstack1ll1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫᬼ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11l11lll11_opy_)
  except Exception as e:
      logger.warn(bstack1ll1l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡴࡾࡺࡥࡴࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧᬽ").format(e))
def bstack1l11l1llll_opy_(error_message, test_name, index, logger):
  try:
    bstack11ll111l1l1_opy_ = []
    bstack11l11lll11_opy_ = {bstack1ll1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᬾ"): test_name, bstack1ll1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᬿ"): error_message, bstack1ll1l1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᭀ"): index}
    bstack11l11lllll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ᭁ"))
    if os.path.exists(bstack11l11lllll1_opy_):
        with open(bstack11l11lllll1_opy_) as f:
            bstack11ll111l1l1_opy_ = json.load(f)
    bstack11ll111l1l1_opy_.append(bstack11l11lll11_opy_)
    with open(bstack11l11lllll1_opy_, bstack1ll1l1_opy_ (u"࠭ࡷࠨᭂ")) as f:
        json.dump(bstack11ll111l1l1_opy_, f)
  except Exception as e:
    logger.warn(bstack1ll1l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡵࡳࡧࡵࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥᭃ").format(e))
def bstack1l1l1l1l1_opy_(bstack1lll11l1_opy_, name, logger):
  try:
    bstack11l11lll11_opy_ = {bstack1ll1l1_opy_ (u"ࠨࡰࡤࡱࡪ᭄࠭"): name, bstack1ll1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᭅ"): bstack1lll11l1_opy_, bstack1ll1l1_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᭆ"): str(threading.current_thread()._name)}
    return bstack11l11lll11_opy_
  except Exception as e:
    logger.warn(bstack1ll1l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡢࡦࡪࡤࡺࡪࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣᭇ").format(e))
  return
def bstack11l1l1lllll_opy_():
    return platform.system() == bstack1ll1l1_opy_ (u"ࠬ࡝ࡩ࡯ࡦࡲࡻࡸ࠭ᭈ")
def bstack1lllll111l_opy_(bstack11ll11ll111_opy_, config, logger):
    bstack11ll11llll1_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11ll11ll111_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1ll1l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡱࡺࡥࡳࠢࡦࡳࡳ࡬ࡩࡨࠢ࡮ࡩࡾࡹࠠࡣࡻࠣࡶࡪ࡭ࡥࡹࠢࡰࡥࡹࡩࡨ࠻ࠢࡾࢁࠧᭉ").format(e))
    return bstack11ll11llll1_opy_
def bstack11l1l11111l_opy_(bstack11l1ll11l1l_opy_, bstack11l1ll1ll11_opy_):
    bstack11l1lll1l1l_opy_ = version.parse(bstack11l1ll11l1l_opy_)
    bstack11l1ll11ll1_opy_ = version.parse(bstack11l1ll1ll11_opy_)
    if bstack11l1lll1l1l_opy_ > bstack11l1ll11ll1_opy_:
        return 1
    elif bstack11l1lll1l1l_opy_ < bstack11l1ll11ll1_opy_:
        return -1
    else:
        return 0
def bstack111l1l1ll1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1l1l1ll1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1l1l11l1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l11llll1l_opy_(options, framework, bstack1l11lll111_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1ll1l1_opy_ (u"ࠧࡨࡧࡷࠫᭊ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l1llll1ll_opy_ = caps.get(bstack1ll1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᭋ"))
    bstack11l1lllll11_opy_ = True
    bstack111l11l1l_opy_ = os.environ[bstack1ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᭌ")]
    if bstack11l1ll111l1_opy_(caps.get(bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪ࡝࠳ࡄࠩ᭍"))) or bstack11l1ll111l1_opy_(caps.get(bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫ᭎"))):
        bstack11l1lllll11_opy_ = False
    if bstack1l11111lll_opy_({bstack1ll1l1_opy_ (u"ࠧࡻࡳࡦ࡙࠶ࡇࠧ᭏"): bstack11l1lllll11_opy_}):
        bstack1l1llll1ll_opy_ = bstack1l1llll1ll_opy_ or {}
        bstack1l1llll1ll_opy_[bstack1ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ᭐")] = bstack11l1l1l11l1_opy_(framework)
        bstack1l1llll1ll_opy_[bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᭑")] = bstack1l1llll11ll_opy_()
        bstack1l1llll1ll_opy_[bstack1ll1l1_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ᭒")] = bstack111l11l1l_opy_
        bstack1l1llll1ll_opy_[bstack1ll1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ᭓")] = bstack1l11lll111_opy_
        if getattr(options, bstack1ll1l1_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫ᭔"), None):
            options.set_capability(bstack1ll1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᭕"), bstack1l1llll1ll_opy_)
        else:
            options[bstack1ll1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᭖")] = bstack1l1llll1ll_opy_
    else:
        if getattr(options, bstack1ll1l1_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧ᭗"), None):
            options.set_capability(bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ᭘"), bstack11l1l1l11l1_opy_(framework))
            options.set_capability(bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᭙"), bstack1l1llll11ll_opy_())
            options.set_capability(bstack1ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ᭚"), bstack111l11l1l_opy_)
            options.set_capability(bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ᭛"), bstack1l11lll111_opy_)
        else:
            options[bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ᭜")] = bstack11l1l1l11l1_opy_(framework)
            options[bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭᭝")] = bstack1l1llll11ll_opy_()
            options[bstack1ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᭞")] = bstack111l11l1l_opy_
            options[bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ᭟")] = bstack1l11lll111_opy_
    return options
def bstack11l1l1ll11l_opy_(bstack11l1lll1l11_opy_, framework):
    bstack1l11lll111_opy_ = bstack11ll11ll_opy_.get_property(bstack1ll1l1_opy_ (u"ࠣࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡖࡒࡐࡆࡘࡇ࡙ࡥࡍࡂࡒࠥ᭠"))
    if bstack11l1lll1l11_opy_ and len(bstack11l1lll1l11_opy_.split(bstack1ll1l1_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ᭡"))) > 1:
        ws_url = bstack11l1lll1l11_opy_.split(bstack1ll1l1_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ᭢"))[0]
        if bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ᭣") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11ll11lll11_opy_ = json.loads(urllib.parse.unquote(bstack11l1lll1l11_opy_.split(bstack1ll1l1_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ᭤"))[1]))
            bstack11ll11lll11_opy_ = bstack11ll11lll11_opy_ or {}
            bstack111l11l1l_opy_ = os.environ[bstack1ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ᭥")]
            bstack11ll11lll11_opy_[bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ᭦")] = str(framework) + str(__version__)
            bstack11ll11lll11_opy_[bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᭧")] = bstack1l1llll11ll_opy_()
            bstack11ll11lll11_opy_[bstack1ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ᭨")] = bstack111l11l1l_opy_
            bstack11ll11lll11_opy_[bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ᭩")] = bstack1l11lll111_opy_
            bstack11l1lll1l11_opy_ = bstack11l1lll1l11_opy_.split(bstack1ll1l1_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ᭪"))[0] + bstack1ll1l1_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ᭫") + urllib.parse.quote(json.dumps(bstack11ll11lll11_opy_))
    return bstack11l1lll1l11_opy_
def bstack1ll1l1111l_opy_():
    global bstack1ll1l1l1ll_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1ll1l1l1ll_opy_ = BrowserType.connect
    return bstack1ll1l1l1ll_opy_
def bstack1lll1lll_opy_(framework_name):
    global bstack1l111l1l1l_opy_
    bstack1l111l1l1l_opy_ = framework_name
    return framework_name
def bstack1l1ll11l1l_opy_(self, *args, **kwargs):
    global bstack1ll1l1l1ll_opy_
    try:
        global bstack1l111l1l1l_opy_
        if bstack1ll1l1_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ᭬ࠪ") in kwargs:
            kwargs[bstack1ll1l1_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫ᭭")] = bstack11l1l1ll11l_opy_(
                kwargs.get(bstack1ll1l1_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬ᭮"), None),
                bstack1l111l1l1l_opy_
            )
    except Exception as e:
        logger.error(bstack1ll1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡗࡉࡑࠠࡤࡣࡳࡷ࠿ࠦࡻࡾࠤ᭯").format(str(e)))
    return bstack1ll1l1l1ll_opy_(self, *args, **kwargs)
def bstack11l1l1lll11_opy_(bstack11ll1111l11_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack111ll1l1_opy_(bstack11ll1111l11_opy_, bstack1ll1l1_opy_ (u"ࠥࠦ᭰"))
        if proxies and proxies.get(bstack1ll1l1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥ᭱")):
            parsed_url = urlparse(proxies.get(bstack1ll1l1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦ᭲")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1ll1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩ᭳")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1ll1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪ᭴")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1ll1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫ᭵")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1ll1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬ᭶")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11111l11_opy_(bstack11ll1111l11_opy_):
    bstack11l1l111l11_opy_ = {
        bstack11ll1lll1ll_opy_[bstack11l1ll11111_opy_]: bstack11ll1111l11_opy_[bstack11l1ll11111_opy_]
        for bstack11l1ll11111_opy_ in bstack11ll1111l11_opy_
        if bstack11l1ll11111_opy_ in bstack11ll1lll1ll_opy_
    }
    bstack11l1l111l11_opy_[bstack1ll1l1_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥ᭷")] = bstack11l1l1lll11_opy_(bstack11ll1111l11_opy_, bstack11ll11ll_opy_.get_property(bstack1ll1l1_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦ᭸")))
    bstack11ll11l111l_opy_ = [element.lower() for element in bstack11ll1ll1ll1_opy_]
    bstack11l1l1l11ll_opy_(bstack11l1l111l11_opy_, bstack11ll11l111l_opy_)
    return bstack11l1l111l11_opy_
def bstack11l1l1l11ll_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1ll1l1_opy_ (u"ࠧ࠰ࠪࠫࠬࠥ᭹")
    for value in d.values():
        if isinstance(value, dict):
            bstack11l1l1l11ll_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11l1l1l11ll_opy_(item, keys)
def bstack1ll1111ll11_opy_():
    bstack11ll1111ll1_opy_ = [os.environ.get(bstack1ll1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡉࡍࡇࡖࡣࡉࡏࡒࠣ᭺")), os.path.join(os.path.expanduser(bstack1ll1l1_opy_ (u"ࠢࡿࠤ᭻")), bstack1ll1l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᭼")), os.path.join(bstack1ll1l1_opy_ (u"ࠩ࠲ࡸࡲࡶࠧ᭽"), bstack1ll1l1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ᭾"))]
    for path in bstack11ll1111ll1_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1ll1l1_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࠪࠦ᭿") + str(path) + bstack1ll1l1_opy_ (u"ࠧ࠭ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠣᮀ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1ll1l1_opy_ (u"ࠨࡇࡪࡸ࡬ࡲ࡬ࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰࡶࠤ࡫ࡵࡲࠡࠩࠥᮁ") + str(path) + bstack1ll1l1_opy_ (u"ࠢࠨࠤᮂ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1ll1l1_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࠧࠣᮃ") + str(path) + bstack1ll1l1_opy_ (u"ࠤࠪࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡮ࡡࡴࠢࡷ࡬ࡪࠦࡲࡦࡳࡸ࡭ࡷ࡫ࡤࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠴ࠢᮄ"))
            else:
                logger.debug(bstack1ll1l1_opy_ (u"ࠥࡇࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧࠣࠫࠧᮅ") + str(path) + bstack1ll1l1_opy_ (u"ࠦࠬࠦࡷࡪࡶ࡫ࠤࡼࡸࡩࡵࡧࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴ࠮ࠣᮆ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1ll1l1_opy_ (u"ࠧࡕࡰࡦࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡸࡧࡨ࡫ࡥࡥࡧࡧࠤ࡫ࡵࡲࠡࠩࠥᮇ") + str(path) + bstack1ll1l1_opy_ (u"ࠨࠧ࠯ࠤᮈ"))
            return path
        except Exception as e:
            logger.debug(bstack1ll1l1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡶࡲࠣࡪ࡮ࡲࡥࠡࠩࡾࡴࡦࡺࡨࡾࠩ࠽ࠤࠧᮉ") + str(e) + bstack1ll1l1_opy_ (u"ࠣࠤᮊ"))
    logger.debug(bstack1ll1l1_opy_ (u"ࠤࡄࡰࡱࠦࡰࡢࡶ࡫ࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠳ࠨᮋ"))
    return None
@measure(event_name=EVENTS.bstack11ll1ll1lll_opy_, stage=STAGE.bstack1llll1l1_opy_)
def bstack1lll11l1111_opy_(binary_path, bstack1llll111l11_opy_, bs_config):
    logger.debug(bstack1ll1l1_opy_ (u"ࠥࡇࡺࡸࡲࡦࡰࡷࠤࡈࡒࡉࠡࡒࡤࡸ࡭ࠦࡦࡰࡷࡱࡨ࠿ࠦࡻࡾࠤᮌ").format(binary_path))
    bstack11l1l11ll11_opy_ = bstack1ll1l1_opy_ (u"ࠫࠬᮍ")
    bstack11ll111llll_opy_ = {
        bstack1ll1l1_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪᮎ"): __version__,
        bstack1ll1l1_opy_ (u"ࠨ࡯ࡴࠤᮏ"): platform.system(),
        bstack1ll1l1_opy_ (u"ࠢࡰࡵࡢࡥࡷࡩࡨࠣᮐ"): platform.machine(),
        bstack1ll1l1_opy_ (u"ࠣࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳࠨᮑ"): bstack1ll1l1_opy_ (u"ࠩ࠳ࠫᮒ"),
        bstack1ll1l1_opy_ (u"ࠥࡷࡩࡱ࡟࡭ࡣࡱ࡫ࡺࡧࡧࡦࠤᮓ"): bstack1ll1l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᮔ")
    }
    try:
        if binary_path:
            bstack11ll111llll_opy_[bstack1ll1l1_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪᮕ")] = subprocess.check_output([binary_path, bstack1ll1l1_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢᮖ")]).strip().decode(bstack1ll1l1_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᮗ"))
        response = requests.request(
            bstack1ll1l1_opy_ (u"ࠨࡉࡈࡘࠬᮘ"),
            url=bstack1l11ll111l_opy_(bstack11lll11111l_opy_),
            headers=None,
            auth=(bs_config[bstack1ll1l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᮙ")], bs_config[bstack1ll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᮚ")]),
            json=None,
            params=bstack11ll111llll_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1ll1l1_opy_ (u"ࠫࡺࡸ࡬ࠨᮛ") in data.keys() and bstack1ll1l1_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡩࡥࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫᮜ") in data.keys():
            logger.debug(bstack1ll1l1_opy_ (u"ࠨࡎࡦࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡣ࡫ࡱࡥࡷࡿࠬࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡥ࡭ࡳࡧࡲࡺࠢࡹࡩࡷࡹࡩࡰࡰ࠽ࠤࢀࢃࠢᮝ").format(bstack11ll111llll_opy_[bstack1ll1l1_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᮞ")]))
            bstack11l1l11l1l1_opy_ = bstack11l1l1l1l1l_opy_(data[bstack1ll1l1_opy_ (u"ࠨࡷࡵࡰࠬᮟ")], bstack1llll111l11_opy_)
            bstack11l1l11ll11_opy_ = os.path.join(bstack1llll111l11_opy_, bstack11l1l11l1l1_opy_)
            os.chmod(bstack11l1l11ll11_opy_, 0o777) # bstack11ll11ll11l_opy_ permission
            return bstack11l1l11ll11_opy_
    except Exception as e:
        logger.debug(bstack1ll1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡴࡥࡸࠢࡖࡈࡐࠦࡻࡾࠤᮠ").format(e))
    return binary_path
@measure(event_name=EVENTS.bstack11ll1l1l111_opy_, stage=STAGE.bstack1llll1l1_opy_)
def bstack11l1l1l1l1l_opy_(bstack11ll111lll1_opy_, bstack11l1lllll1l_opy_):
    logger.debug(bstack1ll1l1_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯࠽ࠤࠧᮡ") + str(bstack11ll111lll1_opy_) + bstack1ll1l1_opy_ (u"ࠦࠧᮢ"))
    zip_path = os.path.join(bstack11l1lllll1l_opy_, bstack1ll1l1_opy_ (u"ࠧࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࡡࡩ࡭ࡱ࡫࠮ࡻ࡫ࡳࠦᮣ"))
    bstack11l1l11l1l1_opy_ = bstack1ll1l1_opy_ (u"࠭ࠧᮤ")
    with requests.get(bstack11ll111lll1_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1ll1l1_opy_ (u"ࠢࡸࡤࠥᮥ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1ll1l1_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺ࠰ࠥᮦ"))
    with zipfile.ZipFile(zip_path, bstack1ll1l1_opy_ (u"ࠩࡵࠫᮧ")) as zip_ref:
        bstack11ll11lll1l_opy_ = zip_ref.namelist()
        if len(bstack11ll11lll1l_opy_) > 0:
            bstack11l1l11l1l1_opy_ = bstack11ll11lll1l_opy_[0] # bstack11ll11ll1ll_opy_ bstack11lll111l11_opy_ will be bstack11l1l1111l1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11l1lllll1l_opy_)
        logger.debug(bstack1ll1l1_opy_ (u"ࠥࡊ࡮ࡲࡥࡴࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡧࡻࡸࡷࡧࡣࡵࡧࡧࠤࡹࡵࠠࠨࠤᮨ") + str(bstack11l1lllll1l_opy_) + bstack1ll1l1_opy_ (u"ࠦࠬࠨᮩ"))
    os.remove(zip_path)
    return bstack11l1l11l1l1_opy_
def get_cli_dir():
    bstack11l1l1ll1ll_opy_ = bstack1ll1111ll11_opy_()
    if bstack11l1l1ll1ll_opy_:
        bstack1llll111l11_opy_ = os.path.join(bstack11l1l1ll1ll_opy_, bstack1ll1l1_opy_ (u"ࠧࡩ࡬ࡪࠤ᮪"))
        if not os.path.exists(bstack1llll111l11_opy_):
            os.makedirs(bstack1llll111l11_opy_, mode=0o777, exist_ok=True)
        return bstack1llll111l11_opy_
    else:
        raise FileNotFoundError(bstack1ll1l1_opy_ (u"ࠨࡎࡰࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡪࡴࡸࠠࡵࡪࡨࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹ࠯ࠤ᮫"))
def bstack1lll11ll11l_opy_(bstack1llll111l11_opy_):
    bstack1ll1l1_opy_ (u"ࠢࠣࠤࡊࡩࡹࠦࡴࡩࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯࡮ࠡࡣࠣࡻࡷ࡯ࡴࡢࡤ࡯ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠯ࠤࠥࠦᮬ")
    bstack11l1l1ll1l1_opy_ = [
        os.path.join(bstack1llll111l11_opy_, f)
        for f in os.listdir(bstack1llll111l11_opy_)
        if os.path.isfile(os.path.join(bstack1llll111l11_opy_, f)) and f.startswith(bstack1ll1l1_opy_ (u"ࠣࡤ࡬ࡲࡦࡸࡹ࠮ࠤᮭ"))
    ]
    if len(bstack11l1l1ll1l1_opy_) > 0:
        return max(bstack11l1l1ll1l1_opy_, key=os.path.getmtime) # get bstack11ll11111ll_opy_ binary
    return bstack1ll1l1_opy_ (u"ࠤࠥᮮ")